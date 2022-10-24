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
This module contains helper functions to generate iso8601-formatted strings from native Python date types.

Notes
-----
NGSI-LD dates are expressed in UTC, using the ISO8601 format.

References
----------
.. [1] ETSI, 2021. "Supported data types for Values" in Context Information Management (CIM); NGSI-LD API
    ETSI GS CIM 009 V1.4.2, pp. 41-42, 2021-04.
"""

from __future__ import annotations

import re
from dateutil.parser import isoparser
from dateutil.tz import UTC

from typing import Union, Optional, Literal, Tuple
from datetime import datetime, date, time
from contextlib import suppress

from ngsildclient.model.constants import TemporalType

ISO8601_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


def from_datetime(value: datetime) -> str:
    """Convert from datetime to ISO8601-formatted string.

    Parameters
    ----------
    value : datetime
        The datetime to be converted. Expected in UTC.

    Returns
    -------
    str
        ISO8601-formatted string

    Example
    -------
    >>> from datetime import datetime
    >>> from ngsildclient import iso8601
    >>> d = datetime(2021, 10, 13, 9, 29)
    >>> print(iso8601.from_datetime(d))
    2021-10-13T09:29:00Z
    """
    if value.tzinfo is None:  # naive datetime => set timezone to UTC (the datetime value remains unchanged)
        value = value.replace(tzinfo=UTC)
    elif (
        value.tzinfo != UTC
    ):  # aware datetime => convert to UTC (the datetime value is changed according to the UTC offset)
        value = value.astimezone(UTC)
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def to_datetime(value: str) -> datetime:
    return isoparser().isoparse(value)


def utcnow() -> str:
    """Converts the current UTC datetime to ISO8601-formatted string.

    Returns
    -------
    str
        The current UTC datetime, ISO8601-formatted
    """
    return from_datetime(datetime.now(UTC))


def from_date(value: date) -> str:
    """Convert from date to ISO8601-formatted string.

    Parameters
    ----------
    value : date
        The date to be converted.

    Returns
    -------
    str
        ISO8601-formatted string

    Example
    -------
    >>> from datetime import date
    >>> from ngsildclient import iso8601
    >>> d = date(2021, 10, 13)
    >>> print(iso8601.from_date(d))
    2021-10-13
    """
    return value.strftime("%Y-%m-%d")


def to_date(value: str) -> date:
    return isoparser().parse_isodate(value)


def from_time(value: time) -> str:
    """Convert from time to ISO8601-formatted string.

    Parameters
    ----------
    value : time
        The time to be converted. Expected in UTC.

    Returns
    -------
    str
        ISO8601-formatted string

    Example
    -------
    >>> from datetime import time
    >>> from ngsildclient import iso8601
    >>> d = time(9, 29)
    >>> print(iso8601.from_time(d))
    09:29:00Z
    """
    if value.tzinfo is None:  # naive time => set timezone to UTC (the time value remains unchanged)
        value = value.replace(tzinfo=UTC)
    return value.strftime("%H:%M:%SZ")


def to_time(value: str) -> time:
    return isoparser().parse_isotime(value)


def _from_string(value: str) -> tuple[str, TemporalType, datetime]:
    """Guess the temporal date type from a given string.

    This function should not be called by the end user. It is used internally by the `parse()` function.

    Parameters
    ----------
    value : str
        A string representation of either a datetime, date or time

    Returns
    -------
    tuple[str, TemporalType]
        A tuple composed of the `value` argument and the TemporalType that has been identified

    Raises
    ------
    ValueError
        The date format does not match datetime, date or time

    Example
    -------
    >>> from ngsildclient import iso8601
    >>> print(iso8601._from_string("2021-10-13"))
    ('2021-10-13', <TemporalType.DATE: 'Date'>)
    """
    with suppress(ValueError):
        if len(value) == 20:
            dt = to_datetime(value)
            return value, TemporalType.DATETIME, dt
        elif len(value) == 10:
            dt = to_date(value)
            return value, TemporalType.DATE, dt
        elif len(value) == 9:
            dt = to_time(value)
            return value, TemporalType.TIME, dt
    raise ValueError(f"Bad date format : {value}")


def from_string(type: Literal["DateTime", "Date", "Time"], value: str) -> Union[datetime, date, time]:
    with suppress(ValueError):
        if type == "DateTime":
            return to_datetime(value)
        if type == "Date":
            return to_date(value)
        if type == "Time":
            return to_time(value)
    raise ValueError(f"Bad date format : {value}")


def to_string(dt: Union[datetime, date, time]) -> Tuple[str, str]:
    if isinstance(dt, datetime):
        type = "DateTime"
        value = from_datetime(dt)
    elif isinstance(dt, date):
        type = "Date"
        value = from_date(dt)
    elif isinstance(dt, time):
        type = "Time"
        value = from_time(dt)
    else:
        raise ValueError(f"Bad date format : {dt}")
    return type, value


def parse(value: Union[datetime, date, time, str]) -> tuple[str, TemporalType, datetime]:
    """Guess the temporal date type from a given argument carrying a temporal information.

    This function is typically used to build a NGSI-LD Temporal Property or temporal metadata such as `observedAt`.

    Parameters
    ----------
    value : Union[datetime, date, time, str]
        A value carrying temporal information, could be either either a datetime, date or time,
        or a string representation of these former types.

    Returns
    -------
    tuple[str, TemporalType, datetime]
        A tuple composed of a ISO8601 string representation of the date and the TemporalType that has been identified

    Raises
    ------
    ValueError
        The date format does not match datetime, date or time or a valid string representation of a date

    See Also
    --------
    ngsildclient.attribute

    Example
    -------
    >>> from ngsildclient import iso8601
    >>> print(iso8601.parse(date(2021,9,13)))
    ('2021-10-13', <TemporalType.DATE: 'Date'>)
    """
    if isinstance(value, datetime):
        return from_datetime(value), TemporalType.DATETIME, value
    if isinstance(value, date):
        return from_date(value), TemporalType.DATE, value
    if isinstance(value, time):
        return from_time(value), TemporalType.TIME, value
    if isinstance(value, str):
        return _from_string(value)
    raise ValueError(f"Bad date format : {value}")


def extract(value: str) -> Optional[datetime]:
    """Extract an ISO8601 datetime string from the input string.

    Parameters
    ----------
    value : str
        the input string

    Returns
    -------
    datetime
        the extracted datetime if found, else None

    Example
    -------
    >>> from ngsildclient.utils import iso8601
    >>> iso8601.extract("urn:ngsi-ld:WeatherObserved:Spain-WeatherObserved-Valladolid-2016-11-30T07:00:00Z")
    datetime.datetime(2016, 11, 30, 7, 0)
    """
    dates = ISO8601_PATTERN.findall(value)
    if len(dates) < 1:
        return None
    try:
        return to_datetime(dates[-1])
    except ValueError:
        return None
