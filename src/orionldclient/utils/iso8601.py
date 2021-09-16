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

from typing import Union
from datetime import datetime, date, time
from contextlib import suppress

from orionldclient.model.constants import TemporalType


def from_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def utcnow() -> str:
    return from_datetime(datetime.utcnow())


def from_date(value: date):
    return value.strftime("%Y-%m-%d")


def from_time(value: time):
    return value.strftime("%H:%M:%SZ")


def from_string(value: str) -> tuple[str, TemporalType]:
    with suppress(ValueError):
        if len(value) == 20:
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
            return value, TemporalType.DATETIME
        elif len(value) == 10:
            datetime.strptime(value, "%Y-%m-%d")
            return value, TemporalType.DATE
        elif len(value) == 9:
            datetime.strptime(value, "%H:%M:%SZ")
            return value, TemporalType.TIME
    raise ValueError(f"Bad date format : {value}")


def parse(value: Union[datetime, date, time, str]) -> tuple[str, TemporalType]:
    if isinstance(value, datetime):
        return from_datetime(value), TemporalType.DATETIME
    if isinstance(value, date):
        return from_date(value), TemporalType.DATE
    if isinstance(value, time):
        return from_time(value), TemporalType.TIME
    if isinstance(value, str):
        return from_string(value)
    raise ValueError(f"Bad date format : {value}")
