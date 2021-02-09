"""Test the bot commands."""
import discord.ext.test as dpytest
import pytest

from option6.__main__ import make_bot


@pytest.mark.asyncio
async def test_ping():
    bot = make_bot()

    dpytest.configure(bot)

    await dpytest.message("/ping")
    dpytest.verify_message("pong")
