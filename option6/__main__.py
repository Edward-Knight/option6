#!/usr/bin/env python3
"""The sixth option."""
import argparse
import logging
import math
import random
import sys
from datetime import datetime
from typing import Optional, Sequence

from discord.ext import commands
from discord.file import File

from option6 import NOT_HANGOUTS_PROGRAMMING_CHANNEL_ID, __version__
from option6.helpers.message_handler import HANDLERS
from option6.helpers.message_publisher import MessagePublisher
from option6.turtle import make_turtle, save_turtle


def main(argv: Optional[Sequence[str]] = None):
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("token_file", type=argparse.FileType())
    args = parser.parse_args(argv)

    token = args.token_file.read().strip()
    args.token_file.close()

    bot = commands.Bot(command_prefix="/")

    start_time = datetime.now()

    publisher = MessagePublisher()
    for handler in HANDLERS:
        publisher.subscribe(handler())

    @bot.event
    async def on_ready():
        print("Logged in as", bot.user.name, bot.user.id)
        channel = bot.get_channel(NOT_HANGOUTS_PROGRAMMING_CHANNEL_ID)
        await channel.send("I'm back")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        # publish the message
        await publisher.publish(message)
        await bot.process_commands(message)

    @bot.command()
    async def version(ctx):
        await ctx.send(f"I am version {__version__}")

    @bot.command()
    async def ping(ctx):
        await ctx.send("pong")

    @bot.command()
    async def bye(ctx):
        await ctx.send("I'll be back...")
        sys.exit()

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
        time_since_start = datetime.now() - start_time
        secs = time_since_start.seconds
        minutes = math.floor(secs / 60)
        hours = math.floor(minutes / 60)
        days = time_since_start.days

        if days >= 1:
            await ctx.send(f"I have been alive for {days} day(s) and {hours} hour(s).")
        elif hours >= 1:
            await ctx.send(f"I have been alive for {hours} hour(s) and {minutes - (hours * 60)} minute(s).")
        elif minutes >= 1:
            await ctx.send(f"I have been alive for {minutes} minutes(s) and {secs - (minutes * 60)} second(s).")
        else:
            await ctx.send(f"I have been alive for {secs} second(s).")

    @bot.command()
    async def spiro(ctx) -> None:
        """Make some spirograph art."""
        await ctx.send(file=File(save_turtle(make_turtle()), "spiro.png"))

    bot.run(token)


if __name__ == "__main__":
    main()
