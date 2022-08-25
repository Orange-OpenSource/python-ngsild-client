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
from typing import TYPE_CHECKING, Optional
from functools import partialmethod
from hashlib import sha1

import re
import json

from ...model.constants import CORE_CONTEXT
from ..exceptions import NgsiApiError

if TYPE_CHECKING:
    from .client import AsyncClient
from ..exceptions import NgsiResourceNotFoundError, rfc7807_error_handle_async


class Subscriptions:
    def __init__(self, client: AsyncClient, url: str):
        self._client = client
        self._session = client.client
        self.url = url

    @rfc7807_error_handle_async
    async def create(self, subscr: dict, raise_on_conflict: bool = True) -> bool:
        if raise_on_conflict:
            conflicts = await self.conflicts(subscr)
            if conflicts:
                raise ValueError(f"Some subscriptions already exist with same target : {conflicts}")
        headers = {"Content-Type": "application/ld+json"}  # overrides session headers
        r = await self._client.client.post(url=f"{self.url}/", headers=headers, json=subscr)
        self._client.raise_for_status(r)
        location: str = r.headers.get("Location")
        if location is None:
            if self._client.ignore_errors:
                return None
            else:
                raise NgsiApiError("Missing Location header")
        id_returned_from_broker = location.rsplit("/", 1)[-1]
        id = subscr.get("id")
        if id is not None and id != id_returned_from_broker:
            raise NgsiApiError(
                f"Broker returned wrong id. Expected={id} Returned={id_returned_from_broker}"
            )
        return id_returned_from_broker

    @rfc7807_error_handle_async
    async def list(self, pattern: str = None, ctx: str = CORE_CONTEXT) -> Optional[dict]:
        headers = {
            "Accept": "application/ld+json",
            # "Content-Type": None,
        }  # overrides session headers
        if ctx is not None:
            headers[
                "Link"
            ] = f'<{ctx}>; rel="{CORE_CONTEXT}"; type="application/ld+json"'
        r = await self._session.get(f"{self.url}")
        subscriptions = r.json()
        if pattern is not None:
            subscriptions = [
                x
                for x in subscriptions
                if re.search(
                    pattern, x.get("name", "") + x.get("description", ""), re.IGNORECASE
                )
            ]
        return subscriptions

    @staticmethod
    def _criteria_only(subscr: dict):
        params = subscr.copy()
        params.pop("id", None)
        params.pop("name", None)
        params.pop("description", None)
        params.pop("isActive", None)
        return params

    @staticmethod
    def _hash(subscr: dict):
        criteria = Subscriptions._criteria_only(subscr)
        return sha1(json.dumps(criteria, sort_keys=True).encode("utf-8")).digest()

    @rfc7807_error_handle_async
    async def conflicts(self, subscr: dict, ctx: str = CORE_CONTEXT) -> list:
        hashref = Subscriptions._hash(subscr)
        headers = {
            "Accept": "application/ld+json",
            # "Content-Type": None,
        }  # overrides session headers
        if ctx is not None:
            headers[
                "Link"
            ] = f'<{ctx}>; rel="{CORE_CONTEXT}"; type="application/ld+json"'
        r = await self._session.get(f"{self.url}")
        return [x for x in r.json() if Subscriptions._hash(x) == hashref]

    @rfc7807_error_handle_async
    async def get(self, id: str, ctx: str = CORE_CONTEXT) -> dict:
        headers = {
            "Accept": "application/ld+json",
            # "Content-Type": None,
        }  # overrides session headers
        if ctx is not None:
            headers[
                "Link"
            ] = f'<{ctx}>; rel="{CORE_CONTEXT}"; type="application/ld+json"'
        r = await self._session.get(f"{self.url}/{id}", headers=headers)
        self._client.raise_for_status(r)
        return r.json()

    @rfc7807_error_handle_async
    async def exists(self, id: str, ctx: str = CORE_CONTEXT) -> bool:
        try:
            payload = await self.get(id, ctx)
            if payload:
                return "@context" in payload
        except NgsiResourceNotFoundError:
            return False
        return False

    @rfc7807_error_handle_async
    async def _delete(self, id: str) -> bool:
        r = await self._session.delete(f"{self.url}/{id}")
        self._client.raise_for_status(r)
        return bool(r)

    @rfc7807_error_handle_async
    async def delete(self, pattern: str) -> bool:
        deleted = False
        for subscription in await self.list(pattern):
            deleted |= await self._delete(subscription["id"])
        return deleted

    purge = partialmethod(delete, pattern=None)
