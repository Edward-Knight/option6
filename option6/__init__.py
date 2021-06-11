"""The sixth option."""
import json
import subprocess
from typing import IO, Any, MutableMapping

__version__ = "1.5.6"
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
