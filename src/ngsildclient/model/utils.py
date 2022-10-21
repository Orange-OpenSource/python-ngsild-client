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

import ngsildclient.model.entity as entity
import ngsildclient.model.ngsidict as ngsidict
from ngsildclient.utils import iso8601
from ngsildclient.model.constants import TemporalType
from ngsildclient.model.exceptions import NgsiDateFormatError

from json import JSONEncoder
from typing import Literal, Tuple
from collections.abc import Mapping
from geojson import Point


class NgsiEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (ngsidict.NgsiDict, entity.Entity)):
            return o.to_dict()
        return str

def guess_ngsild_type(attr: Mapping) -> Literal["Property", "GeoProperty", "TemporalProperty", "Relationship"]:
    if not isinstance(attr, Mapping): # not a NGSI-LD attribute
        raise ValueError("NGSI-LD attribute MUST be a JSON object")
    type = attr.get("type")
    if type is None:
        raise ValueError("NGSI-LD attribute has no type")
    if type == "GeoProperty":
        if attr.get("value"):
            return type
        else:
            raise ValueError("Malformed NGSI-LD GeoProperty")
    if type == "Relationship":
        object: str = attr.get("object")
        if object is not None and object.startswith("urn:ngsi-ld:"):
            return type
        else:
            raise ValueError("Malformed NGSI-LD Relationship")
    if type != "Property":
        raise ValueError("NGSI-LD attribute has unknown type")
    # unfortunately Property and TemporalProperty share the same "Property" JSON-string type
    # we've to look deeper to distinguish between them
    value = attr.get("value")
    if value is None:
        raise ValueError("NGSI-LD property has no value")
    if isinstance(value, Mapping): # should be a TemporalProperty
        inner_type = value.get("@type")
        if inner_type in ("DateTime", "Date", "Time"):
            return "TemporalProperty"
        raise ValueError("Malformed NGSI-LD TemporalProperty")
    return "Property"

def process_observedat(observedat):
    date_str, temporaltype, _ = iso8601.parse(observedat)
    if temporaltype != TemporalType.DATETIME:
        raise NgsiDateFormatError(f"observedAt must be a DateTime : {date_str}")
    return date_str

def tuple_to_point(*coord, **kwargs) -> Point:
    if len(coord) == 1 and isinstance(coord, Tuple):
            return Point(coord[0])
    if len(coord) == 2:
        return Point(coord)
    raise ValueError("lat,lon tuple expected")     