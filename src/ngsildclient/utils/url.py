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
This module contains a few helper functions to deal with URLs.
"""

import urllib.parse
import re


URL_PATTERN = re.compile(r"^http[s]{0,1}://")
"""Simple regex pattern that matches on strings starting with URL scheme (`regex.Pattern`).
"""


def escape(value: str) -> str:
    """URLEncode an URL.

    Parameters
    ----------
    value : str
        String representation of the URL

    Returns
    -------
    str
        The encoded URL as a string

    Example
    -------
    >>> from ngsildclient.utils import url
    >>> print(url.escape("https://example.com?query=dummy&limit=5"))
    https%3A//example.com%3Fquery%3Ddummy%26limit%3D5

    See Also
    --------
    ngsildclient.utils.url.unescape
    """
    return urllib.parse.quote(value)


def unescape(value: str) -> str:
    """URLDecode an URL.

    Parameters
    ----------
    value : str
        String representation of the encoded URL

    Returns
    -------
    str
        The encoded URL as a string

    Example
    -------
    >>> from ngsildclient.utils import url
    >>> print(url.escape("https%3A//example.com%3Fquery%3Ddummy%26limit%3D5"))
    https://example.com?query=dummy&limit=5

    See Also
    --------
    ngsildclient.utils.url.escape
    """
    return urllib.parse.unquote(value)


def isurl(value: str) -> bool:
    """Check if the given string represents an URL.

    Just test whether it starts with "http://" or "https://"

    Parameters
    ----------
    value : str
        The given string to be checked

    Returns
    -------
    bool
        True if the string looks like an URL

    Example
    -------
    >>> from ngsildclient.utils import url
    >>> print(url.isurl("https://example.com?query=dummy&limit=5"))
    True
    """
    return URL_PATTERN.match(value) is not None
