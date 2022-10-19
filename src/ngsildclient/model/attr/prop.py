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

from typing import Any, TYPE_CHECKING

import ngsildclient

from ngsildclient.model.utils import process_observedat
from ...utils.urn import Urn
from ..constants import *
from ..exceptions import *

class AttrProp(ngsildclient.model.ngsidict.NgsiDict):

    @property
    def value(self):
        if self["type"] != "Property":
            raise ValueError("Attribute type MUST be Property")
        return self["value"]

    @value.setter
    def value(self, v: Any):
        if self["type"] != "Property":
            raise ValueError("Attribute type MUST be Property")
        self["value"] = v

    @property
    def type(self):
        return "Property"

    @classmethod
    def build(
        cls,
        attrV: AttrValue,
    ) -> AttrProp:
        property: AttrProp = cls()
        value = attrV.value
        if isinstance(value, (int, float, bool, str, list, dict)):
            v = value
        else:
            raise NgsiUnmatchedAttributeTypeError(f"Cannot map {type(value)} to NGSI type. {value=}")
        property["type"] = AttrType.PROP.value  # set type
        property["value"] = v  # set value
        if attrV.unitcode is not None:
            property[META_ATTR_UNITCODE] = attrV.unitcode
        if attrV.observedat is not None:
            property[META_ATTR_OBSERVED_AT] = process_observedat(attrV.observedat)
        if attrV.datasetid is not None:
            property[META_ATTR_DATASET_ID] = Urn.prefix(attrV.datasetid)
        if attrV.userdata:
            property |= attrV.userdata
        return property
