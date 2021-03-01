"""Tests for option6.turtle."""
import subprocess
from pathlib import Path

import py.path

from option6.turtle import make_turtle, save_turtle  # type: ignore


def check_file_mime(file_path: Path, mime_type: str):
    """Check that a file exists and is of the correct format.

    Uses the `file` command to match the {mime_type}.
    """
    assert file_path.exists()
    command = ["file", "--brief", "--mime-type", str(file_path)]
    p = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    assert p.returncode == 0
    assert p.stdout.strip() == mime_type


def test_make_png(tmpdir: py.path.local):
    file_path = Path(tmpdir.strpath) / "test.png"
    with open(file_path, "wb") as f:
        f.write(save_turtle(make_turtle()).read())
    check_file_mime(file_path, "image/png")
