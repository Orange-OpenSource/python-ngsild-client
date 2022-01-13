#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.
# SPDX-License-Identifier: Apache-2.0

from random import random


class RandomWalker:
    def __init__(
        self,
        value: float,
        multiplier: float = 1,
        allow_negative: bool = True,
    ):
        self.value = value
        self.multiplier = multiplier
        self.allow_negative = allow_negative

    def __repr__(self):
        return str(self.value)

    def walk(self):
        r = random()
        self.value += (r - 0.5) * self.multiplier
        self.value = round(self.value, 2)
        if not self.allow_negative:
            self.value = max(0, self.value)
        return self.value
