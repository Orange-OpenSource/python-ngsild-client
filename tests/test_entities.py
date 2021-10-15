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
import pytest

from orionldclient.api.client import Client
from orionldclient.api.exceptions import (
    NgsiAlreadyExistsError,
    NgsiResourceNotFoundError,
)
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


def test_api_create_error_already_exists(mock_connected, requests_mock):
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


def test_api_retrieve_error_not_found(mock_connected, requests_mock):
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


def test_api_delete_error_not_found(mock_connected, requests_mock):
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
