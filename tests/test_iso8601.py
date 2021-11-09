#!/usr/bin/env python3

# Software Name: python-orion-client
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.
# SPDX-License-Identifier: Apache-2.0

import pytest

from datetime import datetime, date, time
from orionldclient.utils import iso8601
from orionldclient.model.constants import TemporalType


def test_from_datetime():
    d = datetime(2021, 9, 17, 9, 25)
    assert iso8601.from_datetime(d) == "2021-09-17T09:25:00Z"


def test_from_date():
    d = date(2021, 9, 17)
    assert iso8601.from_date(d) == "2021-09-17"


def test_from_time():
    t = time(9, 25)
    assert iso8601.from_time(t) == "09:25:00Z"


def test_parse_datetime():
    d = "2021-09-17T09:25:00Z"
    assert iso8601.parse(d) == (d, TemporalType.DATETIME, datetime(2021, 9, 17, 9, 25))


def test_parse_date():
    d = "2021-09-17"
    assert iso8601.parse(d) == (d, TemporalType.DATE, None)


def test_parse_time():
    d = "09:25:00Z"
    assert iso8601.parse(d) == (d, TemporalType.TIME, None)


def test_parse_bad_format_bad_length():
    d = "2021-09-17T09:25:00"
    with pytest.raises(ValueError):
        iso8601.parse(d)


def test_parse_bad_format_wrong_date():
    d = "2021-13-17T09:25:00Z"
    with pytest.raises(ValueError):
        iso8601.parse(d)


def test_extract_datetime():
    dt = iso8601.extract(
        "urn:ngsi-ld:WeatherObserved:Spain-WeatherObserved-Valladolid-2016-11-30T07:00:00Z"
    )
    assert dt == datetime(2016, 11, 30, 7, 0)


def test_extract_datetime_not_found():
    dt = iso8601.extract(
        "urn:ngsi-ld:WeatherObserved:Spain-WeatherObserved-Valladolid-2016-13-30T07:00:00Z"
    )
    assert dt is None
