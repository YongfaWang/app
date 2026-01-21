#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Console script to generate headers."""

import os
from argparse import ArgumentParser

from . import __version__
from .headers import CHeaderGenerator, CppHeaderGenerator


def generate_header() -> None:
    """Console script to generate header file.

    usage: python -m lisaconstants [-h] [--dir DIR] {c,cpp}

    Generate LISA Constants header files.

    positional arguments:
      {c,cpp}     header file format

    options:
      -h, --help  show this help message and exit
      --dir DIR   path to output directory
    """
    # Package path
    package_path = os.path.dirname(os.path.abspath(__file__))

    # Define command-line arguments
    parser = ArgumentParser(
        prog="python -m lisaconstants",
        description="Generate LISA Constants header files.",
    )
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"lisaconstants {__version__} from {package_path}",
    )
    parser.add_argument(
        "format",
        choices=["c", "cpp"],
        help="header file format",
    )
    parser.add_argument(
        "--dir",
        default=".",
        help="path to output directory",
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Generate header file
    if args.format == "c":
        path = os.path.join(args.dir, "lisaconstants.h")
        CHeaderGenerator().write(path)
    elif args.format == "cpp":
        path = os.path.join(args.dir, "lisaconstants.hpp")
        CppHeaderGenerator().write(path)
    else:
        raise ValueError(f"Invalid format '{args.format}', choose 'c' or 'cpp'.")
    print(f"Header file generated at '{os.path.abspath(path)}'")


if __name__ == "__main__":
    generate_header()
