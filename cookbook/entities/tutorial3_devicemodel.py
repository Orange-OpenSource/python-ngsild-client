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
        "DeviceModel",
        "DeviceModel:myDevice-wastecontainer-sensor-345",
        ctx=[
            "https://smartdatamodels.org/context.jsonld",
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        ],
    )
    e.prop("category", ["sensor"])
    e.prop("function", ["sensing"])
    e.prop("modelName", "S4Container 345")
    e.prop("name", "myDevice Sensor for Containers 345")
    e.prop("brandName", "myDevice")
    e.prop("manufacturerName", "myDevice Inc.")
    e.prop("controlledProperty", ["fillingLevel", "temperature"])
    return e


if __name__ == "__main__":
    entity = build_entity()
    entity.pprint()
