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
    assert res == sample_entity

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
        json=sample_entity.to_dict(),
    )
    client = AsyncClient()
    res = await client.entities.get("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert res == sample_entity
