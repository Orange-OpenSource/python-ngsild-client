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

from typing import Union
from datetime import datetime, date, time
from contextlib import suppress

from orionldclient.model.constants import TemporalType


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

    Examples
    --------
    >>> from datetime import datetime
    >>> from orionldclient import iso8601
    >>> d = datetime(2021, 10, 13, 9, 29)
    >>> print(iso8601.from_datetime(d))
    2021-10-13T09:29:00Z
    """
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def utcnow() -> str:
    """Converts the current UTC datetime to ISO8601-formatted string.

    Returns
    -------
    str
        The current UTC datetime, ISO8601-formatted
    """
    return from_datetime(datetime.utcnow())


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

    Examples
    --------
    >>> from datetime import date
    >>> from orionldclient import iso8601
    >>> d = date(2021, 10, 13)
    >>> print(iso8601.from_date(d))
    2021-10-13
    """
    return value.strftime("%Y-%m-%d")


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

    Examples
    --------
    >>> from datetime import time
    >>> from orionldclient import iso8601
    >>> d = time(9, 29)
    >>> print(iso8601.from_time(d))
    09:29:00Z
    """
    return value.strftime("%H:%M:%SZ")


def _from_string(value: str) -> tuple[str, TemporalType]:
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

    Examples
    --------
    >>> from orionldclient import iso8601
    >>> print(iso8601._from_string("2021-10-13"))
    ('2021-10-13', <TemporalType.DATE: 'Date'>)
    """
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
    """Guess the temporal date type from a given argument carrying a temporal information.

    This function is typically used to build a NGSI-LD Temporal Property or temporal metadata such as `observedAt`.

    Parameters
    ----------
    value : Union[datetime, date, time, str]
        A value carrying temporal information, could be either either a datetime, date or time,
        or a string representation of these former types.

    Returns
    -------
    tuple[str, TemporalType]
        A tuple composed of a ISO8601 string representation of the date and the TemporalType that has been identified

    Raises
    ------
    ValueError
        The date format does not match datetime, date or time or a valid string representation of a date

    See Also
    --------
    orionldclient._attribute

    Examples
    --------
    >>> from orionldclient import iso8601
    >>> print(iso8601.parse(date(2021,9,13)))
    ('2021-10-13', <TemporalType.DATE: 'Date'>)
    """
    if isinstance(value, datetime):
        return from_datetime(value), TemporalType.DATETIME
    if isinstance(value, date):
        return from_date(value), TemporalType.DATE
    if isinstance(value, time):
        return from_time(value), TemporalType.TIME
    if isinstance(value, str):
        return _from_string(value)
    raise ValueError(f"Bad date format : {value}")
