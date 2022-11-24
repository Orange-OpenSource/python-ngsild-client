#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import pkg_resources
import json
from pytest import fixture

from datetime import datetime
from dateutil.tz import UTC
from ngsildclient.model.entity import Entity, mkprop, mkgprop, mktprop, mkrel
from ngsildclient.model.constants import MultAttrValue
from ngsildclient.model.helper.postal import PostalAddressBuilder


def expected_dict(basename: str) -> dict:
    filename: str = pkg_resources.resource_filename(__name__, f"data/{basename}.json")
    with open(filename, "r") as fp:
        expected = json.load(fp)
    return expected


@fixture(scope="class")
def expected_air_quality():
    return expected_dict("air_quality")


def test_loc_1_tuple():
    e = Entity("Barn", "Barn001")
    e.loc((1, 2))
    assert e.to_dict() == {
        "@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"],
        "id": "urn:ngsi-ld:Barn:Barn001",
        "type": "Barn",
        "location": {"type": "GeoProperty", "value": {"coordinates": [2, 1], "type": "Point"}},
    }


def test_loc_2_float():
    e = Entity("Barn", "Barn001")
    e.loc(3, 4)
    assert e.to_dict() == {
        "@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"],
        "id": "urn:ngsi-ld:Barn:Barn001",
        "type": "Barn",
        "location": {"type": "GeoProperty", "value": {"coordinates": [4, 3], "type": "Point"}},
    }


def test_loc_high_precision():
    e = Entity("OffStreetParking", "porto-ParkingLot-23889")
    e.loc(41.150691773, -8.60961198807, precision=11)  # default precision is 6 (geojson default)
    assert e.to_dict() == {
        "id": "urn:ngsi-ld:OffStreetParking:porto-ParkingLot-23889",
        "type": "OffStreetParking",
        "@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"],
        "location": {"type": "GeoProperty", "value": {"coordinates": [-8.60961198807, 41.150691773], "type": "Point"}},
    }


def test_constructor_type_and_id_fully_qualified():
    e = Entity("AirQualityObserved", "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert e.type == "AirQualityObserved"
    assert e.id == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"


def test_constructor_type_and_id_without_scheme():
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    assert e.type == "AirQualityObserved"
    assert e.id == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"


def test_constructor_type_and_id_without_type_included():
    e = Entity("AirQualityObserved", "RZ:Obsv4567")
    assert e.type == "AirQualityObserved"
    assert e.id == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"


def test_constructor_type_and_id_with_type_included():
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    assert e.type == "AirQualityObserved"
    assert e.id == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"


def test_constructor_id_only():
    e = Entity("AirQualityObserved:RZ:Obsv4567")
    assert e.type == "AirQualityObserved"  # infered from id
    assert e.id == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"


def test_simple_prop():
    e = Entity("Barn", "Barn001")
    e.prop("fillingLevel", 0.6).prop("accuracy", 0.9, nested=True)
    assert e.to_dict() == {
        "@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"],
        "id": "urn:ngsi-ld:Barn:Barn001",
        "type": "Barn",
        "fillingLevel": {"type": "Property", "value": 0.6, "accuracy": {"type": "Property", "value": 0.9}},
    }


def test_mkprop():
    p = mkprop("CO2", 33, unitcode="GP")
    assert p == {"CO2": {"type": "Property", "value": 33, "unitCode": "GP"}}


def test_mktprop():
    p = mktprop("dateObserved", "2018-08-07T12:00:00Z")
    assert p == {"dateObserved": {"type": "Property", "value": {"@type": "DateTime", "@value": "2018-08-07T12:00:00Z"}}}


def test_mkgprop():
    p = mkgprop("location", (1.0, 2.0))
    assert p == {"location": {"type": "GeoProperty", "value": {"coordinates": [2.0, 1.0], "type": "Point"}}}


def test_mkrel():
    p = mkrel("hasObject", "Object:Object1")
    assert p == {"hasObject": {"type": "Relationship", "object": "urn:ngsi-ld:Object:Object1"}}


def test_air_quality(expected_air_quality):
    e = Entity("AirQualityObserved", "RZ:Obsv4567")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12, tzinfo=UTC))
    e.prop("NO2", 22, unitcode="GP")
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert e.to_dict() == expected_air_quality


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
    e = Entity.from_dict(payload)
    assert e.to_dict() == expected_air_quality


def test_air_quality_from_json_file(expected_air_quality):
    filename = pkg_resources.resource_filename(__name__, "data/air_quality.json")
    e = Entity.load(filename)
    assert e.to_dict() == expected_air_quality


def test_air_quality_with_userdata():
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12, tzinfo=UTC))
    e.prop("NO2", 22, unitcode="GP", userdata={"reliability": 0.95})
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert e.to_dict() == expected_dict("air_quality_with_userdata")


