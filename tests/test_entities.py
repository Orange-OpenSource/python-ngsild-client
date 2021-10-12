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

import logging

from datetime import datetime
from orionldclient.model.entity import Entity
from orionldclient.core.client import Client
from .common import mock_connected, sample_entity

logger = logging.getLogger(__name__)


def test_api_create(mock_connected, requests_mock):
    requests_mock.post(
        "http://localhost:1026/ngsi-ld/v1/entities/",
        request_headers={"Content-Type": "application/ld+json"},
        headers={"Location": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"},
        status_code=201,
    )
    client = Client()
    res = client._entities.create(sample_entity)
    assert res == sample_entity


def test_api_retrieve(mock_connected, requests_mock):
    requests_mock.get(
        "http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        request_headers={"Accept": "application/ld+json"},
        status_code=200,
        json=sample_entity.to_dict(),
    )
    client = Client()
    res = client._entities.retrieve("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert res == sample_entity


def test_api_exists(mock_connected, requests_mock):
    requests_mock.get(
        "http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        request_headers={"Accept": "application/ld+json"},
        status_code=200,
        json=sample_entity.to_dict(),
    )
    client = Client()
    res = client._entities.exists("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert res


def test_api_delete(mock_connected, requests_mock):
    requests_mock.delete(
        "http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        status_code=200,
    )
    client = Client()
    res = client._entities.delete("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert res
