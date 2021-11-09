#!/usr/bin/env python3

# Software Name: python-orion-client
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

from orionldclient.model.entity import *
from orionldclient.model.helper.postal import PostalAddressBuilder


def expected_dict(basename: str) -> dict:
    filename: str = pkg_resources.resource_filename(
        __name__, f"data/weather/{basename}.json"
    )
    with open(filename, "r") as fp:
        expected = json.load(fp)
    return expected


def test_weatherobserved():
    """
    https://smart-data-models.github.io/dataModel.Weather/WeatherObserved/examples/example-normalized.jsonld
    """
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
    e.prop("address", address)

    e.prop("stationCode", 2422)
    e.prop("dataProvider", "TEF")
    e.prop("windDirection", -45)
    e.prop("relativeHumidity", 1)
    e.prop("streamGauge", 50)
    e.prop("snowHeight", 20)
    e.prop("uvIndexMax", 1.0)

    assert e.to_dict() == expected_dict("weather_observed")
    assert e.to_dict(kv=True) == expected_dict("weather_observed.kv")