def test_air_quality_with_nested_prop_1_lvl():
    """Build a sample AirQualityObserved Entity

    .. _NGSI-LD FAQ: Example of a NGSI-LD Payload
    https://fiware.github.io/data-models/specs/ngsi-ld_faq.html

    """
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12, tzinfo=UTC))
    e.prop("NO2", 22, unitcode="GP").prop("accuracy", 0.95, nested=True)
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert e.to_dict() == expected_dict("air_quality_with_nested_prop_1_lvl")


def test_air_quality_with_nested_prop_2_lvl():
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12, tzinfo=UTC))
    e.prop("NO2", 22, unitcode="GP").prop("qc", "checked", nested=True).prop("status", "discarded", nested=True)
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert e.to_dict() == expected_dict("air_quality_with_nested_prop_2_lvl")


def test_air_quality_with_nested_prop_3_lvl():
    e = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12, tzinfo=UTC))
    e.prop("NO2", 22, unitcode="GP").prop("qc", "checked", nested=True).prop("status", "passed", nested=True).prop(
        "reliability", 0.95, nested=True
    )
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert e.to_dict() == expected_dict("air_quality_with_nested_prop_3_lvl")


def test_poi():
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
        "001",
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
        observedat=datetime(2017, 7, 29, 12, 0, 4, tzinfo=UTC),
    ).rel("providedBy", "Person:Bob", nested=True)
    assert e.to_dict() == expected_dict("vehicle")


def test_vehicle_multiple_attribute():
    """Build a sample Vehicle Entity

    .. _NGSI-LD Specification
    Context Information Management (CIM) ; NGSI-LD API []ETSI GS CIM 009 V1.1.1 (2019-01)]

    """
    e = Entity("Vehicle", "A4567")
    m = MultAttrValue()
    m.add(55.0, datasetid="Property:speedometerA4567-speed", userdata=mkprop("source", "Speedometer"))
    m.add(54.5, datasetid="Property:gpsBxyz123-speed", userdata=mkprop("source", "GPS"))
    e.prop("speed", m)
    e.ctx = [
        {
            "Vehicle": "http://example.org/Vehicle",
            "speed": "http://example.org/speed",
            "source": "http://example.org/hasSource",
        },
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context-v1.5.jsonld",
    ]
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
    e.prop("availableSpotNumber", 121, observedat=datetime(2017, 7, 29, 12, 5, 2, tzinfo=UTC)).anchor()
    e.prop("reliability", 0.7).rel("providedBy", "Camera:C1").unanchor()
    e.prop("totalSpotNumber", 200)
    e.gprop("location", (41.2, -8.5))
    assert e.to_dict() == expected_dict("parking")


def test_shelf_1_1_relationship():
    ctx = ["https://fiware.github.io/tutorials.Step-by-Step/tutorials-context.jsonld"]
    e = Entity("Shelf", "unit001", ctx=ctx)
    e.loc((52.554699, 13.3986112))
    e.prop("name", "Corner Unit").prop("maxCapacity", 50)
    e.rel("stocks", "Product:001")
    e.prop("numberOfItems", 50)
    e.rel("locatedIn", "Building:store001").anchor().rel("requestedBy", "bob-the-manager").rel(
        "installedBy", "Person:employee001"
    ).prop("statusOfWork", "completed")
    assert e.to_dict() == expected_dict("shelf_1_1_relationship")


def test_shelf_1_1_relationship_alt():
    ctx = ["https://fiware.github.io/tutorials.Step-by-Step/tutorials-context.jsonld"]
    e = Entity("Shelf", "unit001", ctx=ctx)
    e.loc((52.554699, 13.3986112))
    e.prop("name", "Corner Unit").prop("maxCapacity", 50)
    e.rel("stocks", "Product:001")
    e.prop("numberOfItems", 50)
    e.rel("locatedIn", "Building:store001")
    located_in: NgsiDict = e["locatedIn"]
    located_in |= mkrel("requestedBy", "bob-the-manager")
    located_in |= mkrel("installedBy", "Person:employee001")
    located_in |= mkprop("statusOfWork", "completed")
    assert e.to_dict() == expected_dict("shelf_1_1_relationship")


def test_store_1_many_relationship():
    ctx = ["https://fiware.github.io/tutorials.Step-by-Step/tutorials-context.jsonld"]
    e = Entity("Building", "store001", ctx=ctx)
    e.prop("category", ["commercial"])
    addr = (
        PostalAddressBuilder()
        .street("Bornholmer Straße 65")
        .region("Berlin")
        .locality("Prenzlauer Berg")
        .postalcode("10439")
        .build()
    )
    e.prop("address", addr).prop("verified", True, nested=True)
    e.loc((52.5547, 13.3986)).prop("name", "Bösebrücke Einkauf")
    m = MultAttrValue()
    m.add("Shelf001", datasetid="Relationship:1")
    m.add("Shelf002", datasetid="Relationship:2")
    e.rel("furniture", m)
    assert e.to_dict() == expected_dict("store_1_many_relationship")
