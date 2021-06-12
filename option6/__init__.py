"""The sixth option."""
import asyncio
import json
import subprocess
from typing import IO, Any, MutableMapping

__version__ = "1.7.1"
GIT_HASH = "unknown"

KEYS: MutableMapping[str, Any] = {
    "channel_id": 739761480471150613,
}


def update_keys(key_file: IO) -> None:
    """Update the {KEYS} global with keys loaded from {key_file}."""
    global KEYS
    KEYS.update(json.load(key_file))


def git_hash() -> str:
    """Get the short commit hash of the HEAD commit.

    Must be called with a git repo in the current directory.

    May raise a CalledProcessError.
    """
    return subprocess.check_output(("git", "rev-parse", "--short", "HEAD"), text=True).strip()


def version_on_disk() -> str:
    """Load the current version of Option 6 on disk."""
    grep_command = ("grep", "-m", "1", "-o", '__version__ = ".*"', "option6/__init__.py")
    version_string = subprocess.check_output(grep_command, text=True).strip()
    return version_string.split()[-1].strip('"')


async def update_and_reinstall() -> None:
    """Pull changes from origin/trunk and reinstall.

    Runs tasks in background threads.
    """
    kwargs = {"stdin": subprocess.DEVNULL, "stdout": None, "stderr": None}
    # update
    await asyncio.create_subprocess_exec("git", "fetch", "origin", **kwargs)  # type: ignore
    await asyncio.create_subprocess_exec(
        "git", "reset", "--hard", "origin/trunk", **kwargs  # type: ignore
    )
    # reinstall
    await asyncio.create_subprocess_exec(
        ".venv/bin/python", "-m", "pip", "install", ".", **kwargs  # type: ignore
    )
