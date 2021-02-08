#!/usr/bin/env python3
"""The sixth option."""
import argparse
import logging
import sys
from typing import Optional, Sequence

from discord.ext import commands

__version__ = "0.1"
NOT_HANGOUTS_GENERAL_CHANNEL_ID = 739551135173705743


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
        channel = bot.get_channel(NOT_HANGOUTS_GENERAL_CHANNEL_ID)
        await channel.send("I'm back")

    @bot.command()
    async def ping(ctx):
        await ctx.send("pong")

    @bot.command()
    async def bye(ctx):
        await ctx.send("I'll be back...")
        sys.exit()

    bot.run(token)


if __name__ == "__main__":
    main()
