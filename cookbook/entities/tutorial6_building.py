#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from datetime import time
from geojson import Polygon
from ngsildclient import Entity, PostalAddressBuilder, OpeningHoursBuilder


def build_entity():
    polygon = Polygon([[(100, 0), (101, 0), (101, 1), (100, 1), (100, 0)]])
    e = Entity("Building", "building-a85e3da145c1")
    e.addr(PostalAddressBuilder().locality("London").postalcode("EC4N 8AF").street("25 Walbrook").build())
    e.prop("category", ["office"])
    e.gprop("containedInPlace", polygon)
    e.prop("dataProvider", "OperatorA").prop("description", "Office block")
    e.prop("floorsAboveGround", 7).prop("floorsBelowGround", 0)
    e.loc(polygon)
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
            "cdfd9cb8-ae2b-47cb-a43a-b9767ffd5c84",
            "1be9cd61-ef59-421f-a326-4b6c84411ad4",
        ],
    )
    e.prop("source", "http://www.example.com")
    return e


if __name__ == "__main__":
    entity = build_entity()
    entity.pprint()
