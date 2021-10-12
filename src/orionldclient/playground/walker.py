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

import uuid
from random import random
from base64 import urlsafe_b64encode


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


def uuidshortener(uuid: uuid.UUID) -> str:
    return urlsafe_b64encode(uuid.bytes).decode().rstrip("=")


def shortuuid(random: bool = False) -> str:
    uid = uuid.uuid1() if random else uuid.uuid4()
    return uuidshortener(uid)
