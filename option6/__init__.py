"""The sixth option."""
import json
from typing import IO, Any, MutableMapping

__version__ = "1.5.2"

KEYS: MutableMapping[str, Any] = {
    "channel_id": 739761480471150613,
}


def update_keys(key_file: IO) -> None:
    """Update the {KEYS} global with keys loaded from {key_file}."""
    global KEYS
    KEYS.update(json.load(key_file))
