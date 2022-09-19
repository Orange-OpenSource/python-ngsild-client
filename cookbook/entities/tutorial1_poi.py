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
    poi = Entity("PointOfInterest", "PointOfInterest-A-Concha-123456")
    poi.prop("name", "Playa de a Concha")
    poi.addr(PostalAddressBuilder().country("ES").locality("Vilagarcía de Arousa").build())
    poi.prop("category", [113])
    poi.prop(
        "description",
        "La Playa de A Concha se presenta como una continuacion de la Playa de Compostela, una de las mas frecuentadas de Vilagarcia.",
    )
    poi.loc((42.60214472222222, -8.768460000000001))
    poi.prop("source", "http://www.tourspain.es")
    poi.prop("refSeeAlso", ["urn:ngsi-ld:SeeAlso:Beach-A-Concha-123456"])
    return poi


if __name__ == "__main__":
    entity = build_entity()
    entity.pprint()
