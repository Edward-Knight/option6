"""Test bot functionality outside of commands."""
from unittest.mock import Mock

import discord.ext.test as dpytest
import pytest
from discord.ext.commands import Bot


@pytest.mark.asyncio
async def test_say_goodbye_and_close(bot: Bot):
    # patch bot.get_channel so a valid channel is returned
    get_channel_mock = Mock(bot.get_channel)
    get_channel_mock.return_value = next(iter(bot.get_all_channels()))
    bot.get_channel = get_channel_mock
    # patch websocket so it can be "closed"
    bot.ws.socket = Mock()

    await bot.close()
    get_channel_mock.assert_called_once()
    assert dpytest.verify().message().content("I'll be back...")
