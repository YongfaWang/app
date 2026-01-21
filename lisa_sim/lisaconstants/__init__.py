#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""LISA Python Constant module."""

import importlib.metadata

from .constants import Constant

# Automatically set by `poetry dynamic-versioning`
__version__ = "0.0.0"

try:
    metadata = importlib.metadata.metadata("lisaconstants").json
    __author__ = metadata["author"]
    __email__ = metadata["author_email"]
except importlib.metadata.PackageNotFoundError:
    pass


# Iterate over constants and set their values as
# attributes of the current module for easy access
for name, constant in Constant.ALL.items():
    vars()[name] = constant.value
