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

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class PostalAddress:
    """https://schema.org/PostalAddress"""

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
