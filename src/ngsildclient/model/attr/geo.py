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

import geojson
from geojson import Point, LineString, Polygon, MultiPoint
from geojson.geometry import Geometry

from ngsildclient.model.utils import process_observedat
from ...utils.urn import Urn
from ..constants import *
from ..exceptions import *

import ngsildclient.model.ngsidict as ngsidict

class AttrGeo(ngsidict.NgsiDict):

    @property
    def value(self):
        if self["type"] != "GeoProperty":
            raise ValueError("Attribute type MUST be GeoProperty")
        return geojson.loads(str(self["value"]))

    @value.setter
    def value(self, v: Geometry):
        if self["type"] != "GeoProperty":
            raise ValueError("Attribute type MUST be GeoProperty")
        self["value"] = v

    @property
    def type(self):
        return "GeoProperty"

    @classmethod
    def build(
        cls,
        attrV: AttrValue,
    ) -> AttrGeo:
        property: AttrGeo = cls()
        value = attrV.value
        if isinstance(value, (Point, LineString, Polygon, MultiPoint)):
            geometry = value
        elif isinstance(value, tuple) and len(value) == 2:  # simple way for a location Point
            lat, lon = value
            geometry = Point((lon, lat))
        else:
            raise NgsiUnmatchedAttributeTypeError(f"Cannot map {type(value)} to NGSI type. {value=}")
        property["type"] = AttrType.GEO.value
        property["value"] = geometry
        if attrV.observedat is not None:
            property[META_ATTR_OBSERVED_AT] = process_observedat(attrV.observedat)
        if attrV.datasetid is not None:
            property[META_ATTR_DATASET_ID] = Urn.prefix(attrV.datasetid)
        return property
