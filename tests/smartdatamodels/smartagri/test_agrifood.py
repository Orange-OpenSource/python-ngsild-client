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

from ngsildclient.model.entity import *
from ngsildclient.model.helper.postal import PostalAddressBuilder


def expected_dict(basename: str) -> dict:
    filename: str = pkg_resources.resource_filename(
        __name__, f"data/agrifood/{basename}.json"
    )
    with open(filename, "r") as fp:
        expected = json.load(fp)
    return expected


def test_agricrop():
    """
    https://smart-data-models.github.io/dataModel.Agrifood/AgriCrop/examples/example-normalized.jsonld
    """
    e = Entity(
        "AgriCrop",
        "AgriCrop:df72dc57-1eb9-42a3-88a9-8647ecc954b4",
        ctx=[
            "https://smartdatamodels.org/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
    )
    e.prop("name", "Wheat")
    e.prop("alternateName", "Triticum aestivum")
    e.prop("description", "Spring wheat")
    e.prop("agroVocConcept", "http://aims.fao.org/aos/agrovoc/c_7951")
    e.prop("wateringFrequency", "daily")
    e.prop(
        "harvestingInterval",
        [
            {"dateRange": "-03-21/-04-01", "description": "Best Season"},
            {"dateRange": "-04-02/-04-15", "description": "Season OK"},
        ],
    )
    e.prop(
        "hasAgriFertiliser",
        [
            "urn:ngsi-ld:AgriFertiliser:1b0d6cf7-320c-4a2b-b2f1-4575ea850c73",
            "urn:ngsi-ld:AgriFertiliser:380973c8-4d3b-4723-a899-0c0c5cc63e7e",
        ],
    )
    e.prop(
        "hasAgriPest",
        [
            "urn:ngsi-ld:AgriPest:1b0d6cf7-320c-4a2b-b2f1-4575ea850c73",
            "urn:ngsi-ld:AgriPest:380973c8-4d3b-4723-a899-0c0c5cc63e7e",
        ],
    )
    e.prop(
        "hasAgriSoil",
        [
            "urn:ngsi-ld:AgriSoil:00411b56-bd1b-4551-96e0-a6e7fde9c840",
            "urn:ngsi-ld:AgriSoil:e8a8389a-edf5-4345-8d2c-b98ac1ce8e2a",
        ],
    )
    e.prop(
        "plantingFrom",
        [
            {"dateRange": "-09-28/-10-12", "description": "Best Season"},
            {"dateRange": "-10-11/-10-18", "description": "Season OK"},
        ],
    )
    e.prop(
        "relatedSource",
        [
            {
                "application": "urn:ngsi-ld:AgriApp:72d9fb43-53f8-4ec8-a33c-fa931360259a",
                "applicationEntityId": "app:weat",
            }
        ],
    )
    e.prop(
        "seeAlso",
        ["https://example.org/concept/wheat", "https://datamodel.org/example/wheat"],
    )

    assert e.to_dict() == expected_dict("agri_crop")
    assert e.to_dict(kv=True) == expected_dict("agri_crop.kv")


def test_agrisoil():
    """
    https://smart-data-models.github.io/dataModel.Agrifood/AgriSoil/examples/example-normalized.jsonld
    """
    e = Entity(
        "AgriSoil",
        "AgriSoil:00411b56-bd1b-4551-96e0-a6e7fde9c840",
        ctx=[
            "https://smartdatamodels.org/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
    )
    e.prop("name", "Clay")
    e.prop("alternateName", "Heavy soil")
    e.prop(
        "description",
        "Fine grained, poor draining soil. Particle size less than 0.002mm",
    )
    e.prop("agroVocConcept", "http://aims.fao.org/aos/agrovoc/c_7951")
    e.prop(
        "hasAgriProductType",
        [
            "urn:ngsi-ld:AgriProductType:ea54eedf-d5a7-4e44-bddd-50e9935237c0",
            "urn:ngsi-ld:AgriProductType:275b4c08-5e52-4bb7-8523-74ce5d0007de",
        ],
    )
    e.prop(
        "relatedSource",
        [
            {
                "application": "urn:ngsi-ld:AgriApp:72d9fb43-53f8-4ec8-a33c-fa931360259a",
                "applicationEntityId": "app:clay",
            }
        ],
    )
    e.prop(
        "seeAlso",
        ["https://example.org/concept/clay", "https://datamodel.org/example/clay"],
    )

    assert e.to_dict() == expected_dict("agri_soil")
    assert e.to_dict(kv=True) == expected_dict("agri_soil.kv")
