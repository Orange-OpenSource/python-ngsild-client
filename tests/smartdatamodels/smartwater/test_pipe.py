#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import pkg_resources
import json

from geojson import MultiPoint
from ngsildclient.model.entity import Entity
from ngsildclient.model.constants import NESTED, Rel

def expected_dict(basename: str) -> dict:
    filename: str = pkg_resources.resource_filename(
        __name__, f"data/network/{basename}.json"
    )
    with open(filename, "r") as fp:
        expected = json.load(fp)
    return expected


def test_pipe():
    """
    https://smart-data-models.github.io/dataModel.WaterDistributionManagementEPANET/Pipe/examples/example-normalized.jsonld
    """
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

    assert e.to_dict() == expected_dict("pipe")
