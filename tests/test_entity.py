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

import pkg_resources

from datetime import datetime
from orionldclient.model.entity import *
from orionldclient.model.attribute import *


def test_air_quality():
    """Build a sample AirQualityObserved Entity

    .. _NGSI-LD HOWTO:
    http://google.github.io/styleguide/pyguide.html

    """
    e = Entity("AirQualityObserved:RZ:Obsv4567", "AirQualityObserved")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12))
    e.prop("NO2", 22, unitcode="GP")
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert (
        e.to_json() == r'{"id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567", '
        r'"type": "AirQualityObserved", '
        r'"dateObserved": {"type": "Property", "value": {"@type": "DateTime", "@value": "2018-08-07T12:00:00Z"}}, '
        r'"NO2": {"type": "Property", "value": 22, "unitCode": "GP"}, '
        r'"refPointOfInterest": {"type": "Relationship", "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"}, '
        r'"@context": ["https://schema.lab.fiware.org/ld/context", "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]}'
    )


def test_air_quality_from_dict():
    payload = {
        "@context": [
            "https://schema.lab.fiware.org/ld/context",
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
    assert (
        e.to_json() == r'{"id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567", '
        r'"type": "AirQualityObserved", '
        r'"dateObserved": {"type": "Property", "value": {"@type": "DateTime", "@value": "2018-08-07T12:00:00Z"}}, '
        r'"NO2": {"type": "Property", "value": 22, "unitCode": "GP"}, '
        r'"refPointOfInterest": {"type": "Relationship", "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"}, '
        r'"@context": ["https://schema.lab.fiware.org/ld/context", "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]}'
    )

def test_air_quality_from_json_file():
    filename = pkg_resources.resource_filename(__name__, "data/air_quality.json")
    e = Entity.load(filename)
    assert (
        e.to_json() == r'{"id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567", '
        r'"type": "AirQualityObserved", '
        r'"dateObserved": {"type": "Property", "value": {"@type": "DateTime", "@value": "2018-08-07T12:00:00Z"}}, '
        r'"NO2": {"type": "Property", "value": 22, "unitCode": "GP"}, '
        r'"refPointOfInterest": {"type": "Relationship", "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"}, '
        r'"@context": ["https://schema.lab.fiware.org/ld/context", "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]}'
    )

def test_air_quality_with_userdata():
    """Build a sample AirQualityObserved Entity

    .. _NGSI-LD FAQ: Example of a NGSI-LD Payload
    https://fiware.github.io/data-models/specs/ngsi-ld_faq.html

    """
    e = Entity("AirQualityObserved:RZ:Obsv4567", "AirQualityObserved")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12))
    e.prop("NO2", 22, unitcode="GP", userdata={"reliability": 0.95})
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert (
        e.to_json()
        == r'{"id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567", "type": "AirQualityObserved", "dateObserved": {"type": "Property", "value": {"@type": "DateTime", "@value": "2018-08-07T12:00:00Z"}}, "NO2": {"type": "Property", "value": 22, "unitCode": "GP", "reliability": 0.95}, "refPointOfInterest": {"type": "Relationship", "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"}, "@context": ["https://schema.lab.fiware.org/ld/context", "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]}'
    )


def test_air_quality_with_nested_prop_1_lvl():
    """Build a sample AirQualityObserved Entity

    .. _NGSI-LD FAQ: Example of a NGSI-LD Payload
    https://fiware.github.io/data-models/specs/ngsi-ld_faq.html

    """
    e = Entity("AirQualityObserved:RZ:Obsv4567", "AirQualityObserved")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12))
    e.prop("NO2", 22, unitcode="GP").prop("accuracy", 0.95)
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert (
        e.to_json() == r'{"id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567", '
        r'"type": "AirQualityObserved", '
        r'"dateObserved": {"type": "Property", "value": {"@type": "DateTime", "@value": "2018-08-07T12:00:00Z"}}, '
        r'"NO2": {"type": "Property", "value": 22, "unitCode": "GP", "accuracy": {"type": "Property", "value": 0.95}}, '
        r'"refPointOfInterest": {"type": "Relationship", "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"}, '
        r'"@context": ["https://schema.lab.fiware.org/ld/context", "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]}'
    )


