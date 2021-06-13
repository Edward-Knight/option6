"""Test bot functionality outside of commands."""
import pickle
from pathlib import Path
from unittest.mock import Mock

import discord.ext.test as dpytest
import pytest
from discord.ext.commands import Bot

import option6
from option6.__main__ import load_globals, save_globals


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


def test_load_globals(bot, tmp_path: Path, capsys):
    # override globals file
    previous_globals_file = option6.__main__.OPTION6_GLOBALS_FILE
    globals_file = tmp_path / "globals.pickle"
    option6.__main__.OPTION6_GLOBALS_FILE = globals_file

    try:
        # test with no file
        assert not globals_file.exists()
        assert load_globals() == {}
        stdout, _ = capsys.readouterr()
        assert stdout == f"{globals_file} is not a file, not loading globals\n"

        # test with file
        globals_ = {"test_key": "test_value"}
        with open(globals_file, "wb") as f:
            pickle.dump(globals_, f)
        assert load_globals() == globals_

        # test with corrupt file
        globals_file.write_text("test")
        assert load_globals() == {}
        stdout, _ = capsys.readouterr()
        assert stdout.startswith("Failed to load globals: UnpicklingError:")
    finally:
        # restore globals file
        option6.__main__.OPTION6_GLOBALS_FILE = previous_globals_file


def test_save_globals(tmp_path: Path, capsys):
    # override var dir and globals file
    previous_var_dir = option6.__main__.OPTION6_VAR_DIR
    previous_globals_file = option6.__main__.OPTION6_GLOBALS_FILE
    var_dir = tmp_path / "var" / "local" / "option6"
    globals_file = var_dir / "globals.pickle"
    option6.__main__.OPTION6_VAR_DIR = var_dir
    option6.__main__.OPTION6_GLOBALS_FILE = globals_file

    try:
        # test with no directory
        var_dir.parent.mkdir(parents=True)
        save_globals({})
        stdout, _ = capsys.readouterr()
        assert stdout == f"{var_dir} is not a directory, not saving globals\n"

        # test with directory
        var_dir.mkdir()
        globals_ = {"test_key": "test_value"}
        save_globals(globals_)
        assert load_globals() == globals_

        # test without permissions
        var_dir.chmod(444)
        save_globals({})
        stdout, _ = capsys.readouterr()
        assert stdout.startswith("Failed to save globals: PermissionError:")
    finally:
        # restore var dir and globals file
        option6.__main__.OPTION6_VAR_DIR = previous_var_dir
        option6.__main__.OPTION6_GLOBALS_FILE = previous_globals_file
