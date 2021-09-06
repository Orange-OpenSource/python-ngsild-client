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


from datetime import datetime, date, time
from geojson import Point, LineString, Polygon
from typing import Any, Union
from collections.abc import Sequence
from enum import Enum
from .exceptions import *
from .constants import *
from ..utils import datetime_to_iso8601, urn_prefix
from .ngsidict import NgsiDict


def build_property(
    value: Any,
    unitcode: str = None,
    observed_at: Union[str, datetime] = None,
    dataset_id: str = None,
    userdata: NgsiDict = NgsiDict(),
) -> NgsiDict:
    property: NgsiDict = NgsiDict()
    property["type"] = AttrType.PROP.value  # set type
    if isinstance(value, (int, float, bool, str, list, dict)):
        v = value
    else:
        raise NgsiUnmatchedAttributeTypeError(
            f"Cannot map {type(value)} to NGSI type. {value=}"
        )
    property["value"] = value  # set value
    if unitcode is not None:
        property[META_ATTR_UNITCODE] = unitcode
    if observed_at is not None:
        if isinstance(observed_at, datetime):
            observed_at = datetime_to_iso8601(observed_at)
        property[META_ATTR_OBSERVED_AT] = observed_at
    if dataset_id is not None:
        property[META_ATTR_DATASET_ID] = dataset_id
    if userdata:
        property |= userdata
    return property


def build_geoproperty(value: Any) -> NgsiDict:
    property: NgsiDict = NgsiDict()
    property["type"] = AttrType.GEO.value  # set type
    if isinstance(value, (Point, LineString, Polygon)):
        geometry = value
    elif (
        isinstance(value, tuple) and len(value) == 2
    ):  # simple way for a location Point
        lat, lon = value
        geometry = Point((lon, lat))
    else:
        raise NgsiUnmatchedAttributeTypeError(
            f"Cannot map {type(value)} to NGSI type. {value=}"
        )
    property["value"] = geometry  # set value
    return property


def build_temporal_property(value: Any) -> NgsiDict:
    # TODO : handle Date and Time
    property: NgsiDict = NgsiDict()
    property["type"] = AttrType.TEMPORAL.value  # set type
    if isinstance(value, datetime):
        v = {
            "@type": TemporalType.DATETIME.value,
            "@value": datetime_to_iso8601(value),
        }
    else:
        raise NgsiUnmatchedAttributeTypeError(
            f"Cannot map {type(value)} to NGSI type. {value=}"
        )
    property["value"] = v  # set value
    return property


def build_relationship(
    value: str,
    observed_at: Union[str, datetime] = None,
    userdata: NgsiDict = NgsiDict(),
) -> NgsiDict:
    property: NgsiDict = NgsiDict()
    property["type"] = AttrType.REL.value  # set type
    v = urn_prefix(DEFAULT_NID) + value
    property["object"] = v  # set value
    if observed_at is not None:
        if isinstance(observed_at, datetime):
            observed_at = datetime_to_iso8601(observed_at)
        property[META_ATTR_OBSERVED_AT] = observed_at
    if userdata:
        property |= userdata
    return property