def test_air_quality_with_nested_prop_2_lvl():
    """Build a sample AirQualityObserved Entity"""
    e = Entity("AirQualityObserved:RZ:Obsv4567", "AirQualityObserved")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12))
    e.prop("NO2", 22, unitcode="GP").prop("accuracy", 0.95)
    e.prop("NO2", 22, unitcode="GP").prop("qc", "checked").prop("status", "discarded")
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert (
        e.to_json()
        == r'{"id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567", "type": "AirQualityObserved", "dateObserved": {"type": "Property", "value": {"@type": "DateTime", "@value": "2018-08-07T12:00:00Z"}}, "NO2": {"type": "Property", "value": 22, "unitCode": "GP", "qc": {"type": "Property", "value": "checked", "status": {"type": "Property", "value": "discarded"}}}, "refPointOfInterest": {"type": "Relationship", "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"}, "@context": ["https://schema.lab.fiware.org/ld/context", "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]}'
    )


def test_air_quality_with_nested_prop_3_lvl():
    """Build a sample AirQualityObserved Entity"""
    e = Entity("AirQualityObserved:RZ:Obsv4567", "AirQualityObserved")
    e.tprop("dateObserved", datetime(2018, 8, 7, 12))
    e.prop("NO2", 22, unitcode="GP").prop("accuracy", 0.95)
    e.prop("NO2", 22, unitcode="GP").prop("qc", "checked").prop(
        "status", "passed"
    ).prop("reliability", 0.95)
    e.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")
    assert (
        e.to_json()
        == r'{"id": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567", "type": "AirQualityObserved", "dateObserved": {"type": "Property", "value": {"@type": "DateTime", "@value": "2018-08-07T12:00:00Z"}}, "NO2": {"type": "Property", "value": 22, "unitCode": "GP", "qc": {"type": "Property", "value": "checked", "status": {"type": "Property", "value": "passed", "reliability": {"type": "Property", "value": 0.95}}}}, "refPointOfInterest": {"type": "Relationship", "object": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare"}, "@context": ["https://schema.lab.fiware.org/ld/context", "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]}'
    )


def test_poi():
    """Build a sample PointOfInterest Entity

    .. _NGSI-LD HOWTO:
    http://google.github.io/styleguide/pyguide.html

    """
    e = Entity("PointOfInterest:RZ:MainSquare", "PointOfInterest")
    e.prop("category", [113])
    e.prop("description", "Beach of RZ")
    e.gprop("location", (44, -8))
    assert (
        e.to_json() == r'{"id": "urn:ngsi-ld:PointOfInterest:RZ:MainSquare", '
        r'"type": "PointOfInterest", '
        r'"category": {"type": "Property", "value": [113]}, '
        r'"description": {"type": "Property", "value": "Beach of RZ"}, '
        r'"location": {"type": "GeoProperty", "value": {"type": "Point", "coordinates": [-8, 44]}}, '
        r'"@context": ["https://schema.lab.fiware.org/ld/context", "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]}'
    )


