#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

"""
This module contains utils functions to deal with graphs.
"""

from typing import Set, Tuple

class CacheArc:

    def __init__(self):
        self._cache: Set[Tuple[str, str]] = set()

    def put(self, source: str, target: str):
        self._cache.add((source, target))

    def is_cached(self, source: str, target: str) -> bool:
        return (source, target) in self._cache or (target, source) in self._cache
