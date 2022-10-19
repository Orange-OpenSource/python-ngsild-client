#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import pytest

from datetime import datetime, date, time, timezone
from geojson import Point

from ngsildclient.model.entity import Entity
from ngsildclient.model.ngsidict import NgsiDict
from ngsildclient.model.constants import AttrValue

def test_type():
    d = {"@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"],
        "id": "urn:ngsi-ld:Barn:Barn001",
        "type": "Barn",
        "fillingLevel": {"type": "Property", "value": 0.6}}
    e = Entity(payload=d)
    prop = e["fillingLevel"]
    assert prop.type == "Property"

def test_prop():
    p = NgsiDict()._build_single(AttrValue(22))
    assert p == {"type": "Property", "value": 22}


def test_prop_string():
    p = NgsiDict()._build_single(AttrValue(r"A<>\"'=;()Z"))
    assert p == {"type": "Property", "value": r"A<>\"'=;()Z"}


def test_prop_string_escaped():
    p = NgsiDict()._build_single(AttrValue(r"A<>\"'=;()Z"), escape=True)
    assert p == {"type": "Property", "value": r"A%3C%3E%5C%22%27%3D%3B%28%29Z"}


def test_prop_with_meta_unitcode():
    attrV = AttrValue(22, unitcode="GP")
    p = NgsiDict()._build_single(attrV)
    assert p == {"type": "Property", "unitCode": "GP", "value": 22}


def test_prop_with_meta_timestamp():
    attrV = AttrValue(22, observedat=datetime(2021, 8, 31, 12, tzinfo=timezone.utc))
    p = NgsiDict()._build_single(attrV)
    assert p == {"observedAt": "2021-08-31T12:00:00Z", "type": "Property", "value": 22}


def test_prop_with_meta_userdata():
    attrV = AttrValue(22, userdata={"accuracy": 0.95})
    p = NgsiDict()._build_single(attrV)
    assert p == {"accuracy": 0.95, "type": "Property", "value": 22}


def test_prop_with_nested_property():
    nd = NgsiDict()
    p = nd._build_single(
        AttrValue(22, unitcode="GP", \
            userdata={"accuracy": nd._build_single(AttrValue(0.95))})
    )
    assert p == {
        "type": "Property",
        "value": 22,
        "unitCode": "GP",
        "accuracy": {"type": "Property", "value": 0.95},
    }


def test_geoprop_point():
    bx = Point((-0.5805, 44.84044))
    p = NgsiDict()._build_geoproperty(bx)
    assert p == {
        "type": "GeoProperty",
        "value": {"coordinates": [-0.5805, 44.84044], "type": "Point"},
    }


def test_geoprop_point_as_tuple():
    p = NgsiDict()._build_geoproperty((44.84044, -0.5805))
    assert p == {
        "type": "GeoProperty",
        "value": {"coordinates": [-0.5805, 44.84044], "type": "Point"},
    }


def test_temporal_prop_datetime():
    p = NgsiDict()._build_temporal_property(datetime(2021, 8, 31, 12, tzinfo=timezone.utc))
    assert p == {
        "type": "Property",
        "value": {"@type": "DateTime", "@value": "2021-08-31T12:00:00Z"},
    }


def test_temporal_prop_datetime_str():
    p = NgsiDict()._build_temporal_property("2021-08-31T12:00:00Z")
    assert p == {
        "type": "Property",
        "value": {"@type": "DateTime", "@value": "2021-08-31T12:00:00Z"},
    }


def test_temporal_prop_date():
    p = NgsiDict()._build_temporal_property(date(2021, 8, 31))
    assert p == {
        "type": "Property",
        "value": {"@type": "Date", "@value": "2021-08-31"},
    }


def test_temporal_prop_date_str():
    p = NgsiDict()._build_temporal_property("2021-08-31")
    assert p == {
        "type": "Property",
        "value": {"@type": "Date", "@value": "2021-08-31"},
    }


def test_temporal_prop_time():
    p = NgsiDict()._build_temporal_property(time(12, 0, 0))
    assert p == {
        "type": "Property",
        "value": {"@type": "Time", "@value": "12:00:00Z"},
    }


def test_temporal_prop_time_str():
    p = NgsiDict()._build_temporal_property("12:00:00Z")
    assert p == {
        "type": "Property",
        "value": {"@type": "Time", "@value": "12:00:00Z"},
    }


def test_temporal_prop_str_bad_format():
    with pytest.raises(ValueError):
        p = NgsiDict()._build_temporal_property("25:00:00Z")
