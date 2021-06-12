import os
import subprocess
from pathlib import Path
from typing import AsyncGenerator, Generator

import discord.ext.test as dpytest
import pytest
from discord.ext.commands import Bot

from option6.__main__ import make_bot


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
