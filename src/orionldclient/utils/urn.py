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

import re

NID_PATTERN = re.compile(r"^[0-9a-zA-Z\-]+$")
URN_PATTERN = re.compile(r"^urn:(?P<nid>[0-9a-zA-Z\-]+):(?P<nss>.+)$")


class UrnError(Exception):
    pass


class Urn:

    DEFAULT_NID = "ngsi-ld"

    def __init__(self, nss: str, nid: str = DEFAULT_NID):
        self.nss = nss
        self.nid = nid

    @property
    def scheme(self):
        return "urn"

    @property
    def fq(self):
        return f"{self.scheme}:{self.nid}:{self.nss}"

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self.nid == other.nid and self.nss == other.nss

    def __repr__(self):
        return self.fq

    @classmethod
    def from_fully_qualified_string(cls, resource: str):
        m = URN_PATTERN.match(resource)
        if m is None:
            raise UrnError(f"Bad urn format : {resource}")
        d = m.groupdict()
        return cls(d["nss"], d["nid"])

    @classmethod
    def from_string(cls, resource: str):
        try:
            cls = Urn.from_fully_qualified_string(resource)
        except UrnError:
            cls = Urn(resource)
        return cls


    @staticmethod
    def is_valid_nid(nid: str) -> str:
        m = NID_PATTERN.match(nid)
        return m is not None
