"""Test miscellaneous functions in option6/__init__.py."""
import io
import re
import subprocess
from pathlib import Path

import pytest

import option6
from option6 import __version__, git_hash, update_and_reinstall, update_keys, version_on_disk


def test_update_keys():
    f = io.StringIO('{"test_key": "test_value"}')
    assert "test_key" not in option6.KEYS
    update_keys(f)
    assert option6.KEYS["test_key"] == "test_value"


def test_git_hash(git_repo):
    assert re.match("^[0-9A-Fa-f]{7}$", git_hash())


def test_version_on_disk():
    assert version_on_disk() == __version__


@pytest.mark.asyncio
async def test_update_and_reinstall(git_repo: Path):
    # create virtual environment (to allow install)
    subprocess.check_call(("python3", "-m", "venv", ".venv"))
    assert (git_repo / ".venv").is_dir()

    await update_and_reinstall()
