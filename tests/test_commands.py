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

    with patch.object(wolfram_alpha, "query", return_value="General Kenobi") as mock_query:
        await dpytest.message("/ask Hello there")
        dpytest.verify_message("General Kenobi")
        mock_query.assert_called_once_with("Hello there")


@pytest.mark.asyncio
async def test_eval():
    bot = make_bot(0xED)
    dpytest.configure(bot)

    await dpytest.message("/eval 1 + 2")
    dpytest.verify_message("3")


@pytest.mark.asyncio
async def test_exec():
    bot = make_bot(0xED)
    dpytest.configure(bot)

    code_block = """/code
Ignore this line
```
def add_one(x: int) -> int:
    return x + 1
```
Ignore this line too
"""

    await dpytest.message(code_block)
    await dpytest.run_all_events()
    # todo: verify message react
    await dpytest.message("/eval add_one(2)")
    dpytest.verify_message("3")
