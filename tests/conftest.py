import os
import subprocess
from pathlib import Path
from typing import AsyncGenerator, Generator

import discord.ext.test as dpytest
import pytest
from discord.ext.commands import Bot

import option6
from option6.__main__ import make_bot


@pytest.fixture(scope="session", autouse=True)
def patch_var_dir(tmp_path_factory) -> None:
    var_dir = tmp_path_factory.mktemp("var") / "local" / "option6"
    globals_file = var_dir / "globals.py"
    option6.__main__.OPTION6_VAR_DIR = var_dir
    option6.__main__.OPTION6_GLOBALS_FILE = globals_file


@pytest.fixture
def git_repo(tmp_path) -> Generator[Path, None, None]:
    """Run a test inside the Option 6 git repository.

    Requires an internet connection.
    """
    previous_dir = os.getcwd()
    os.chdir(tmp_path)
    try:
        subprocess.check_call(
            ("git", "clone", "--depth", "1", "https://github.com/Edward-Knight/option6.git")
        )
        os.chdir("option6")
        current_dir = Path(os.getcwd())
        assert current_dir.is_dir()
        assert (current_dir / ".git").is_dir()
        yield current_dir
    finally:
        os.chdir(previous_dir)


@pytest.fixture
async def bot(event_loop) -> AsyncGenerator[Bot, None]:
    bot = make_bot(0xED, event_loop)
    dpytest.configure(bot)
    yield bot
    # Despite this test fixture being function scoped,
    # the message queue persists between tests,
    # so we need to clear it after each test.
    await dpytest.empty_queue()
