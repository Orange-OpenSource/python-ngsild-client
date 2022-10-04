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
This module contains a few helper functions to deal with UUIDs.
"""

import uuid
from base64 import b64encode


def uuidshortener(uuid: uuid.UUID) -> str:
    """Returns a "short" string representation of the UUID object.

    The string will be 22 characters long, base64-encoded, with padding characters removed.
    The encoding uses the urlsafe alphabet with a slightly difference.
    The dash character (sometimes used as a field separator) is replaced by the tilde character.

    Parameters
    ----------
    uuid : uuid.UUID
        The input UUID object

    Returns
    -------
    str
        Its string representation, 22 characters

    Example
    -------
    >>> from uuid import uuid4
    >>> from ngsildclient.utils.uuid import uuidshortener
    >>> uuid = uuid4()
    >>> print(uuid)
    632dd95d-55bf-4f4e-9dd1-05f02531756f
    >>> shortid: str = uuidshortener(uuid)
    >>> print(shortid)
    Yy3ZXVW_T06d0QXwJTF1bw
    """
    # like in urlsafe_base64encode() but ~ replaces -
    return b64encode(uuid.bytes, altchars=b"~_").decode().rstrip("=")


def shortuuid(random: bool = False) -> str:
    """Returns a unique identifier, 22 characters long.

    May be useful in some cases to create a unique Entity identifier.
    The string will be 22 characters long, base64-encoded, with padding characters removed.
    The encoding uses the urlsafe alphabet with a slightly difference.
    The dash character (sometimes used as a field separator) is replaced by the tilde character.

    Parameters
    ----------
    random : bool, optional
        if set uses UUID1 else UUID4, by default False

    Returns
    -------
    str
        A short unique identifier, 22 characters longs.

    Example
    -------
    >>> from ngsildclient import *
    >>> crop = Entity("AgriCrop", shortuuid())
    >>> crop.pprint()
    {
      "@context": [
          "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
      ],
      "id": "urn:ngsi-ld:AgriCrop:SQiKZZRYRnOYgeojIVz5lA",
      "type": "AgriCrop"
    }
    """
    uid = uuid.uuid1() if random else uuid.uuid4()
    return uuidshortener(uid)
