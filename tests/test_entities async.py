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
from pytest_httpx import HTTPXMock
from ngsildclient.api.asyn.client import AsyncClient
from .common import sample_entity


@pytest.mark.asyncio
async def test_api_retrieve(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        match_headers={"Accept": "application/ld+json"},
        status_code=200,
        json=sample_entity.to_dict(),
    )
    client = AsyncClient()
    res = await client.entities.get("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert res == sample_entity
