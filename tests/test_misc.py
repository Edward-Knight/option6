"""Test miscellaneous functions in option6/__init__.py."""
import re
import subprocess
from pathlib import Path

from option6 import __version__, git_hash, update_and_reinstall, version_on_disk


def test_git_hash(git_repo):
    assert re.match("^[0-9A-Fa-f]{7}$", git_hash())


def test_version_on_disk():
    assert version_on_disk() == __version__


def test_update_and_reinstall(git_repo: Path):
    # create virtual environment (to allow install)
    subprocess.check_call(("python3", "-m", "venv", ".venv"))
    assert (git_repo / ".venv").is_dir()

    update_and_reinstall()
