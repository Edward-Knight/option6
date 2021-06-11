import os
import subprocess
from pathlib import Path
from typing import Generator

import pytest


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
