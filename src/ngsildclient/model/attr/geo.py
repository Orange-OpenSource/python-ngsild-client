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

from typing import Tuple
import geojson
from geojson import Point, LineString, Polygon, MultiPoint
from geojson.geometry import Geometry

from ngsildclient.model.utils import process_observedat
from ...utils.urn import Urn
from ..constants import *
from ..exceptions import *

import ngsildclient.model.ngsidict as ngsidict


class AttrGeoValue(ngsidict.NgsiDict):
    @property
    def value(self):
        if self["type"] != "GeoProperty":
            raise ValueError("Attribute type MUST be GeoProperty")
        return geojson.loads(str(self["value"]))

    @value.setter
    def value(self, v: Union[Tuple, Geometry]):
        if self["type"] != "GeoProperty":
            raise ValueError("Attribute type MUST be GeoProperty")
        if isinstance(v, Tuple) and len(v) == 2:
            lat, lon = v
            v = Point((lon, lat))
        self["value"] = v

    @property
    def type(self):
        return "GeoProperty"

    @classmethod
    def build(
        cls,
        attrV: AttrValue,
    ) -> AttrGeoValue:
        property: AttrGeoValue = cls()
        value = attrV.value
        if isinstance(value, (Point, LineString, Polygon, MultiPoint)):
            geometry = value
        else:
            raise NgsiUnmatchedAttributeTypeError(f"Cannot map {type(value)} to NGSI type. {value=}")
        property["type"] = AttrType.GEO.value
        property["value"] = geometry
        if attrV.observedat is not None:
            property[META_ATTR_OBSERVED_AT] = process_observedat(attrV.observedat)
        if attrV.datasetid is not None:
            property[META_ATTR_DATASET_ID] = Urn.prefix(attrV.datasetid)
        return property
