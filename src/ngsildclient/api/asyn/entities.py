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
from typing import TYPE_CHECKING, Union, Optional, List
from httpx import Response
import logging

if TYPE_CHECKING:
    from .client import AsyncClient

from ..constants import EntityId, JSONLD_CONTEXT
from ...model.entity import Entity

from ..exceptions import rfc7807_error_handle_async, NgsiApiError, NgsiAlreadyExistsError

logger = logging.getLogger(__name__)


class Entities:
    def __init__(self, client: AsyncClient, url: str):
        self._client = client
        self.url = url

    @rfc7807_error_handle_async
    async def create(self, entity: Entity, skip: bool = False, overwrite: bool = False) -> Optional[Entity]:
        headers = {"Content-Type": "application/ld+json"}
        r: Response = await self._client.client.post(url=f"{self.url}/", headers=headers, json=entity._payload)

        if r.status_code == 409:  # already exists
            if skip:
                return None
            elif overwrite or self._client.overwrite:
                return self.update(entity, check_exists=False)

        self._client.raise_for_status(r)

        location = r.headers.get("Location")
        if location is None:
            if self._client.ignore_errors:
                return None
            else:
                raise NgsiApiError("Missing Location header")
        logger.info(f"{r.status_code=}")
        logger.info(f"{location=}")
        id_returned_from_broker = location.rsplit("/", 1)[-1]
        if entity.id != id_returned_from_broker:
            raise NgsiApiError(f"Broker returned wrong id. Expected={entity.id} Returned={id_returned_from_broker}")
        return entity

    @rfc7807_error_handle_async
    async def get(
        self,
        eid: Union[EntityId, Entity],
        ctx: str = None,
        asdict: bool = False,
        **kwargs,
    ) -> Entity:
        eid = eid.id if isinstance(eid, Entity) else eid
        headers = {"Accept": "application/ld+json"}  # overrides session headers
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        logger.info(f"{headers=}")
        r: Response = await self._client.client.get(f"{self.url}/{eid}", headers=headers, **kwargs)
        r.raise_for_status()
        return r.json() if asdict else Entity.from_dict(r.json())

    @rfc7807_error_handle_async
    async def delete(self, eid: Union[EntityId, Entity]) -> bool:
        eid = eid.id if isinstance(eid, Entity) else eid
        logger.info(f"{eid=}")
        logger.info(f"url={self.url}/{eid}")
        r: Response = await self._client.client.delete(f"{self.url}/{eid}")
        logger.info(f"requests: {r.request.url}")
        r.raise_for_status()
        return bool(r)

    @rfc7807_error_handle_async
    async def exists(self, eid: Union[EntityId, Entity]) -> bool:
        eid = eid.id if isinstance(eid, Entity) else eid
        r: Response = await self._client.client.get(f"{self.url}/{eid}")
        if r:
            payload = r.json()
            return "@context" in payload
        return False

    @rfc7807_error_handle_async
    async def upsert(self, entity: Entity) -> Entity:
        try:
            return await self.create(entity)
        except NgsiAlreadyExistsError:
            await self.delete(entity)
            return await self.create(entity)

    @rfc7807_error_handle_async
    async def update(self, entity: Entity, check_exists: bool = True) -> Optional[Entity]:
        if check_exists and await self.exists(entity):
            await self.delete(entity)
            return await self.create(entity)
        return None

    @rfc7807_error_handle_async
    async def query(
        self,
        type: str = None,
        q: str = None,
        ctx: str = None,
        limit: int = 0,
        offset: int = 0,
        **kwargs,
    ) -> List[Entity]:
        params = {}
        if limit != 0:
            params |= {"limit": limit}
        if offset != 0:
            params |= {"offset": offset}
        if type is None and q is None:
            raise ValueError("Must indicate at least a type or a query string")
        if type:
            params["type"] = type
        if q:
            params["q"] = q
        headers = {
            "Accept": "application/ld+json",
        }  # overrides session headers
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        r: Response = await self._client.client.get(
            self.url,
            headers=headers,
            params=params,
        )
        r.raise_for_status()
        entities = r.json()
        logger.debug(f"{entities=}")
        return [Entity.from_dict(entity) for entity in entities]

    @rfc7807_error_handle_async
    async def count(self, type: str = None, q: str = None, ctx: str = None, **kwargs) -> int:
        params = {"limit": 0, "count": "true"}
        if type is None and q is None:
            raise ValueError("Must indicate at least a type or a query string")
        if type:
            params["type"] = type
        if q:
            params["q"] = q

        headers = {
            "Accept": "application/json",
        }  # overrides session headers
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        r: Response = await self._client.client.get(
            self.url,
            headers=headers,
            params=params,
        )
        r.raise_for_status()
        count = int(r.headers["NGSILD-Results-Count"])
        return count