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
    return e


if __name__ == "__main__":
    entity = build_entity()
    entity.pprint()
