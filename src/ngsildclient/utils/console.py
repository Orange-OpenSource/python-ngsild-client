#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import re
import rich.console as console
from rich.text import Text
from typing import Literal, Generator

from ngsildclient.utils import is_interactive


"""
This module contains functions to print to the console in interactive mode
"""

MsgLvl = Literal["info", "success", "warning", "error"]
MAP_LEVEL_COLOR = {"info": None, "success": "green", "warning": "orange3", "error": "red3"}
PATTERN_RICHSTYLE = re.compile(r"\[[^\]]+\]")


class Console:
    def __init__(self, verbose=True):
        self.console = console.Console() if is_interactive() else None
        self.verbose = verbose

    def message(self, msg: str, *, color: str = None, level: MsgLvl = "info"):
        if not self.verbose:
            return
        if not self.console:
            print(msg)
            return
        text = Text(msg)
        if level:
            color = MAP_LEVEL_COLOR.get(level, None)
        if color:
            text.stylize(color)
        self.console.print(text)

    def success(self):
        self.message(color="green")

    def warn(self):
        self.message(color="orange")

    def error(self):
        self.message(color="red")

    def print(self, msg: str):
        if not self.verbose:
            return
        if not self.console:
            print(re.sub(PATTERN_RICHSTYLE, "", msg))
            return
        self.console.print(msg)
