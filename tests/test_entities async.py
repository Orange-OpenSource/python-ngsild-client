#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import pytest
import logging

from pytest_httpx import HTTPXMock
from pytest_mock.plugin import MockerFixture

from ngsildclient.api.asyn.client import AsyncClient
from .common import sample_entity
from ngsildclient.api.exceptions import (
    NgsiAlreadyExistsError,
    NgsiResourceNotFoundError,
    ProblemDetails,
)

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_api_create(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entities/",
        match_headers={"Content-Type": "application/ld+json"},
        headers={"Location": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"},
        status_code=201,
    )
    client = AsyncClient()
    res = await client.entities.create(sample_entity)
    assert res == True


@pytest.mark.asyncio
async def test_api_create_error_already_exists(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:1026/ngsi-ld/v1/entities/",
        match_headers={"Content-Type": "application/ld+json"},
        status_code=409,
        json={
            "type": "https://uri.etsi.org/ngsi-ld/errors/AlreadyExists",
            "title": "Entity already exists",
            "detail": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        },
    )
    client = AsyncClient()
    with pytest.raises(NgsiAlreadyExistsError) as excinfo:
        await client.entities.create(sample_entity)
    logger.info(f"{type(excinfo.value)=}")
    assert excinfo.value.problemdetails.type == "https://uri.etsi.org/ngsi-ld/errors/AlreadyExists"
    assert excinfo.value.problemdetails.title == "Entity already exists"
    assert excinfo.value.problemdetails.status == 409
    assert excinfo.value.problemdetails.detail == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"
    assert excinfo.value.problemdetails.instance is None
    assert excinfo.value.problemdetails.extension == {}


@pytest.mark.asyncio
async def test_api_retrieve(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url="http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        match_headers={"Accept": "application/ld+json"},
        status_code=200,
        text=sample_entity.to_json(),
    )
    client = AsyncClient()
    res = await client.entities.get("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert res == sample_entity


@pytest.mark.asyncio
async def test_api_retrieve_error_not_found(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url="http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        match_headers={"Accept": "application/ld+json"},
        status_code=404,
        json={
            "type": "https://uri.etsi.org/ngsi-ld/errors/ResourceNotFound",
            "title": "Entity Not Found",
            "detail": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        },
    )
    client = AsyncClient()
    with pytest.raises(NgsiResourceNotFoundError) as excinfo:
        await client.entities.get("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568")
    assert excinfo.value.problemdetails.type == "https://uri.etsi.org/ngsi-ld/errors/ResourceNotFound"
    assert excinfo.value.problemdetails.title == "Entity Not Found"
    assert excinfo.value.problemdetails.status == 404
    assert excinfo.value.problemdetails.detail == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568"
    assert excinfo.value.problemdetails.instance is None
    assert excinfo.value.problemdetails.extension == {}


@pytest.mark.asyncio
async def test_api_exists(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url="http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        status_code=200,
        text=sample_entity.to_json(),
    )
    client = AsyncClient()
    res = await client._entities.exists("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert res == True


@pytest.mark.asyncio
async def test_api_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="DELETE",
        url="http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        status_code=200,
    )
    client = AsyncClient()
    res = await client._entities.delete("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert res == True


@pytest.mark.asyncio
async def test_api_delete_error_not_found(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="DELETE",
        url="http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        status_code=404,
        json={
            "type": "https://uri.etsi.org/ngsi-ld/errors/ResourceNotFound",
            "title": "Entity Not Found",
            "detail": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        },
    )
    client = AsyncClient()
    with pytest.raises(NgsiResourceNotFoundError) as excinfo:
        await client._entities.delete("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568")
    assert excinfo.value.problemdetails.type == "https://uri.etsi.org/ngsi-ld/errors/ResourceNotFound"
    assert excinfo.value.problemdetails.title == "Entity Not Found"
    assert excinfo.value.problemdetails.status == 404
    assert excinfo.value.problemdetails.detail == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568"
    assert excinfo.value.problemdetails.instance is None
    assert excinfo.value.problemdetails.extension == {}


@pytest.mark.asyncio
async def test_api_upsert_existent_entity(mocker: MockerFixture):
    client = AsyncClient()
    pd = ProblemDetails(
        "AlreadyExists",
        "Entity already exists",
        409,
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
    )
    mocked_create = mocker.patch.object(
        client._entities,
        "create",
        side_effect=[NgsiAlreadyExistsError(pd), True],
    )
    mocked_delete = mocker.patch.object(client._entities, "delete", return_value=True)
    res = await client._entities.upsert(sample_entity)
    assert mocked_create.call_count == 2
    assert mocked_delete.call_count == 1
    assert res == True


@pytest.mark.asyncio
async def test_api_upsert_nonexistent_entity(mocker: MockerFixture):
    client = AsyncClient()
    mocked_create = mocker.patch.object(client._entities, "create", return_value=True)
    mocked_delete = mocker.patch.object(client._entities, "delete", return_value=True)
    res = await client._entities.upsert(sample_entity)
    assert mocked_create.call_count == 1
    assert mocked_delete.call_count == 0
    assert res == True


@pytest.mark.asyncio
async def test_api_update_existent_entity(mocker: MockerFixture):
    client = AsyncClient()
    mocker.patch.object(client._entities, "exists", return_value=True)
    mocker.patch.object(client._entities, "delete", return_value=True)
    mocker.patch.object(client._entities, "create", return_value=True)
    res = await client._entities.update(sample_entity)
    assert res == True


@pytest.mark.asyncio
async def test_api_update_nonexistent_entity(mocker: MockerFixture):
    client = AsyncClient()
    mocker.patch.object(client._entities, "exists", return_value=False)
    res = await client._entities.update(sample_entity)
    assert res == False
