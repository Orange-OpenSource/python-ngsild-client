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

from ngsildclient.model.utils import process_observedat
from ...utils.urn import Urn
from ..constants import *
from ..exceptions import *

class AttrRel(ngsildclient.model.ngsidict.NgsiDict):

    @property
    def value(self):
        if self["type"] != "Relationship":
            raise ValueError("Attribute type MUST be Relationship")
        return self["object"]

    @value.setter
    def value(self, v: str):
        if self["type"] != "Relationship":
            raise ValueError("Attribute type MUST be Relationship")
        self["object"] = v

    @property
    def type(self):
        return "Relationship"

    @classmethod
    def build(
        cls,
        attrV: AttrValue,
    ) -> AttrRel:
        property: AttrRel = cls()
        value = attrV.value
        if isinstance(value, str):
            v = value
        else:
            raise NgsiUnmatchedAttributeTypeError(f"Cannot map {type(value)} to NGSI type. {value=}")
        property["type"] = AttrType.REL.value  # set type
        property["object"] = Urn.prefix(v)  # set value
        if attrV.observedat is not None:
            property[META_ATTR_OBSERVED_AT] = process_observedat(attrV.observedat)
        if attrV.datasetid is not None:
            property[META_ATTR_DATASET_ID] = Urn.prefix(attrV.datasetid)
        return property
