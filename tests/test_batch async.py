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

from pytest_httpx import HTTPXMock

from ngsildclient.api.asyn.client import AsyncClient
from .common import sample_entity

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_api_batch_create(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entityOperations/create/",
        match_headers={"Content-Type": "application/ld+json"},
        status_code=201,
        json=[
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
        ],
    )
    client = AsyncClient()
    sample2 = sample_entity.copy()
    sample3 = sample_entity.copy()
    sample2.id = "AirQualityObserved:RZ:Obsv4568"
    sample3.id = "AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    success, response = await client.batch.create(batch)
    assert success
    assert response == [
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
    ]


@pytest.mark.asyncio
async def test_api_batch_upsert(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entityOperations/upsert/",
        match_headers={"Content-Type": "application/ld+json"},
        status_code=201,
        json=[
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
        ],
    )
    client = AsyncClient()
    sample2 = sample_entity.copy()
    sample3 = sample_entity.copy()
    sample2.id = "AirQualityObserved:RZ:Obsv4568"
    sample3.id = "AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    success, response = await client.batch.upsert(batch)
    assert success
    assert response == [
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
    ]


@pytest.mark.asyncio
async def test_api_batch_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entityOperations/update/",
        match_headers={"Content-Type": "application/ld+json"},
        status_code=204,
        json={"success": "all entities have been successfully updated"},
    )
    client = AsyncClient()
    sample2 = sample_entity.copy()
    sample3 = sample_entity.copy()
    sample2.id = "AirQualityObserved:RZ:Obsv4568"
    sample3.id = "AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    success, response = await client.batch.update(batch)
    assert success
    assert response == {"success": "all entities have been successfully updated"}


@pytest.mark.asyncio
async def test_api_batch_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entityOperations/delete/",
        status_code=204,
        json={"success": "all entities existed and have been successfully deleted"},
    )
    client = AsyncClient()
    sample2 = sample_entity.copy()
    sample3 = sample_entity.copy()
    sample2.id = "AirQualityObserved:RZ:Obsv4568"
    sample3.id = "AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    success, response = await client.batch.delete(batch)
    assert success
    assert response == {"success": "all entities existed and have been successfully deleted"}
