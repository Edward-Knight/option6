"""Test the bot commands."""
from unittest.mock import patch

import discord.ext.test as dpytest
import pytest

from option6 import wolfram_alpha
from option6.__main__ import make_bot


@pytest.mark.asyncio
async def test_ping():
    bot = make_bot(0xED)

    dpytest.configure(bot)

    await dpytest.message("/ping")
    dpytest.verify_message("pong")


@pytest.mark.asyncio
async def test_ask():
    bot = make_bot(0xED)
    dpytest.configure(bot)

    with patch.object(wolfram_alpha, "query", return_value="test") as mock_query:
        await dpytest.message("/ask hello")
        dpytest.verify_message("test")
        mock_query.assert_called_once_with("hello")
