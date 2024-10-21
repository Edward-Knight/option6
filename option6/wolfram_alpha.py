"""Functions for interacting with Wolfram|Alpha."""

import functools

from wolframalpha import Client

from option6 import KEYS


@functools.lru_cache(None)
def get_client() -> Client:
    """Return a Wolfram|Alpha client singleton."""
    return Client(KEYS["wolfram"])


def query(q: str) -> str:
    """Query Wolfram|Alpha."""
    client = get_client()
    try:
        return next(client.query(q).results).text
    except StopIteration:
        return "I dunno 🤷"
