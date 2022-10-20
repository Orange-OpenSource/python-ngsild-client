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

from geojson import Polygon
from datetime import time
from ngsildclient import Entity, PostalAddressBuilder, OpeningHoursBuilder


def expected_dict(basename: str) -> dict:
    filename: str = pkg_resources.resource_filename(
        __name__, f"data/building/{basename}.json"
    )
    with open(filename, "r") as fp:
        expected = json.load(fp)
    return expected


def test_building():
    """
    https://smart-data-models.github.io/dataModel.Building/Building/examples/example-normalized.jsonld
    """
    polygon = Polygon([[(100, 0), (101, 0), (101, 1), (100, 1), (100, 0)]])
    e = Entity("Building", "building-a85e3da145c1")
    e.addr(
        PostalAddressBuilder()
        .locality("London")
        .postalcode("EC4N 8AF")
        .street("25 Walbrook")
        .build()
    )
    e.prop("category", ["office"])
    e.gprop("containedInPlace", polygon)
    e.prop("dataProvider", "OperatorA").prop("description", "Office block")
    e.prop("floorsAboveGround", 7).prop("floorsBelowGround", 0)
    e.gprop("location", polygon)
    e.prop("mapUrl", "http://www.example.com")
    e.rel("occupier", "Person:9830f692-7677-11e6-838b-4f9fb3dc5a4f")
    e.prop(
        "openingHours",
        OpeningHoursBuilder()
        .monday(time(10), time(19))
        .tuesday(time(10), time(19))
        .saturday(time(10), time(22))
        .sunday(time(10), time(21))
        .build(),
    )
    e.rel(
        "owner",
        [
            "urn:ngsi-ld:cdfd9cb8-ae2b-47cb-a43a-b9767ffd5c84",
            "urn:ngsi-ld:1be9cd61-ef59-421f-a326-4b6c84411ad4",
        ],
    )
    e.prop("source", "http://www.example.com")

    assert e.to_dict() == expected_dict("building")
