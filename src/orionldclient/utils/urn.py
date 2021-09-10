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

from typing import Union, List

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
    def from_name_fully_qualified(cls, name: str):
        m = URN_PATTERN.match(name)
        if m is None:
            raise UrnError(f"Bad urn format : {name}")
        d = m.groupdict()
        return cls(d["nss"], d["nid"])

    @classmethod
    def from_name(cls, resource: str):
        try:
            cls = Urn.from_name_fully_qualified(resource)
        except UrnError:
            cls = Urn(resource)
        return cls

    @staticmethod
    def is_valid_nid(nid: str) -> str:
        m = NID_PATTERN.match(nid)
        return m is not None

    @staticmethod
    def prefix(nss: Union[str,List], nid: str = DEFAULT_NID) -> Union[str,List]:
        if nss is None:
            return None
        if isinstance(nss, str):
            return Urn(nss, nid).fq
        return [Urn(x, nid).fq for x in nss]

    @staticmethod
    def unprefix(resource: str) -> str:
        return Urn.from_name(resource).nss
