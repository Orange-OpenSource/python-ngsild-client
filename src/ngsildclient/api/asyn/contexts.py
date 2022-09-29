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
import re
import json
import aiofiles
import logging

if TYPE_CHECKING:
    from .client import AsyncClient

from ngsildclient.model.constants import CORE_CONTEXT
from ..exceptions import rfc7807_error_handle_async


logger = logging.getLogger(__name__)


class Contexts:
    def __init__(self, client: AsyncClient, url: str):
        self._client = client
        self._session = client.client
        self.url = url

    @rfc7807_error_handle_async
    async def list(self, pattern: str = None) -> Optional[dict]:
        r = await self._session.get(f"{self.url}")
        contexts = r.json()
        if pattern is not None:
            contexts = [x for x in contexts if re.search(pattern, x, re.IGNORECASE)]
        return contexts

    @rfc7807_error_handle_async
    async def get(self, ctx: str) -> dict:
        r = await self._session.get(f"{self.url}/{ctx}")
        self._client.raise_for_status(r)
        return r.json()

    @rfc7807_error_handle_async
    async def _delete(self, ctx: str) -> bool:
        r = await self._session.delete(f"{self.url}/{ctx}")
        self._client.raise_for_status(r)
        return bool(r)

    @rfc7807_error_handle_async
    async def delete(self, ctx: str, pattern: str = None) -> bool:
        if pattern is None:
            return await self._delete(ctx)
        deleted = False
        for ctx in self.list():
            if re.search(pattern, ctx, re.IGNORECASE):
                deleted |= await self.delete(ctx)
        return deleted

    @rfc7807_error_handle_async
    async def exists(self, ctx: str) -> bool:
        r = await self._session.get(f"{self.url}/{ctx}")
        if r:
            payload = r.json()
            return "@context" in payload
        return False

    @rfc7807_error_handle_async
    async def cleanup(self) -> None:
        """Delete all contexts except the Core context."""
        for ctx in self.list():
            if ctx != CORE_CONTEXT:
                await self.delete(ctx)

    @rfc7807_error_handle_async
    async def add(self, ctx: dict):
        if not ctx.get("@context"):
            raise ValueError("Expect a JSON object that has a top-level field named @context.")
        r = await self._session.post(f"{self.url}/", json=ctx)
        self._client.raise_for_status(r)

    @rfc7807_error_handle_async
    async def add_file(self, ctxfilename: str):
        async with aiofiles.open(ctxfilename, "r") as fp:
            contents = await fp.read()
            ctx = json.loads(contents)
        await self.add(ctx)
