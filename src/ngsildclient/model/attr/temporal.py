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

from ..constants import *
from ..exceptions import *

import ngsildclient.model.ngsidict as ngsidict
from ngsildclient.utils import iso8601

class AttrTemporalValue(ngsidict.NgsiDict):

    @property
    def value(self) -> Union[datetime, date, time]:
        if self["type"] != "Property":
            raise ValueError("Attribute type MUST be Property")
        type = self["value"]["@type"]
        value = self["value"]["@value"]
        return iso8601.from_string(type, value)

    @value.setter
    def value(self, v: Union[datetime, date, time]):
        if self["type"] != "Property":
            raise ValueError("Attribute type MUST be Property")
        type, value = iso8601.to_string(v)
        self["value"]["@type"] = type
        self["value"]["@value"] = value

    @property
    def type(self):
        return "TemporalProperty"

    @classmethod
    def build(
        cls,
        attrV: AttrValue,
    ) -> AttrTemporalValue:
        property: AttrTemporalValue = cls()
        value = attrV.value
        date_str, temporaltype, _ = iso8601.parse(value)
        v = {
            "@type": temporaltype.value,
            "@value": date_str,
        }
        property["type"] = AttrType.TEMPORAL.value        
        property["value"] = v  # set value
        return property
