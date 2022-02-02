#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import logging
import pytest
from pytest_mock.plugin import MockerFixture

from ngsildclient.api.client import Client
from .common import sample_entity

logger = logging.getLogger(__name__)


def test_api_batch_create(mocked_connected, requests_mock):
    requests_mock.post(
        "http://localhost:1026/ngsi-ld/v1/entityOperations/create/",
        request_headers={"Content-Type": "application/ld+json"},
        status_code=201,
        json=[
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
        ],
    )
    client = Client()
    sample2 = sample_entity.copy()
    sample3 = sample_entity.copy()
    sample2.id = "AirQualityObserved:RZ:Obsv4568"
    sample3.id = "AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    success, response = client.batch.create(batch)
    assert success
    assert response == [
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
    ]


def test_api_batch_upsert(mocked_connected, requests_mock):
    requests_mock.post(
        "http://localhost:1026/ngsi-ld/v1/entityOperations/upsert/",
        request_headers={"Content-Type": "application/ld+json"},
        status_code=201,
        json=[
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
        ],
    )
    client = Client()
    sample2 = sample_entity.copy()
    sample3 = sample_entity.copy()
    sample2.id = "AirQualityObserved:RZ:Obsv4568"
    sample3.id = "AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    success, response = client.batch.upsert(batch)
    assert success
    assert response == [
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
    ]


def test_api_batch_update(mocked_connected, requests_mock):
    requests_mock.post(
        "http://localhost:1026/ngsi-ld/v1/entityOperations/update/",
        request_headers={"Content-Type": "application/ld+json"},
        status_code=204,
        json={"success": "all entities have been successfully updated"},
    )
    client = Client()
    sample2 = sample_entity.copy()
    sample3 = sample_entity.copy()
    sample2.id = "AirQualityObserved:RZ:Obsv4568"
    sample3.id = "AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    success, response = client.batch.update(batch)
    assert success
    assert response == {"success": "all entities have been successfully updated"}


def test_api_batch_delete(mocked_connected, requests_mock):
    requests_mock.post(
        "http://localhost:1026/ngsi-ld/v1/entityOperations/delete/",
        request_headers={"Content-Type": "application/ld+json"},
        status_code=204,
        json={"success": "all entities existed and have been successfully deleted"},
    )
    client = Client()
    sample2 = sample_entity.copy()
    sample3 = sample_entity.copy()
    sample2.id = "AirQualityObserved:RZ:Obsv4568"
    sample3.id = "AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    success, response = client.batch.delete(batch)
    assert success
    assert response == {
        "success": "all entities existed and have been successfully deleted"
    }
