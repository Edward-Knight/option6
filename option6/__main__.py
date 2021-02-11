#!/usr/bin/env python3
"""The sixth option."""
import argparse
import logging
import random
import sys
from typing import Optional, Sequence

from discord.ext import commands

from option6 import NOT_HANGOUTS_PROGRAMMING_CHANNEL_ID, __version__


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

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        
        #Todo: would be good to import from config file

        # are you talking behind my back?
        respondToKeywords(
            message,
            ["option 6", "option six"],
            f"Are you talking behind my back, {message.author.name}?"
        )

        # dog
        respondToKeywords(
            message,
            ["hello", "tea", "breakfast", "chicken", "custards", "walkies", "treat","Betty"],
            "Woof! Woof! Wag! Wag!"
        )

        await bot.process_commands(message)

    bot.run(token)


async def respondToKeywords(message, keywords, response):
    """responds to keywords with the provided response"""
    if any(keyword in message.content.lower() for keyword in keywords):
            await message.channel.send(response)

if __name__ == "__main__":
    main()
