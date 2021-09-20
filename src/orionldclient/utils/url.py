#!/usr/bin/env python3

# Software Name: python-orion-client
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battelo@orange.com> et al.
# SPDX-License-Identifier: Apache-2.0

import urllib.parse
import re

URL_PATTERN = re.compile("^http[s]{0,1}:")


def escape(value: str) -> str:
    return urllib.parse.quote(value)


def unescape(value: str) -> str:
    return urllib.parse.unquote(value)


def isurl(value: str) -> bool:
    return URL_PATTERN.match(value)
