#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.


from ngsildclient import Entity


def build_entity():
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
    return e


if __name__ == "__main__":
    entity = build_entity()
    entity.pprint()
