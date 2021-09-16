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

from typing import Optional
from datetime import datetime, date, time
from contextlib import suppress

from orionldclient.model.constants import TemporalType


def from_datetime(date: datetime) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


def utcnow() -> str:
    return from_datetime(datetime.utcnow())


def from_date(date: date):
    return date.strftime("%Y-%m-%d")


def from_time(time: time):
    return time.strftime("%H:%M:%SZ")


def parse(date: str) -> TemporalType:
    if len(date) == 20:
        with suppress(ValueError):
            datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            return TemporalType.DATETIME
    elif len(date) == 10:
        with suppress(ValueError):
            datetime.strptime(date, "%Y-%m-%d")
            return TemporalType.DATE
    elif len(date) == 9:
        with suppress(ValueError):
            datetime.strptime(date, "%H:%M:%SZ")
            return TemporalType.TIME
    raise ValueError(f"Bad date format : {date}")
