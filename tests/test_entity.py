#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.
# SPDX-License-Identifier: Apache-2.0

import pkg_resources
import json
from pytest import fixture

from datetime import datetime
from ngsildclient.model.entity import *


def expected_dict(basename: str) -> dict:
    filename: str = pkg_resources.resource_filename(__name__, f"data/{basename}.json")
    with open(filename, "r") as fp:
        expected = json.load(fp)
    return expected


@fixture(scope="class")
def expected_air_quality():
    return expected_dict("air_quality")


def test_constructor_type_and_id_fully_qualified():
    e = Entity("AirQualityObserved", "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert e.type == "AirQualityObserved"
    assert e.id == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"


def test_constructor_type_and_id_without_scheme():
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    assert e.type == "AirQualityObserved"
    assert e.id == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"


def test_constructor_autoprefix_type_and_id_without_type_included():
    e = Entity("AirQualityObserved", "RZ:Obsv4567", autoprefix=True)
    assert e.type == "AirQualityObserved"
    assert e.id == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"


def test_constructor_autoprefix_type_and_id_with_type_included():
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567", autoprefix=True)
    assert e.type == "AirQualityObserved"
    assert e.id == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"


def test_constructor_id_only():
    e = Entity("AirQualityObserved:RZ:Obsv4567")
    assert e.type == "AirQualityObserved"  # infered from id
    assert e.id == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"


def test_air_quality(expected_air_quality):
    """Build a sample AirQualityObserved Entity

    .. _NGSI-LD HOWTO:
    http://google.github.io/styleguide/pyguide.html

    """
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12))
    e.prop("NO2", 22, unitcode="GP")
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert e.to_dict() == expected_air_quality
    assert e.to_dict(kv=True) == expected_dict("air_quality.kv")


def test_air_quality_from_dict(expected_air_quality):
    payload = {
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
        "id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        "type": "AirQualityObserved",
        "dateObserved": {
            "type": "Property",
            "value": {"@type": "DateTime", "@value": "2018-08-07T12:00:00Z"},
        },
        "NO2": {"type": "Property", "value": 22, "unitCode": "GP"},
        "refPointOfInterest": {
            "type": "Relationship",
            "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare",
        },
    }
    e = Entity.from_dict(payload=payload)
    assert e.to_dict() == expected_air_quality


def test_air_quality_from_json_file(expected_air_quality):
    filename = pkg_resources.resource_filename(__name__, "data/air_quality.json")
    e = Entity.load(filename)
    assert e.to_dict() == expected_air_quality


def test_air_quality_with_userdata():
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12))
    e.prop("NO2", 22, unitcode="GP", userdata={"reliability": 0.95})
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert e.to_dict() == expected_dict("air_quality_with_userdata")


def test_air_quality_with_nested_prop_1_lvl():
    """Build a sample AirQualityObserved Entity

    .. _NGSI-LD FAQ: Example of a NGSI-LD Payload
    https://fiware.github.io/data-models/specs/ngsi-ld_faq.html

    """
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12))
    e.prop("NO2", 22, unitcode="GP").prop("accuracy", 0.95, NESTED)
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert e.to_dict() == expected_dict("air_quality_with_nested_prop_1_lvl")


def test_air_quality_with_nested_prop_2_lvl():
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12))
    e.prop("NO2", 22, unitcode="GP").prop("qc", "checked", NESTED).prop(
        "status", "discarded", nested=True
    )
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert e.to_dict() == expected_dict("air_quality_with_nested_prop_2_lvl")


def test_air_quality_with_nested_prop_3_lvl():
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12))
    e.prop("NO2", 22, unitcode="GP").prop("qc", "checked", NESTED).prop(
        "status", "passed", NESTED
    ).prop("reliability", 0.95, NESTED)
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert e.to_dict() == expected_dict("air_quality_with_nested_prop_3_lvl")


def test_poi():
    """Build a sample PointOfInterest Entity

    .. _NGSI-LD HOWTO:
    http://google.github.io/styleguide/pyguide.html

    """
    e = Entity("PointOfInterest", "PointOfInterest:RZ:MainSquare")
    e.prop("category", [113])
    e.prop("description", "Beach of RZ")
    e.gprop("location", (44, -8))
    assert e.to_dict() == expected_dict("poi")


