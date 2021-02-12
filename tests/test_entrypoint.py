"""Test the entry point exposed by this module."""
import subprocess


def test_help():
    subprocess.check_call(["option6", "--help"])


def test_version():
    subprocess.check_call(["option6", "--version"])


def test_module_interface():
    subprocess.check_call(["python", "-m", "option6", "--version"])
