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

import ngsildclient

from ngsildclient.model.utils import process_observedat, iso8601
from ...utils.urn import Urn
from ..constants import *
from ..exceptions import *

class AttrRelValue(ngsildclient.model.ngsidict.NgsiDict):

    @property
    def type(self):
        return "Relationship"

    @property
    def value(self):
        if self["type"] != "Relationship":
            raise ValueError("Attribute type MUST be Relationship")
        return self["object"]

    @value.setter
    def value(self, v: str):
        if self["type"] != "Relationship":
            raise ValueError("Attribute type MUST be Relationship")
        self["object"] = Urn.prefix(v)

    @property
    def observedat(self) -> datetime:
        dt: str = self.get("observedAt")
        if dt:
            return iso8601.to_datetime(dt)
        return

    @observedat.setter
    def observedat(self, dt: datetime):
        self["observedAt"] = iso8601.from_datetime(dt)

    @property
    def datasetid(self) -> str:
        return self.get("datasetId")

    @datasetid.setter
    def datasetid(self, datasetid: str):
        self["datasetId"] = Urn.prefix(datasetid)        

    @classmethod
    def build(
        cls,
        attrV: AttrValue,
    ) -> AttrRelValue:
        property: AttrRelValue = cls()
        value = attrV.value
        if isinstance(value, str):
            value = Urn.prefix(value)
        elif isinstance(value, Sequence):
            value = [Urn.prefix(v) for v in value]
        else:
            raise NgsiUnmatchedAttributeTypeError(f"Cannot map {type(value)} to NGSI type. {value=}")
        property["type"] = AttrType.REL.value  # set type
        property["object"] = value  # set value
        if attrV.observedat is not None:
            property[META_ATTR_OBSERVED_AT] = process_observedat(attrV.observedat)
        if attrV.datasetid is not None:
            property[META_ATTR_DATASET_ID] = Urn.prefix(attrV.datasetid)
        return property
