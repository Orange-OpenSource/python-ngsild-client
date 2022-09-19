#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from ngsildclient import Entity, PostalAddressBuilder


def build_entity():
    e = Entity(
        "WeatherObserved",
        "WeatherObserved:Spain-WeatherObserved-Valladolid-2016-11-30T07:00:00.00Z",
        ctx=[
            "https://smartdatamodels.org/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
    )
    e.tprop("dateObserved", "2016-11-30T07:00:00Z")
    e.prop("illuminance", 1000)
    e.prop("temperature", 3.3)
    e.prop("precipitation", 0)
    e.prop("atmosphericPressure", 938.9)
    e.prop("pressureTendency", 0.5)
    e.rel("refDevice", "Device:device-0A3478")
    e.prop("source", "http://www.aemet.es")
    e.prop("dataProvider", "http://www.smartsantander.eu/")
    e.prop("windSpeed", 2)
    e.gprop("location", (41.640833333, -4.754444444))
    e.prop("stationName", "Valladolid")
    builder = PostalAddressBuilder()
    address = (
        builder.street("C/ La Pereda 14")
        .locality("Santander")
        .region("Cantabria")
        .country("Spain")
        .build()
    )
    e.prop("address", address)
    builder = PostalAddressBuilder()
    address = builder.locality("Valladolid").country("ES").build()
    e.prop("address", address).prop("stationCode", 2422).prop("dataProvider", "TEF")
    e.prop("windDirection", -45).prop("relativeHumidity", 1)
    e.prop("streamGauge", 50).prop("snowHeight", 20).prop("uvIndexMax", 1.0)
    return e


if __name__ == "__main__":
    entity = build_entity()
    entity.pprint()
