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

from ngsildclient.model.entity import Entity
from ngsildclient.api.asyn.client import AsyncClient
from ngsildclient.api.batch import BatchResult
from .common import sample_entity

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_api_batch_single_create_ok(mocked_connected, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entityOperations/create/",
        headers = {"Content-Type": "application/ld+json"},
        status_code=201,
        json=[
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
        ],
    )
    client = AsyncClient()
    sample2 = sample_entity.dup()
    sample3 = sample_entity.dup()
    sample2.id = "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568"
    sample3.id = "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    r: BatchResult = await client.batch._create(batch)
    assert r.ok
    assert r.n_ok == 3
    assert r.n_err == 0
    assert r.ratio == 1.0

@pytest.mark.asyncio
async def test_api_batch_single_create_nok(mocked_connected, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entityOperations/create/",
        headers = {"Content-Type": "application/ld+json"},
        status_code=207,
        json={"success": [], 
            "errors": [
                {"entityId": "urn:ngsi-ld:RoomObserved:Room1", "error": {"type": "https://uri.etsi.org/ngsi-ld/errors/BadRequestData", "title": "entity already exists", "status": 400}}, 
                {'entityId': 'urn:ngsi-ld:RoomObserved:Room2', 'error': {'type': 'https://uri.etsi.org/ngsi-ld/errors/BadRequestData', 'title': 'entity already exists', 'status': 400}}
            ]
        }
    )
    client = AsyncClient()
    room1 = Entity("RoomObserved", "Room1").prop("temperature", 21.7)
    room2 = Entity("RoomObserved", "Room2").prop("temperature", 22.8)
    batch = [room1, room2]
    r: BatchResult = await client.batch._create(batch)
    assert not r.ok
    assert r.n_ok == 0
    assert r.n_err == 2
    assert r.ratio == 0.0
    assert r.errors == [
        {"entityId": "urn:ngsi-ld:RoomObserved:Room1", "error": {"type": "https://uri.etsi.org/ngsi-ld/errors/BadRequestData", "title": "entity already exists", "status": 400}}, 
        {'entityId': 'urn:ngsi-ld:RoomObserved:Room2', 'error': {'type': 'https://uri.etsi.org/ngsi-ld/errors/BadRequestData', 'title': 'entity already exists', 'status': 400}}
    ]

@pytest.mark.asyncio
async def test_api_batch_create_multi_ok(mocked_connected, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entityOperations/create/",
        headers = {"Content-Type": "application/ld+json"},
        status_code=201,
        json=[
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        ]
    )
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entityOperations/create/",
        headers = {"Content-Type": "application/ld+json"},
        status_code=201,
        json=[
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
        ]
    )
    client = AsyncClient()
    sample2 = sample_entity.dup()
    sample3 = sample_entity.dup()
    sample2.id = "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568"
    sample3.id = "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    r: BatchResult = await client.batch.create(batch, batchsize=2)
    assert r.ok
    assert r.n_ok == 3
    assert r.n_err == 0
    assert r.ratio == 1.0
    assert r.errors == []

@pytest.mark.asyncio
async def test_api_batch_upsert_ok_201(mocked_connected, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entityOperations/upsert/?options=replace",
        headers = {"Content-Type": "application/ld+json"},
        status_code=201,
        json=[
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
        ],
    )
    client = AsyncClient()
    sample2 = sample_entity.dup()
    sample3 = sample_entity.dup()
    sample2.id = "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568"
    sample3.id = "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    r: BatchResult = await client.batch.upsert(batch)
    assert r.ok
    assert r.n_ok == 3
    assert r.n_err == 0
    assert r.ratio == 1.0
    assert r.errors == []
    assert r.success == [
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
    ]

@pytest.mark.asyncio
async def test_api_batch_upsert_ok_204(mocked_connected, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entityOperations/upsert/?options=replace",
        headers = {"Content-Type": "application/ld+json"},
        status_code=204
    )    
    client = AsyncClient()
    sample2 = sample_entity.dup()
    sample3 = sample_entity.dup()
    sample2.id = "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568"
    sample3.id = "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    r: BatchResult = await client.batch.upsert(batch)
    assert r.ok
    assert r.n_ok == 3
    assert r.n_err == 0
    assert r.ratio == 1.0
    assert r.errors == []
    assert r.success == [
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
    ]

@pytest.mark.asyncio
async def test_api_batch_update_ok_204(mocked_connected, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entityOperations/update/",
        headers = {"Content-Type": "application/ld+json"},
        status_code=204,
        json=[
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
        ],
    )
    client = AsyncClient()
    sample2 = sample_entity.dup()
    sample3 = sample_entity.dup()
    sample2.id = "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568"
    sample3.id = "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    r: BatchResult = await client.batch.update(batch)
    assert r.ok
    assert r.n_ok == 3
    assert r.n_err == 0
    assert r.ratio == 1.0
    assert r.errors == []
    assert r.success == [
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
    ]

@pytest.mark.asyncio
async def test_api_batch_delete_ok_204(mocked_connected, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entityOperations/delete/",
        headers = {"Content-Type": "application/ld+json"},
        status_code=204,
        json=[
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
            "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
        ],
    )    
    client = AsyncClient()
    sample2 = sample_entity.dup()
    sample3 = sample_entity.dup()
    sample2.id = "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568"
    sample3.id = "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569"
    batch = [sample_entity, sample2, sample3]
    r: BatchResult = await client.batch.delete(batch)
    assert r.ok
    assert r.n_ok == 3
    assert r.n_err == 0
    assert r.ratio == 1.0
    assert r.errors == []
    assert r.success == [
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4569",
    ]    