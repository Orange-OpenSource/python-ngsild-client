#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from geojson import MultiPoint
from ngsildclient import Entity, NESTED, Rel


def build_entity():
    device = "Device:device-9845A"
    e = Entity("Pipe", "74azsty-70d4l-4da9-b7d0-3340ef655nnb")
    e.prop("bulkCoeff", 72.4549, unitcode="E91")
    e.prop("description", "Free Text")
    e.prop("diameter", 203, unitcode="MMT")
    e.rel("endsAt", "Reservoir:1863179e-3768-4480-9167-ff21f870dd19")
    e.prop("flow", 20, unitcode="G51").rel(Rel.OBSERVED_BY, device, NESTED)
    e.prop("inititalStatus", "OPEN").prop("length", 52.9, unitcode="MTR")
    e.prop("minorLoss", 72.4549, unitcode="C62")
    e.prop("quality", 0.5, unitcode="F27").rel(Rel.OBSERVED_BY, device, NESTED)
    e.prop("roughness", 72.4549, unitcode="C62")
    e.rel("startsAt", "Junction:63fe7d79-0d4c-4da9-b7d0-3340efa0656a")
    e.prop("status", "OPEN").prop("tag", "DMA1")
    e.prop("velocity", 2, unitcode="MTS").rel(Rel.OBSERVED_BY, device, NESTED)
    e.gprop("vertices", MultiPoint([[(24.40623, 60.17966), (24.50623, 60.27966)]]))
    e.prop("wallCoeff", 72.4549, unitcode="RRC")
    return e


if __name__ == "__main__":
    entity = build_entity()
    entity.pprint()
