#!/usr/bin/env python3
"""The sixth option."""
import argparse
from typing import Optional, Sequence

__version__ = "0.1"


def main(argv: Optional[Sequence[str]] = None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.parse_args(argv)


if __name__ == "__main__":
    main()
