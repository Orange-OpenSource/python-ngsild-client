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
import json

from orionldclient.model.entity import *
from orionldclient.model.helper.postal import PostalAddressBuilder


def expected_dict(basename: str) -> dict:
    filename: str = pkg_resources.resource_filename(__name__, f"data/{basename}.json")
    with open(filename, "r") as fp:
        expected = json.load(fp)
    return expected


def test_poi():
    """
    https://smart-data-models.github.io/dataModel.PointOfInterest/PointOfInterest/examples/example-normalized.jsonld
    """
    e = Entity(
        "PointOfInterest",
        "PointOfInterest:PointOfInterest-A-Concha-123456",
        ctx=[
            "https://smartdatamodels.org/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
    )
    e.prop("name", "Playa de a Concha")

    builder = PostalAddressBuilder()
    address = builder.country("ES").locality("Vilagarcía de Arousa").build()
    e.prop("address", address)

    e.prop("category", [113])
    e.prop(
        "description",
        "La Playa de A Concha se presenta como una continuación de la Playa de Compostela, una de las más frecuentadas de Vilagarcía.",
    )
    e.gprop("location", (42.60214472222222, -8.768460000000001))
    e.prop("refSeeAlso", "urn:ngsi-ld:SeeAlso:Beach-A-Concha-123456")
    e.prop("source", "http://www.tourspain.es")

    assert e.to_dict() == expected_dict("poi")
    assert e.to_dict(kv=True) == expected_dict("poi.kv")
