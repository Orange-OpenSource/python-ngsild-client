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
from typing import TYPE_CHECKING, Union, List, Optional, Generator, Callable
from dataclasses import dataclass
from datetime import timedelta
from isodate import duration_isoformat
from httpx import Response

import logging

if TYPE_CHECKING:
    from .client import AsyncClient

from ..constants import EntityId, JSONLD_CONTEXT, AggrMethod
from ..helper.temporal import TemporalQuery
from ...model.entity import Entity


logger = logging.getLogger(__name__)


def addopt(params: dict, newopt: str):
    if params.get("options", "") == "":
        params["options"] = newopt
    else:
        params["options"] += f",{newopt}"


@dataclass
class Pagination:
    count: int = 0
    pagesize: int = 0
    next_url: Optional[str] = None
    prev_url: Optional[str] = None

    @classmethod
    def from_headers(cls, headers: dict):
        count = int(headers.get("NGSILD-Results-Count", 0))
        pagesize = int(headers.get("Page-Size", 0))
        next_url = headers.get("Next-Page")
        prev_url = headers.get("Previous-Page")
        return cls(count, pagesize, next_url, prev_url)


@dataclass
class TemporalResult:
    result: List[dict]
    pagination: Optional[Pagination] = None


class Temporal:
    def __init__(self, client: AsyncClient, url: str):
        self._client = client
        self._session = client.client
        self.url = url

    async def get(
        self,
        eid: Union[EntityId, Entity],
        ctx: str = None,
        verbose: bool = False,
        lastn: int = 0,
        pagesize: int = 0,  # default broker pageSize
        pageanchor: str = None,
        count: bool = True,
    ) -> TemporalResult:
        eid = eid.id if isinstance(eid, Entity) else eid
        params = {}
        headers = {
            "Accept": "application/ld+json",
            "Content-Type": None,
        }  # overrides session headers
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        if count:
            addopt(params, "count")
        params = {}
        if lastn > 0:
            params["lastN"] = lastn
        if pagesize > 0:
            params["pageSize"] = pagesize
        if pageanchor is not None:
            params["pageAnchor"] = pageanchor
        if not verbose:
            addopt(params, "temporalValue")
        r: Response = await self._session.get(f"{self.url}/{eid}", headers=headers, params=params)
        self._client.raise_for_status(r)
        return TemporalResult(r.json(), Pagination.from_headers(r.headers))

    async def _query(
        self,
        type: str = None,
        attrs: List[str] = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        verbose: bool = False,
        tq: TemporalQuery = None,
        lastn: int = 0,
        pagesize: int = 0,  # default broker pageSize
        pageanchor: str = None,
        count: bool = True,
    ) -> TemporalResult:
        params = {}
        if type:
            params["type"] = type
        if attrs:
            params["attrs"] = ",".join(attrs)
        if q:
            params["q"] = q
        if gq:
            params["georel"] = gq
        if count:
            addopt(params, "count")
        if not verbose:
            addopt(params, "temporalValue")
        if tq is None:
            tq = TemporalQuery().before()
        params |= tq
        if lastn > 0:
            params["lastN"] = lastn
        if pagesize > 0:
            params["pageSize"] = pagesize
        if pageanchor is not None:
            params["pageAnchor"] = pageanchor
        headers = {
            "Accept": "application/ld+json",
        }  # overrides session headers
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        r: Response = await self._session.get(
            self.url,
            headers=headers,
            params=params,
        )
        self._client.raise_for_status(r)
        return TemporalResult(r.json(), Pagination.from_headers(r.headers))

    async def query_head(
        self,
        type: str = None,
        attrs: List[str] = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        verbose: bool = False,
        tq: TemporalQuery = None,
        limit: int = 5,
    ) -> List[dict]:
        r = await self._query(type, attrs, q, gq, ctx, verbose, tq, lastn=limit, pagesize=limit)
        return r.result

    async def query_all(
        self,
        type: str = None,
        attrs: List[str] = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        verbose: bool = False,
        tq: TemporalQuery = None,
        pagesize: int = 0,
    ) -> List[dict]:
        r: TemporalResult = await self._query(type, attrs, q, gq, ctx, verbose, tq, pagesize=pagesize)
        troes: List[dict] = r.result
        while r.pagination.next_url is not None:
            r: TemporalResult = await self._query(type, attrs, q, gq, ctx, verbose, tq, pagesize=pagesize, pageanchor=r.pagination.next_url)
            troes.extend(r.result)
        return troes

    async def query_generator(
        self,
        type: str = None,
        attrs: List[str] = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        verbose: bool = False,
        tq: TemporalQuery = None,
        pagesize: int = 0,
    ) -> Generator[List[dict], None, None]:
        r: TemporalResult = await self._query(type, attrs, q, gq, ctx, verbose, tq, pagesize=pagesize)
        for x in r.result:
            yield x
        while r.pagination.next_url is not None:
            r: TemporalResult = await self._query(type, attrs, q, gq, ctx, verbose, tq, pagesize=pagesize, pageanchor=r.pagination.next_url)
            for x in r.result:
                yield x
        return

    async def query_handle(
        self,
        type: str = None,
        attrs: List[str] = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        verbose: bool = False,
        tq: TemporalQuery = None,
        *,
        callback: Callable[[Entity], None],
    ) -> None:
        async for troe in self.query_generator(type, attrs, q, gq, ctx, verbose, tq):
            callback(troe)

    async def aggregate(
        self,
        type: str = None,
        attrs: List[str] = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        tq: TemporalQuery = None,
        lastn: int = 0,
        pagesize: int = 0,  # default broker pageSize
        pageanchor: str = None,
        count: bool = False,
        methods: List[AggrMethod] = [AggrMethod.AVERAGE],
        period: timedelta = timedelta(days=1),
    ) -> TemporalResult:
        params = {}
        if type:
            params["type"] = type
        if attrs:
            params["attrs"] = ",".join(attrs)
        if q:
            params["q"] = q
        if gq:
            params["georel"] = gq
        addopt(params, "aggregatedValues")
        if count:
            addopt(params, "count")
        if tq is None:
            tq = TemporalQuery().before()
        params |= tq
        if lastn > 0:
            params["lastN"] = lastn
        if pagesize > 0:
            params["pageSize"] = pagesize
        if pageanchor is not None:
            params["pageAnchor"] = pageanchor
        params["aggrMethods"] = ",".join([m.value for m in methods])
        params["aggrPeriodDuration"] = duration_isoformat(period)
        headers = {
            "Accept": "application/ld+json",
        }  # overrides session headers
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        r: Response = await self._session.get(
            self.url,
            headers=headers,
            params=params,
        )
        self._client.raise_for_status(r)
        return TemporalResult(r.json(), Pagination.from_headers(r.headers))
