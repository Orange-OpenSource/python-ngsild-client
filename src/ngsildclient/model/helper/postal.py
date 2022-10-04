#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class PostalAddress:
    """A PostalAddress as defined here : https://schema.org/PostalAddress.
    """
    country: str = None
    locality: str = None
    region: str = None
    pobox: str = None
    postalcode: str = None
    streetaddress: str = None

    def to_dict(self):
        d = {}
        if self.streetaddress and self.pobox:
            raise ValueError("Provide either a Street Address or a PO Box but not both")
        if self.streetaddress:
            d["streetAddress"] = self.streetaddress
        if self.pobox:
            d["postOfficeBoxNumber"] = self.pobox
        if self.locality:
            d["addressLocality"] = self.locality
        if self.postalcode:
            d["postalCode"] = self.postalcode
        if self.region:
            d["addressRegion"] = self.region
        if self.country:
            d["addressCountry"] = self.country
        if not d:
            raise ValueError("PostalAddress is empty")
        return d


class PostalAddressBuilder:
    """A helper class that allows to easily build a PostalAddress property.

    Example
    -------
    >>> from ngsildclient import *
    >>> builder = PostalAddressBuilder()
    >>> address = builder.street("C/ La Pereda 14")
        .locality("Santander")
        .region("Cantabria")
        .country("Spain")
        .build()
    >>> # Add an address property to the entity you're creating
    >>> busstop = Entity("PublicTransportStop", "santander:busStop:463")
    >>> busstop.prop("adress", address)
    >>> busstop.pprint()
    {
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ],
        "id": "urn:ngsi-ld:PublicTransportStop:santander:busStop:463",
        "type": "PublicTransportStop",
        "adress": {
            "type": "Property",
            "value": {
                "streetAddress": "C/ La Pereda 14",
                "addressLocality": "Santander",
                "addressRegion": "Cantabria",
                "addressCountry": "Spain"
            }
        }
    }
    """
    def __init__(self):
        self._addr: PostalAddress = PostalAddress()

    def country(self, value: str) -> PostalAddressBuilder:
        self._addr.country = value
        return self

    def locality(self, value: str) -> PostalAddressBuilder:
        self._addr.locality = value
        return self

    def region(self, value: str) -> PostalAddressBuilder:
        self._addr.region = value
        return self

    def pobox(self, value: str) -> PostalAddressBuilder:
        self._addr.pobox = value
        return self

    def postalcode(self, value: str) -> PostalAddressBuilder:
        self._addr.postalcode = value
        return self

    def street(self, value: str) -> PostalAddressBuilder:
        self._addr.streetaddress = value
        return self

    def build(self) -> dict:
        return self._addr.to_dict()
