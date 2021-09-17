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


def expected_dict(basename: str) -> dict:
    filename: str = pkg_resources.resource_filename(
        __name__, f"data/{basename}.json"
    )
    with open(filename, "r") as fp:
        expected = json.load(fp)
    return expected


def test_device():
    """
    https://smart-data-models.github.io/dataModel.Device/Device/examples/example.jsonld
    """

    ctx = ["https://smartdatamodels.org/context.jsonld"]

    e = Entity("Device:device-9845A", "Device", ctx)
    e.prop("category", ["sensor"])
    e.prop("batteryLevel", 0.75)
    e.tprop("dateFirstUsed", "2014-09-11T11:00:00Z")
    e.rel("controlledAsset", "wastecontainer-Osuna-100")
    e.prop("serialNumber", "9845A")
    e.prop("ipAddress", "192.14.56.78")
    e.prop("mcc", "214")
    e.prop("mnc", "07")
    e.prop("rssi", 0.86)
    e.prop("value", "l%3D0.22%3Bt%3D21.2")
    e.rel("refDeviceModel", "DeviceModel:myDevice-wastecontainer-sensor-345")
    e.prop("controlledProperty", ["fillingLevel", "temperature"])
    e.prop("owner", "http://person.org/leon")
    e.prop("deviceState", "ok")
    e.prop("distance", 20, unitcode="MTR")
    e.prop("depth", 3, unitcode="MTR")
    e.prop("direction", "Outlet")

    assert e.to_dict() == expected_dict("device")
    assert e.to_dict(kv=True) == expected_dict("device.kv")
