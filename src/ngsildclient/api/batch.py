#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from __future__ import annotations
from typing import TYPE_CHECKING

import logging

if TYPE_CHECKING:
    from .client import Client

from .constants import *
from .exceptions import NgsiApiError, rfc7807_error_handle
from ..model.entity import Entity


logger = logging.getLogger(__name__)


class BatchOp:
    """A wrapper for the NGSI-LD API batch endpoint."""    

    def __init__(self, client: Client, url: str):
        self._client = client
        self._session = client.session
        self.url = url

    @rfc7807_error_handle
    def create(
        self, entities: List[Entity]) -> tuple[bool, dict]:
        r = self._session.post(
            f"{self.url}/create/", json=[entity._payload for entity in entities]
        )
        self._client.raise_for_status(r)
        if r.status_code == 201:
            success, errors = r.json(), []
        elif r.status_code == 207:
            content = r.json()
            success, errors = content["success"], content["errors"]
        else:
            raise NgsiApiError("Batch Create : Unkown HTTP response code {}", r.status_code)
        return success, errors

    @rfc7807_error_handle
    def upsert(self, entities: List[Entity]) -> tuple[bool, dict]:
        r = self._session.post(
            f"{self.url}/upsert/", json=[entity._payload for entity in entities]
        )
        if r.status_code == 201:
            return True, r.json()
        elif r.status_code == 204:
            return True, {
                "success": "all entities already existed and are successfully updated"
            }
        else:
            return False, r.json()

    @rfc7807_error_handle
    def update(self, entities: List[Entity]) -> tuple[bool, dict]:
        r = self._session.post(
            f"{self.url}/update/", json=[entity._payload for entity in entities]
        )
        if r.status_code == 204:
            return True, {"success": "all entities have been successfully updated"}
        else:
            return False, r.json()

    @rfc7807_error_handle
    def delete(self, entities: List[Entity]) -> tuple[bool, dict]:
        r = self._session.post(
            f"{self.url}/delete/", json=[entity.id for entity in entities]
        )
        if r.status_code == 204:
            return True, {
                "success": "all entities existed and have been successfully deleted"
            }
        else:
            return False, r.json()
