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

from enum import Enum

CORE_CONTEXT = "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"

META_ATTR_CONTEXT = "@context"
META_ATTR_UNITCODE = "unitCode"
META_ATTR_OBSERVED_AT = "observedAt"
META_ATTR_DATASET_ID = "datasetId"


class PredefinedRelationship(Enum):
    HAS_PART = "hasPart"
    HAS_DIRECT_PART = "hasDirectPart"
    IS_CONTAINED_IN = "isContainedIn"


class GeometryMetaAttr(Enum):
    LOCATION = "location"
    OBSERVATION_SPACE = "observationSpace"
    OPERATION_SPACE = "operationSpace"


class AttrType(Enum):
    PROP = "Property"
    TEMPORAL = "Property"  # Temporal Property
    GEO = "GeoProperty"
    REL = "Relationship"


class GeometryType(Enum):
    POINT = "Point"
    LINESTRING = "LineString"
    POLYGON = "Polygon"


class TemporalType(Enum):
    DATETIME = "DateTime"
    DATE = "Date"
    TIME = "Time"
