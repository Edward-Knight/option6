"""Test miscellaneous functions in option6/__init__.py."""
import re

from option6 import git_hash


def test_git_hash(git_repo):
    assert re.match("^[0-9A-Fa-f]{7}$", git_hash())
