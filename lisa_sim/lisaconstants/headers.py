#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Header generation."""

import logging
from abc import ABC, abstractmethod

from jinja2 import Environment, PackageLoader, Template

from . import __version__
from .constants import Constant

logger = logging.getLogger(__name__)


class HeaderGenerator(ABC):
    """Abstract header generator.

    Args:
        constants: dictionary of `Constant` instances
    """

    def __init__(self, constants: dict[str, Constant] | None = None) -> None:
        if constants is None:
            constants = Constant.ALL
        self.constants = constants

    def write(self, filename: str, mode: str = "w") -> None:
        """Write header file.

        Args:
            filename: path to header file
        """
        content = self.generate()
        logging.info("Writing header file to '%s'", filename)
        with open(filename, mode=mode, encoding="utf-8") as file:
            file.write(content)

    @abstractmethod
    def generate(self) -> str:
        """Generate header file."""


class TemplateHeaderGenerator(HeaderGenerator):
    """Abstract base class for template-based header generators."""

    @abstractmethod
    def get_template(self, environment: Environment) -> Template:
        """Return template object."""

    def generate(self) -> str:
        loader = PackageLoader("lisaconstants", "templates")
        environment = Environment(loader=loader)
        template = self.get_template(environment)
        return template.render(constants=self.constants, version=__version__)


class CHeaderGenerator(TemplateHeaderGenerator):
    """Generate a C header file defining constants."""

    def get_template(self, environment: Environment) -> Template:
        return environment.get_template("c.txt")


class CppHeaderGenerator(TemplateHeaderGenerator):
    """Generate a C++ header file defining constants."""

    def get_template(self, environment: Environment) -> Template:
        return environment.get_template("cpp.txt")
