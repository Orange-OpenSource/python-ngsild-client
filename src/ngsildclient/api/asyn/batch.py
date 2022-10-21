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
from typing import TYPE_CHECKING, Sequence, Literal

import logging
import json

if TYPE_CHECKING:
    from .client import AsyncClient, EntityOrId

from ..constants import BATCHSIZE
from ..exceptions import NgsiApiError, rfc7807_error_handle_async
from ..batch import BatchResult
from ...model.entity import Entity
from ngsildclient.model.utils import NgsiEncoder

logger = logging.getLogger(__name__)

class Batch:
    """A wrapper for the NGSI-LD API batch endpoint."""    

    def __init__(self, client: AsyncClient, url: str):
        self._client = client
        self._session = client.client
        self.url = url

    @rfc7807_error_handle_async
    async def _create(
        self, entities: Sequence[Entity]) -> BatchResult:
        r = await self._session.post(
            f"{self.url}/create/", 
            content=json.dumps([e for e in entities], cls=NgsiEncoder)
        )
        self._client.raise_for_status(r)
        if r.status_code == 201:
            success, errors = r.json(), []
        elif r.status_code == 207:
            content = r.json()
            success, errors = content["success"], content["errors"]
        else:
            raise NgsiApiError("Batch Create : Unkown HTTP response code {}", r.status_code)
        return BatchResult("create", success, errors)

    @rfc7807_error_handle_async
    async def create(self, entities: Sequence[Entity], batchsize: int = BATCHSIZE) -> BatchResult:
        r = BatchResult("create")
        for i in range(0, len(entities), batchsize):
            r += await self._create(entities[i:i+batchsize])
        return r
    
    @rfc7807_error_handle_async
    async def _upsert(self, entities: Sequence[Entity], opt: Literal["replace", "update"] = "replace") -> BatchResult:
        params = {"options": opt} if opt else {}
        r = await self._session.post(
            f"{self.url}/upsert/",
            content=json.dumps([e for e in entities], cls=NgsiEncoder),
            params=params
        )
        self._client.raise_for_status(r)
        if r.status_code == 201:
            success, errors = r.json(), []
        elif r.status_code == 204:
            success, errors = [e.id for e in entities], []
        elif r.status_code == 207:
            content = r.json()
            success, errors = content["success"], content["errors"]
        else:
            raise NgsiApiError("Batch Upsert : Unkown HTTP response code {}", r.status_code)
        return BatchResult("upsert", success, errors)

    @rfc7807_error_handle_async
    async def upsert(self, entities: Sequence[Entity], *, update: bool = False, batchsize: int = BATCHSIZE) -> BatchResult:
        # default mode (without any option) is "replace", anyway always force the option
        opt = "update" if update else "replace"        
        r = BatchResult("upsert")
        for i in range(0, len(entities), batchsize):
            r += await self._upsert(entities[i:i+batchsize], opt) 
        return r

    @rfc7807_error_handle_async
    async def _update(self, entities: Sequence[Entity], opt: Literal["noOverwrite"] = None) -> BatchResult:
        params = {"options": opt} if opt else {}
        r = await self._session.post(
            f"{self.url}/update/", 
            content=json.dumps([e for e in entities], cls=NgsiEncoder),
            params=params
        )
        self._client.raise_for_status(r)
        if r.status_code == 204:
            success, errors = [e.id for e in entities], []
        elif r.status_code == 207:
            content = r.json()
            success, errors = content["success"], content["errors"]
        else:
            raise NgsiApiError("Batch Update : Unkown HTTP response code {}", r.status_code)
        return BatchResult("update", success, errors)

    @rfc7807_error_handle_async
    async def update(self, entities: Sequence[Entity], *, overwrite: bool = True, batchsize: int = BATCHSIZE) -> BatchResult:
        opt = "noOverwrite" if not overwrite else None
        r = BatchResult("update")
        for i in range(0, len(entities), batchsize):
            r += await self._update(entities[i:i+batchsize], opt) 
        return r

    @rfc7807_error_handle_async
    async def _delete(self, entities: Sequence[EntityOrId]) -> BatchResult:
        r = await self._session.post(
            f"{self.url}/delete/", json=[e.id if isinstance(e, Entity) else e for e in entities]
        )
        self._client.raise_for_status(r)
        if r.status_code == 204:
            success, errors = [e.id for e in entities], []
        elif r.status_code == 207:
            content = r.json()
            success, errors = content["success"], content["errors"]
        else:
            raise NgsiApiError("Batch Delete : Unkown HTTP response code {}", r.status_code)
        return BatchResult("delete", success, errors)

    @rfc7807_error_handle_async
    async def delete(self, entities: Sequence[EntityOrId], batchsize: int = BATCHSIZE) -> BatchResult:
        r = BatchResult("delete")
        for i in range(0, len(entities), batchsize):
            r += await self._delete(entities[i:i+batchsize]) 
        return r