def test_store():
    """Build a sample PointOfInterest Entity

    .. _NGSI-LD Primer
    Context Information Management (CIM) ; NGSI-LD Primer [ETSI GR CIM 008 V1.1.1 (2020-03)]

    """
    e = Entity(
        "Store",
        "Store:001",
        ctx=[
            {
                "Store": "https://uri.etsi.org/ngsi-ld/primer/Store",
                "address": "https://uri.etsi.org/ngsi-ld/primer/address",
                "storeName": "https://uri.etsi.org/ngsi-ld/primer/storeName",
                "streetAddress": "https://uri.etsi.org/ngsi-ld/primer/streetAddress",
                "addressRegion": "https://uri.etsi.org/ngsi-ld/primer/addressRegion",
                "addressLocality": "https://uri.etsi.org/ngsi-ld/primer/addressLocality",
                "postalCode": "https://uri.etsi.org/ngsi-ld/primer/postalCode",
            },
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
    )
    e.prop(
        "address",
        {
            "streetAddress": "Main Street 65",
            "addressRegion": "Metropolis",
            "addressLocality": "Duckburg",
            "postalCode": "42000",
        },
    )
    e.gprop("location", (-20.2845607, 57.4874121))
    e.prop("storeName", "Checker Market")
    assert e.to_dict() == expected_dict("store")
    assert e.to_dict(kv=True) == expected_dict("store.kv")


def test_vehicle():
    """Build a sample Vehicle Entity

    .. _NGSI-LD Specification
    Context Information Management (CIM) ; NGSI-LD API []ETSI GS CIM 009 V1.1.1 (2019-01)]

    """
    e = Entity(
        "Vehicle",
        "Vehicle:A4567",
        ctx=[
            "http://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "http://example.org/ngsi-ld/commonTerms.jsonld",
            "http://example.org/ngsi-ld/vehicle.jsonld",
            "http://example.org/ngsi-ld/parking.jsonld",
        ],
    )
    e.prop("brandName", "Mercedes")
    e.rel(
        "isParked",
        "OffStreetParking:Downtown1",
        observedat=datetime(2017, 7, 29, 12, 0, 4),
    ).rel("providedBy", "Person:Bob", NESTED)
    assert e.to_dict() == expected_dict("vehicle")
    assert json.loads(e.to_json(kv=True)) == expected_dict("vehicle.kv")


def test_vehicle_multiple_attribute():
    """Build a sample Vehicle Entity

    .. _NGSI-LD Specification
    Context Information Management (CIM) ; NGSI-LD API []ETSI GS CIM 009 V1.1.1 (2019-01)]

    """
    e = Entity(
        "Vehicle",
        "Vehicle:A4567",
        ctx=[
            "http://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            {
                "speed#1": "http://example.org/speed",
                "speed#2": "http://example.org/speed",
                "source": "http://example.org/hasSource",
            },
        ],
    )
    e.prop("#speed1", 55, datasetid="Property:speedometerA4567-speed").prop(
        "source", "Speedometer", NESTED
    )
    e.prop("#speed2", 54.5, datasetid="Property:gpsBxyz123-speed").prop(
        "source", "GPS", NESTED
    )
    assert e.to_dict() == expected_dict("vehicle_multiple_attribute")


def test_parking():
    """Build a sample Parking Entity

    .. _NGSI-LD Specification
    Context Information Management (CIM) ; NGSI-LD API []ETSI GS CIM 009 V1.1.1 (2019-01)]

    """
    e = Entity(
        "OffStreetParking",
        "OffStreetParking:Downtown1",
        ctx=[
            "http://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
            "http://example.org/ngsi-ld/parking.jsonld",
        ],
    )
    e.prop(
        "availableSpotNumber", 121, observedat=datetime(2017, 7, 29, 12, 5, 2)
    ).anchor()
    e.prop("reliability", 0.7).rel("providedBy", "Camera:C1").unanchor()
    e.prop("totalSpotNumber", 200)
    e.gprop("location", (41.2, -8.5))
    assert e.to_dict() == expected_dict("parking")
    assert e.to_dict(kv=True) == expected_dict("parking.kv")


def test_cached_datetime_in_observedat():
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12))  # cache the datetime
    e.prop(
        "NO2", 22, unitcode="GP", observedat=Auto
    )  # reuse the datetime set by the previous tprop() call
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert e["NO2.observedAt"] == "2018-08-07T12:00:00Z"


def test_cached_datetime_in_prop():
    e = Entity(
        "AirQualityObserved", "AirQualityObserved:RZ:2018-08-07T12:00:00Z"
    )  # cache the datetime
    e.obs()  # dateObserved that uses the cached datetime (the one extracted from the entity identifier)
    assert e["dateObserved.value.@value"] == "2018-08-07T12:00:00Z"
