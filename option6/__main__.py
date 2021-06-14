#!/usr/bin/env python3
"""The sixth option."""
import argparse
import asyncio
import logging
import math
import random
import re
import traceback
from datetime import datetime
from pathlib import Path
from types import MethodType
from typing import Any, Dict, Optional, Sequence

from discord import Intents
from discord.ext import commands
from discord.file import File

import option6
from option6 import (
    KEYS,
    __version__,
    git_hash,
    update_and_reinstall,
    update_keys,
    version_on_disk,
    wolfram_alpha,
)
from option6.helpers.message_handler import HANDLERS
from option6.helpers.message_publisher import MessagePublisher
from option6.turtle import draw_spirograph, make_screen, save_canvas  # type: ignore

OPTION6_VAR_DIR = Path("/var/local/option6")
"""Directory to store persistent data in."""
OPTION6_GLOBALS_FILE = OPTION6_VAR_DIR / "globals.py"
"""File to store persistent globals data in."""


def load_globals() -> Dict[str, Any]:
    """Attempt to load and execute replay data from disk.

    If it fails, returns an empty dict.
    """
    globals_: Dict[str, Any] = {}

    if not OPTION6_GLOBALS_FILE.is_file():
        print(OPTION6_GLOBALS_FILE, "is not a file, not loading globals")
        return globals_

    try:
        with open(OPTION6_GLOBALS_FILE) as f:
            src = f.read()
        number_of_lines = src.count("\n")
        print(f"Replaying {number_of_lines} lines of code")
        exec(src, globals_)
        return globals_
    except Exception as e:
        print(f"Failed to load globals: {e.__class__.__name__}: {e}\n{traceback.format_exc()}")
        return globals_


def save_replay(replay: str) -> None:
    """Attempt to save replay data to disk."""
    if not OPTION6_GLOBALS_FILE.parent.is_dir():
        print(OPTION6_GLOBALS_FILE.parent, "is not a directory, not saving replay data")
        return

    try:
        with open(OPTION6_GLOBALS_FILE, "a") as f:
            f.write(replay)
    except Exception as e:
        print(f"Failed to save replay data: {e.__class__.__name__}: {e}\n{traceback.format_exc()}")


def make_bot(channel_id: int, loop: Optional[asyncio.AbstractEventLoop] = None) -> commands.Bot:
    # set up intents
    intents = Intents.default()
    intents.members = True

    # create bot instance
    bot = commands.Bot("/", intents=intents, loop=loop)

    # set attributes
    bot._globals = load_globals()
    """Environment for executing arbitrary code."""
    bot._globals["bot"] = bot
    bot._replay = ""
    """Source code to recreate changes to bot._globals."""
    bot._start_time = datetime.now()
    """Used by the /age command."""

    # override close
    original_close = bot.close

    async def close(self) -> None:
        """Overridden Client.close method.

        Sends a goodbye message to the channel before closing.
        Saves the bot._replay data to disk.
        """
        channel = self.get_channel(channel_id)
        await channel.send("I'll be back...")
        await original_close()
        save_replay(self._replay)

    bot.close = MethodType(close, bot)

    @bot.event
    async def on_ready():
        print("Logged in as", bot.user.name, bot.user.id)
        channel = bot.get_channel(channel_id)
        await channel.send("I'm back")

    # set up custom on_message handlers
    publisher = MessagePublisher()
    for handler in HANDLERS:
        publisher.subscribe(handler())

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        # publish the message
        await bot.process_commands(message)
        await publisher.publish(message)

    @bot.event
    async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
        if hasattr(error, "original"):
            error = error.original
        await ctx.send(
            "\n".join(
                [
                    "Mr. Stark... I don't feel so good...",
                    "```",
                    "".join(traceback.TracebackException.from_exception(error).format()),
                    "```",
                ]
            )
        )

    @bot.command()
    async def version(ctx):
        await ctx.send(f"I am version {__version__} (`{option6.GIT_HASH}`)")

    @bot.command()
    async def ping(ctx):
        await ctx.send("pong")

    @bot.command()
    async def bye(_ctx):
        """Restart Option 6."""
        await bot.close()

    @bot.command()
    async def update(ctx):
        await ctx.send(
            f"I am currently running version {__version__} (`{option6.GIT_HASH}`).\n"
            f"The current version on disk is {version_on_disk()} (`{git_hash()}`)."
        )
        await update_and_reinstall()
        await ctx.send(
            f"Updated version on disk to {version_on_disk()} (`{git_hash()}`).\n"
            f"Load the new version with `/bye`."
        )

    @bot.command()
    async def roll(ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split("d"))

            if rolls < 0 or limit < 0:
                await ctx.send("No negative rolls or dice!")
                return

        except ValueError:
            await ctx.send("Format has to be in NdN!")
            return

        result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @bot.command()
    async def age(ctx):
        time_since_start = datetime.now() - bot._start_time
        secs = time_since_start.seconds
        minutes = math.floor(secs / 60)
        hours = math.floor(minutes / 60)
        days = time_since_start.days

        if days >= 1:
            await ctx.send(f"I have been alive for {days} day(s) and {hours} hour(s).")
        elif hours >= 1:
            await ctx.send(
                f"I have been alive for {hours} hour(s) and {minutes - (hours * 60)} minute(s)."
            )
        elif minutes >= 1:
            await ctx.send(
                f"I have been alive for {minutes} minute(s) and {secs - (minutes * 60)} second(s)."
            )
        else:
            await ctx.send(f"I have been alive for {secs} second(s).")

    @bot.command()
    async def spiro(ctx) -> None:
        """Make some spirograph art."""
        with make_screen() as screen:
            canvas = draw_spirograph(screen)
            fp = save_canvas(canvas)
        await ctx.send(file=File(fp, "spiro.png"))

    @bot.command()
    async def ask(ctx, *query: str) -> None:
        """Ask Wolfram|Alpha something."""
        await ctx.send(wolfram_alpha.query(" ".join(query)))

    @bot.command(name="eval")
    async def py(ctx: commands.Context, *expr: str) -> None:
        """Eval an arbitrary Python expression. Probably not a good idea."""
        await ctx.send(str(eval(" ".join(expr), bot._globals)))

    @bot.command()
    async def code(ctx: commands.Context) -> None:
        """Execute arbitrary Python statements. Probably not a good idea."""
        msg: str = ctx.message.content

        # find code block
        match = re.search(r"```.*```", msg, re.DOTALL)
        if not match:
            await ctx.send("Cannot find code block to execute 🤷")
            return
        src = match.group()[3:-3].strip()

        # exec code block
        exec(src, bot._globals)

        # if the code ran successfully
        # feedback to the user
        await ctx.message.add_reaction("✅")
        # store the code for replay
        bot._replay += f"# @{ctx.author.name} {ctx.message.created_at.isoformat()}\n{src}\n\n"

    return bot


def main(argv: Optional[Sequence[str]] = None):
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("key_file", type=argparse.FileType())
    args = parser.parse_args(argv)

    # load tokens
    update_keys(args.key_file)
    args.key_file.close()

    # store the current commit hash
    option6.GIT_HASH = git_hash()

    # create bot
    bot = make_bot(KEYS["channel_id"])

    # run bot
    bot.run(KEYS["discord"])


if __name__ == "__main__":
    main()
