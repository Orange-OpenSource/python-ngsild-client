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
This module contains helper functions to URI/URN in the NGSI-LD namespace.

References
----------
.. [2] ETSI, 2021. "NGSI-LD namespace" in Context Information Management (CIM); NGSI-LD API
    ETSI GS CIM 009 V1.4.2, Annex A.3, p.183, 2021-04.
"""

import re
import logging

from typing import overload, Optional, Tuple
from ngsildclient.api.constants import ENDPOINT_ENTITIES

NID_PATTERN = re.compile(r"^[0-9a-zA-Z\-]+$")
"""Regex pattern that matches a valid namespace identifier (`regex.Pattern`).
"""

URN_PATTERN = re.compile(r"^urn:(?P<nid>[0-9a-zA-Z\-]+):(?P<nss>.+)$")
"""Regex pattern that extracts NID and NSS from a full valid urn string(`regex.Pattern`).
"""

ENTITY_TYPE_PATTERN = re.compile(r"^([^:]+):.*")
"""Regex pattern that extracts type from a NGSI-LD NSS following naming convention.(`regex.Pattern`).
"""

logger = logging.getLogger(__name__)


class UrnError(Exception):
    """Exception raised when parsing invalid urn/uri."""

    pass


class Urn:
    """Helper class to handle NGSI-LD urn/uri and allow to work with unprefixed strings."""

    DEFAULT_NID = "ngsi-ld"
    # """Default NGSI-LD namespace value
    # """

    @overload
    def __init__(self, fqn: str) -> None:
        """Construct by providing the fully qualified string.

        Parameters
        ----------
        fqn : str
            the fully qualified name, starting with `urn:`
        """
        ...

    @overload
    def __init__(self, *, nss: str, nid: str = DEFAULT_NID) -> None:
        """Construct by specifying the URN parts.

        Parameters
        ----------
        nss : str
            the namespace specific string
        nid : str, optional
            the namespace identifier, by default DEFAULT_NID
        """
        ...

    def __init__(self, fqn: str = None, *, nss: str = None, nid: str = DEFAULT_NID) -> None:
        self.scheme = "urn"
        if nss and nid:
            self.nss = nss
            self.nid = nid
        elif fqn:
            m = URN_PATTERN.match(fqn)
            if m is None:
                raise UrnError(f"Bad urn format : {fqn}")
            d = m.groupdict()
            self.nss = d["nss"]
            self.nid = d["nid"]
        else:
            raise ValueError("Wrong arguments")

    @property
    def fqn(self) -> str:
        """Returns the fully-qualified name

        Returns
        -------
        str
            the fully qualified name

        Example
        -------
        >>> from ngsildclient.utils.urn import Urn
        >>> urn = Urn(nss="AirQualityObserved:RZ:Obsv4567")
        >>> print(urn.fqn)
        urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567
        """
        return f"{self.scheme}:{self.nid}:{self.nss}"

    def __eq__(self, other) -> bool:
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self.nid == other.nid and self.nss == other.nss

    def __repr__(self) -> str:
        return self.fqn

    def infertype(self) -> Optional[str]:
        """Infer type.

        Work only when following the naming convention `urn:ngsi-ld:<type>:...`

        Returns
        -------
        Optional[str]
            the inferred NGSI LD type if found
        """
        m = ENTITY_TYPE_PATTERN.match(self.nss)
        return m.group(1) if m else None

    @staticmethod
    def is_valid_nid(nid: str) -> bool:
        """Check whether the given nid is a valid one

        Parameters
        ----------
        nid : str
            the nid string to be checked

        Returns
        -------
        bool
            True if if the nid is valid

        Example
        -------
        >>> from ngsildclient.utils.urn import Urn
        >>> print(Urn.is_valid_nid("ngsi-ld"))
        True
        >>> print(Urn.is_valid_nid("ngsi+ld"))
        False
        """
        m = NID_PATTERN.match(nid)
        return m is not None

    @staticmethod
    def is_prefixed(value: str) -> bool:
        """Check whether the given string is prefixed (URN scheme+NID)

        Parameters
        ----------
        value : str
            the string value to be checked

        Returns
        -------
        bool
            True if the string value starts with the NGSI-LD u`urn:ngsi-ld:`

        Example
        -------
        >>> from ngsildclient.utils.urn import Urn
        >>> print(Urn.is_prefixed("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"))
        True
        """
        return value.startswith("urn:ngsi-ld:")

    @staticmethod
    def prefix(value: str) -> str:
        """Prefix a string with URN scheme+NID

        Parameters
        ----------
        value : str
            the string to be prefixed

        Returns
        -------
        str
            the string prefixed (if not already prefixed)

        Example
        -------
        >>> from ngsildclient.utils.urn import Urn
        >>> print(Urn.prefix("AirQualityObserved:RZ:Obsv4567"))
        urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567
        """
        if value is None:
            return None
        return value if Urn.is_prefixed(value) else f"urn:ngsi-ld:{value}"

    @staticmethod
    def shorten(value: str) -> str:
        """Remove the prefix (URN scheme+NID)

        Parameters
        ----------
        value : str
            the string to be unprefixed

        Returns
        -------
        str
            the string without the prefix

        Example
        -------
        >>> from ngsildclient.utils.urn import Urn
        >>> print(Urn.unprefix("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"))
        AirQualityObserved:RZ:Obsv4567
        """
        if value is None:
            return None
        return Urn(value).nss if Urn.is_prefixed(value) else value

    @staticmethod
    def split(value: str) -> Tuple[str, str]:
        """Return 

        Parameters
        ----------
        value : str
            _description_

        Returns
        -------
        Tuple[str, str]
            the type of the entity, and the entity id
        """
        type, shortid = value[12:].split(":", 1)
        return type, f"{type}:{shortid}"
