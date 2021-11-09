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

import logging
from orionldclient.api.client import Client, Vendor
from .common import mocked_connected

logger = logging.getLogger(__name__)


def test_api_is_connected(requests_mock):
    requests_mock.get("http://localhost:1026/ngsi-ld/v1/entities", status_code=200)
    client = Client()
    assert client.is_connected()


def test_api_guess_broker(mocked_connected, requests_mock):
    requests_mock.get(
        "http://localhost:1026/version",
        status_code=200,
        json={"orionld version": "post-v0.8.1"},
    )
    client = Client()
    vendor, version = client.guess_vendor()
    logger.info(f"{vendor=}")
    assert vendor == Vendor.ORIONLD
    assert version == "post-v0.8.1"
