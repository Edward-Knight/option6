"""Test the bot commands."""
from unittest.mock import patch

import discord.ext.test as dpytest
import pytest

from option6 import wolfram_alpha


@pytest.mark.asyncio
async def test_ping(bot):
    await dpytest.message("/ping")
    assert dpytest.verify().message().content("pong")


@pytest.mark.asyncio
async def test_ask(bot):
    with patch.object(wolfram_alpha, "query", return_value="General Kenobi") as mock_query:
        await dpytest.message("/ask Hello there")
        assert dpytest.verify().message().content("General Kenobi")
        mock_query.assert_called_once_with("Hello there")


@pytest.mark.asyncio
async def test_eval(bot):
    await dpytest.message("/eval 1 + 2")
    assert dpytest.verify().message().content("3")


@pytest.mark.asyncio
async def test_exec(bot):
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
    assert dpytest.verify().message().content("3")
