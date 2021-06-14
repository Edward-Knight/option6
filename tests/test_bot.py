"""Test bot functionality outside of commands."""
import asyncio
import inspect
import textwrap
from pathlib import Path
from typing import Generator, Tuple
from unittest.mock import Mock

import discord.ext.test as dpytest
import pytest
from discord.ext.commands import Bot

import option6
from option6.__main__ import load_globals, save_replay


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


@pytest.fixture
def globals_fixture(tmp_path: Path) -> Generator[Tuple[Path, Path], None, None]:
    # override var dir and globals file
    previous_var_dir = option6.__main__.OPTION6_VAR_DIR
    previous_globals_file = option6.__main__.OPTION6_GLOBALS_FILE
    var_dir = tmp_path / "var" / "local" / "option6"
    var_dir.mkdir(parents=True)
    globals_file = var_dir / "globals.py"
    option6.__main__.OPTION6_VAR_DIR = var_dir
    option6.__main__.OPTION6_GLOBALS_FILE = globals_file

    try:
        yield var_dir, globals_file
    finally:
        # restore var dir and globals file
        option6.__main__.OPTION6_VAR_DIR = previous_var_dir
        option6.__main__.OPTION6_GLOBALS_FILE = previous_globals_file


def test_load_globals_no_file(globals_fixture: Tuple[Path, Path], capsys):
    var_dir, globals_file = globals_fixture
    assert not globals_file.exists()
    assert load_globals(None) == {"bot": None}
    stdout, _ = capsys.readouterr()
    assert stdout == f"{globals_file} is not a file, not loading globals\n"


def test_load_globals_with_file(globals_fixture: Tuple[Path, Path]):
    var_dir, globals_file = globals_fixture
    replay = "test_key = 'test_value'"
    globals_file.write_text(replay)
    loaded_globals = load_globals("test_bot")
    assert "__builtins__" in loaded_globals
    assert loaded_globals["bot"] == "test_bot"
    assert loaded_globals["test_key"] == "test_value"
    assert len(loaded_globals) == 3


def test_load_globals_complex_object(globals_fixture: Tuple[Path, Path]):
    """This fails for a pickle-backed store, but passes for a dill-backed store."""
    var_dir, globals_file = globals_fixture
    replay = "test_key = lambda x: x + 1"
    globals_file.write_text(replay)
    loaded_globals = load_globals(None)
    assert loaded_globals["test_key"](2) == 3


@pytest.mark.asyncio
async def test_load_globals_very_complex_object(globals_fixture: Tuple[Path, Path]):
    """This fails for both a pickle-backed store, and a dill-backed store."""
    var_dir, globals_file = globals_fixture

    class ComplexClass:
        @staticmethod
        async def complex_function(cls):
            await asyncio.sleep(0)
            return 3

    globals_file.write_text(textwrap.dedent(inspect.getsource(ComplexClass)))
    loaded_globals = load_globals(None)
    exec("import asyncio", loaded_globals)
    assert (await eval("ComplexClass.complex_function(ComplexClass)", loaded_globals)) == 3


@pytest.mark.asyncio
async def test_load_globals_register_bot_command(globals_fixture: Tuple[Path, Path], bot: Bot):
    var_dir, globals_file = globals_fixture

    src = """
    @bot.command()
    async def test(ctx):
        await ctx.send("test!")
    """
    globals_file.write_text(textwrap.dedent(src))
    load_globals(bot)

    await dpytest.message("/test")
    assert dpytest.verify().message().content("test!")


def test_load_globals_corrupt_file(globals_fixture: Tuple[Path, Path], capsys):
    var_dir, globals_file = globals_fixture
    globals_file.write_text("x = 0\nx++")
    assert set(load_globals(None).keys()) == {"__builtins__", "bot"}
    stdout, _ = capsys.readouterr()
    assert "Failed to load globals: SyntaxError:" in stdout


def test_save_replay_no_directory(globals_fixture: Tuple[Path, Path], capsys):
    var_dir, globals_file = globals_fixture
    var_dir.rmdir()
    assert not var_dir.exists()
    save_replay("")
    stdout, _ = capsys.readouterr()
    assert stdout == f"{var_dir} is not a directory, not saving replay data\n"


def test_save_replay_with_directory(globals_fixture: Tuple[Path, Path]):
    var_dir, globals_file = globals_fixture
    assert var_dir.exists()
    replay = "test_key = 'test_value'"
    save_replay(replay)
    assert globals_file.read_text() == replay


def test_save_replay_complex_object(globals_fixture):
    """This fails for a pickle-backed store,
    but passes for a dill-backed store,
    and passes for a source-code-backed store.
    """
    var_dir, globals_file = globals_fixture
    replay = "test_key = lambda x: x + 1"
    save_replay(replay)
    assert globals_file.read_text() == replay


def test_save_replay_very_complex_object(globals_fixture):
    """This fails for both a pickle-backed store, and a dill-backed store,
    but passes for a source-code-backed store.
    """
    var_dir, globals_file = globals_fixture

    class ComplexClass:
        @staticmethod
        async def complex_function(cls):
            await asyncio.sleep(0)
            return 3

    replay = inspect.getsource(ComplexClass)
    save_replay(replay)
    assert globals_file.read_text() == replay


def test_save_replay_without_permission(globals_fixture: Tuple[Path, Path], capsys):
    var_dir, globals_file = globals_fixture
    var_dir.chmod(444)
    save_replay("")
    stdout, _ = capsys.readouterr()
    assert stdout.startswith("Failed to save replay data: PermissionError:")
