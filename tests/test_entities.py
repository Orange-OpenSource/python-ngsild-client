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
import pytest
from pytest_mock.plugin import MockerFixture

from orionldclient.api.client import Client
from orionldclient.api.entities import Entities
from orionldclient.api.exceptions import (
    NgsiAlreadyExistsError,
    NgsiResourceNotFoundError,
    ProblemDetails,
)
from .common import sample_entity, mocked_connected

logger = logging.getLogger(__name__)


def test_api_create(mocked_connected, requests_mock):
    requests_mock.post(
        "http://localhost:1026/ngsi-ld/v1/entities/",
        request_headers={"Content-Type": "application/ld+json"},
        headers={"Location": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"},
        status_code=201,
    )
    client = Client()
    res = client._entities.create(sample_entity)
    assert res == sample_entity


def test_api_create_error_already_exists(mocked_connected, requests_mock):
    requests_mock.post(
        "http://localhost:1026/ngsi-ld/v1/entities/",
        request_headers={"Content-Type": "application/ld+json"},
        status_code=409,
        json={
            "type": "https://uri.etsi.org/ngsi-ld/errors/AlreadyExists",
            "title": "Entity already exists",
            "detail": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        },
    )
    client = Client()
    with pytest.raises(NgsiAlreadyExistsError) as excinfo:
        client._entities.create(sample_entity)
    logger.info(f"{type(excinfo.value)=}")
    assert (
        excinfo.value.problemdetails.type
        == "https://uri.etsi.org/ngsi-ld/errors/AlreadyExists"
    )
    assert excinfo.value.problemdetails.title == "Entity already exists"
    assert excinfo.value.problemdetails.status == 409
    assert (
        excinfo.value.problemdetails.detail
        == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567"
    )
    assert excinfo.value.problemdetails.instance is None
    assert excinfo.value.problemdetails.extension == {}


def test_api_retrieve(mocked_connected, requests_mock):
    requests_mock.get(
        "http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        request_headers={"Accept": "application/ld+json"},
        status_code=200,
        json=sample_entity.to_dict(),
    )
    client = Client()
    res = client._entities.retrieve("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert res == sample_entity


def test_api_retrieve_error_not_found(mocked_connected, requests_mock):
    requests_mock.get(
        "http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        request_headers={"Accept": "application/ld+json"},
        status_code=404,
        json={
            "type": "https://uri.etsi.org/ngsi-ld/errors/ResourceNotFound",
            "title": "Entity Not Found",
            "detail": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        },
    )
    client = Client()
    with pytest.raises(NgsiResourceNotFoundError) as excinfo:
        client._entities.retrieve("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568")
    assert (
        excinfo.value.problemdetails.type
        == "https://uri.etsi.org/ngsi-ld/errors/ResourceNotFound"
    )
    assert excinfo.value.problemdetails.title == "Entity Not Found"
    assert excinfo.value.problemdetails.status == 404
    assert (
        excinfo.value.problemdetails.detail
        == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568"
    )
    assert excinfo.value.problemdetails.instance is None
    assert excinfo.value.problemdetails.extension == {}


def test_api_exists(mocked_connected, requests_mock):
    requests_mock.get(
        "http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        request_headers={"Accept": "application/ld+json"},
        status_code=200,
        json=sample_entity.to_dict(),
    )
    client = Client()
    res = client._entities.exists("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert res


def test_api_delete(mocked_connected, requests_mock):
    requests_mock.delete(
        "http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
        status_code=200,
    )
    client = Client()
    res = client._entities.delete("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567")
    assert res


def test_api_delete_error_not_found(mocked_connected, requests_mock):
    requests_mock.delete(
        "http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        status_code=404,
        json={
            "type": "https://uri.etsi.org/ngsi-ld/errors/ResourceNotFound",
            "title": "Entity Not Found",
            "detail": "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568",
        },
    )
    client = Client()
    with pytest.raises(NgsiResourceNotFoundError) as excinfo:
        client._entities.delete("urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568")
    assert (
        excinfo.value.problemdetails.type
        == "https://uri.etsi.org/ngsi-ld/errors/ResourceNotFound"
    )
    assert excinfo.value.problemdetails.title == "Entity Not Found"
    assert excinfo.value.problemdetails.status == 404
    assert (
        excinfo.value.problemdetails.detail
        == "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4568"
    )
    assert excinfo.value.problemdetails.instance is None
    assert excinfo.value.problemdetails.extension == {}


def test_api_upsert_existent_entity(mocked_connected, mocker: MockerFixture):
    client = Client()
    pd = ProblemDetails(
        "AlreadyExists",
        "Entity already exists",
        409,
        "urn:ngsi-ld:AirQualityObserved:RZ:Obsv4567",
    )
    mocked_create = mocker.patch.object(
        client._entities,
        "create",
        side_effect=[NgsiAlreadyExistsError(pd), sample_entity],
    )
    mocked_delete = mocker.patch.object(client._entities, "delete", return_value=True)
    res = client._entities.upsert(sample_entity)
    assert mocked_create.call_count == 2
    assert mocked_delete.call_count == 1
    assert res == sample_entity


def test_api_upsert_nonexistent_entity(mocked_connected, mocker: MockerFixture):
    client = Client()
    mocked_create = mocker.patch.object(
        client._entities, "create", return_value=sample_entity
    )
    mocked_delete = mocker.patch.object(client._entities, "delete", return_value=True)
    res = client._entities.upsert(sample_entity)
    assert mocked_create.call_count == 1
    assert mocked_delete.call_count == 0
    assert res == sample_entity


def test_api_update_existent_entity(mocked_connected, mocker: MockerFixture):
    client = Client()
    mocker.patch.object(client._entities, "exists", return_value=True)
    mocker.patch.object(client._entities, "delete", return_value=True)
    mocker.patch.object(client._entities, "create", return_value=sample_entity)
    res = client._entities.update(sample_entity)
    assert res == sample_entity


def test_api_update_nonexistent_entity(mocked_connected, mocker: MockerFixture):
    client = Client()
    mocker.patch.object(client._entities, "exists", return_value=False)
    res = client._entities.update(sample_entity)
    assert res is None