def test_store():
    """Build a sample PointOfInterest Entity

    .. _NGSI-LD Primer
    Context Information Management (CIM) ; NGSI-LD Primer [ETSI GR CIM 008 V1.1.1 (2020-03)]

    """
    ctx = (
        ContextBuilder()
        .add(
            {
                "Store": "https://uri.etsi.org/ngsi-ld/primer/Store",
                "address": "https://uri.etsi.org/ngsi-ld/primer/address",
                "storeName": "https://uri.etsi.org/ngsi-ld/primer/storeName",
                "streetAddress": "https://uri.etsi.org/ngsi-ld/primer/streetAddress",
                "addressRegion": "https://uri.etsi.org/ngsi-ld/primer/addressRegion",
                "addressLocality": "https://uri.etsi.org/ngsi-ld/primer/addressLocality",
                "postalCode": "https://uri.etsi.org/ngsi-ld/primer/postalCode",
            }
        )
        .build()
    )
    e = Entity("Store:001", "Store", ctx)
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
    assert (
        e.to_json() == r'{"id": "urn:ngsi-ld:Store:001", ' r'"type": "Store", ',
        r'"address": {"type": "Property", "value": {"streetAddress": "Main Street 65", "addressRegion": "Metropolis", "addressLocality": "Duckburg", "postalCode": "42000"}}, '
        r'"location": {"type": "GeoProperty", "value": {"type": "Point", "coordinates": [57.487412, -20.284561]}}, '
        r'"storeName": {"type": "Property", "value": "Checker Market"}, '
        r'"@context": ["https://schema.lab.fiware.org/ld/context", "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld", '
        r'{"Store": "https://uri.etsi.org/ngsi-ld/primer/Store", "address": "https://uri.etsi.org/ngsi-ld/primer/address", '
        r'"storeName": "https://uri.etsi.org/ngsi-ld/primer/storeName", "streetAddress": "https://uri.etsi.org/ngsi-ld/primer/streetAddress", '
        r'"addressRegion": "https://uri.etsi.org/ngsi-ld/primer/addressRegion", '
        r'"addressLocality": "https://uri.etsi.org/ngsi-ld/primer/addressLocality",'
        r'"postalCode": "https://uri.etsi.org/ngsi-ld/primer/postalCode"}]}',
    )


def test_vehicle():
    """Build a sample Vehicle Entity

    .. _NGSI-LD Specification
    Context Information Management (CIM) ; NGSI-LD API []ETSI GS CIM 009 V1.1.1 (2019-01)]

    """

    ctx = (
        ContextBuilder()
        .add(
            [
                "http://example.org/ngsi-ld/commonTerms.jsonld",
                "http://example.org/ngsi-ld/vehicle.jsonld",
                "http://example.org/ngsi-ld/parking.jsonld",
            ]
        )
        .build()
    )

    e = Entity("Vehicle:A4567", "Vehicle", ctx)
    e.prop("brandName", "Mercedes")
    e.rel(
        "isParked",
        "OffStreetParking:Downtown1",
        observed_at=datetime(2017, 7, 29, 12, 0, 4),
    ).rel("providedBy", "Person:Bob")
    assert (
        e.to_json()
        == r'{"id": "urn:ngsi-ld:Vehicle:A4567", "type": "Vehicle", "brandName": {"type": "Property", "value": "Mercedes"}, "isParked": {"type": "Relationship", "object": "urn:ngsi-ld:OffStreetParking:Downtown1", "observedAt": "2017-07-29T12:00:04Z", "providedBy": {"type": "Relationship", "object": "urn:ngsi-ld:Person:Bob"}}, "@context": ["https://schema.lab.fiware.org/ld/context", "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld", {"Store": "https://uri.etsi.org/ngsi-ld/primer/Store", "address": "https://uri.etsi.org/ngsi-ld/primer/address", "storeName": "https://uri.etsi.org/ngsi-ld/primer/storeName", "streetAddress": "https://uri.etsi.org/ngsi-ld/primer/streetAddress", "addressRegion": "https://uri.etsi.org/ngsi-ld/primer/addressRegion", "addressLocality": "https://uri.etsi.org/ngsi-ld/primer/addressLocality", "postalCode": "https://uri.etsi.org/ngsi-ld/primer/postalCode"}, ["http://example.org/ngsi-ld/commonTerms.jsonld", "http://example.org/ngsi-ld/vehicle.jsonld", "http://example.org/ngsi-ld/parking.jsonld"]]}'
    )
