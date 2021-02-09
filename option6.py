#!/usr/bin/env python3
"""The sixth option."""
import argparse
import logging
import sys
from typing import Optional, Sequence

from discord.ext import commands

__version__ = "1.1.0"
NOT_HANGOUTS_PROGRAMMING_CHANNEL_ID = 739761480471150613


def main(argv: Optional[Sequence[str]] = None):
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("token_file", type=argparse.FileType())
    args = parser.parse_args(argv)

    token = args.token_file.read().strip()
    args.token_file.close()

    bot = commands.Bot(command_prefix="/")

    @bot.event
    async def on_ready():
        print("Logged in as", bot.user.name, bot.user.id)
        channel = bot.get_channel(NOT_HANGOUTS_PROGRAMMING_CHANNEL_ID)
        await channel.send("I'm back")

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

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        # are you talking behind my back?
        mentions = ["option 6", "option six"]
        if any(mention in message.content.lower() for mention in mentions):
            await message.channel.send(f"Are you talking behind my back, {message.author.name}?")

    bot.run(token)


if __name__ == "__main__":
    main()
