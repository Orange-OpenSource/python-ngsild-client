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

from datetime import datetime
from orionldclient.model._attribute import *


def test_prop():
    p = build_property(22)
    assert p == {"type": "Property", "value": 22}


def test_prop_with_meta_unitcode():
    p = build_property(22, unitcode="GP")
    assert p == {"type": "Property", "unitCode": "GP", "value": 22}


def test_prop_with_meta_timestamp():
    p = build_property(22, observedat=datetime(2021, 8, 31, 12))
    assert p == {"observedAt": "2021-08-31T12:00:00Z", "type": "Property", "value": 22}


def test_prop_with_meta_userdata():
    p = build_property(22, userdata={"accuracy": 0.95})
    assert p == {"accuracy": 0.95, "type": "Property", "value": 22}


def test_prop_with_nested_property():
    p = build_property(22, unitcode="GP", userdata={"accuracy": build_property(0.95)})
    assert p == {
        "type": "Property",
        "value": 22,
        "unitCode": "GP",
        "accuracy": {"type": "Property", "value": 0.95},
    }


def test_geoprop_point():
    bx = Point((-0.5805, 44.84044))
    p = build_geoproperty(bx)
    assert p == {
        "type": "GeoProperty",
        "value": {"coordinates": [-0.5805, 44.84044], "type": "Point"},
    }


def test_geoprop_point_as_tuple():
    p = build_geoproperty((44.84044, -0.5805))
    assert p == {
        "type": "GeoProperty",
        "value": {"coordinates": [-0.5805, 44.84044], "type": "Point"},
    }


def test_temporal_prop():
    p = build_temporal_property(datetime(2021, 8, 31, 12))
    assert p == {
        "type": "Property",
        "value": {"@type": "DateTime", "@value": "2021-08-31T12:00:00Z"},
    }
