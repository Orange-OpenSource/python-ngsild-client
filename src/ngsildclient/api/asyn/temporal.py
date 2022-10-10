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
from typing import TYPE_CHECKING, Union, List, Sequence, Generator, Callable, Awaitable
from dataclasses import dataclass
from datetime import timedelta
from isodate import duration_isoformat
from httpx import Response

import logging

if TYPE_CHECKING:
    from .client import AsyncClient

from ..constants import JSONLD_CONTEXT, AggrMethod
from ...utils.urn import Urn
from ..helper.temporal import TemporalQuery
from ...model.entity import Entity
from ..temporal import _addopt, Pagination, TemporalResult, troes_to_dataframe
from ngsildclient.utils import is_pandas_installed

logger = logging.getLogger(__name__)


class Temporal:
    def __init__(self, client: AsyncClient, url: str):
        self._client = client
        self._session = client.client
        self.url = url

    async def _get(
        self,
        eid: Union[str, Entity],
        attrs: Sequence[str] = None,
        ctx: str = None,
        verbose: bool = False,
        lastn: int = 0,
        pagesize: int = 0,  # default broker pageSize
        pageanchor: str = None,
        count: bool = True,
    ) -> TemporalResult:
        eid = eid.id if isinstance(eid, Entity) else Urn.prefix(eid)
        params = {}
        headers = {"Accept": "application/ld+json"}
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        if count:
            _addopt(params, "count")
        params = {}
        if attrs:
            params["attrs"] = ",".join(attrs)
        if lastn > 0:
            params["lastN"] = lastn
        if pagesize > 0:
            params["pageSize"] = pagesize
        if pageanchor is not None:
            params["pageAnchor"] = pageanchor
        if not verbose:
            _addopt(params, "temporalValues")
        r: Response = await self._session.get(f"{self.url}/{eid}", headers=headers, params=params)
        self._client.raise_for_status(r)
        return TemporalResult(r.json(), Pagination.from_headers(r.headers))

    #  equivalent to get_all()
    async def get(
        self,
        eid: Union[str, Entity],
        attrs: Sequence[str] = None,
        ctx: str = None,
        verbose: bool = False,
        pagesize: int = 0,
        as_dataframe: bool = False,
    ) -> List[dict]:
        if as_dataframe:
            if is_pandas_installed():
                verbose = False  # force simplified representation
            else:
                raise ValueError("Cannot export to dataframe : pandas not installed.")
        r: TemporalResult = await self._get(eid, attrs, ctx, verbose, pagesize=pagesize)
        troes: List[dict] = r.result
        while r.pagination.next_url is not None:
            r: TemporalResult = await self._get(
                eid, attrs, ctx, verbose, pagesize=pagesize, pageanchor=r.pagination.next_url
            )
            troes.extend(r.result)
        return troes_to_dataframe(troes) if as_dataframe else troes

    async def _query(
        self,
        eid: Union[str, Entity] = None,
        type: str = None,
        attrs: Sequence[str] = None,
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
        if eid:
            params["id"] = Urn.prefix(eid)
        if type:
            params["type"] = type
        if attrs:
            params["attrs"] = ",".join(attrs)
        if q:
            params["q"] = q
        if gq:
            params["georel"] = gq
        if count:
            _addopt(params, "count")
        if not verbose:
            _addopt(params, "temporalValues")
        if tq is None:
            tq = TemporalQuery().before()
        params |= tq
        if lastn > 0:
            params["lastN"] = lastn
        if pagesize > 0:
            params["pageSize"] = pagesize
        if pageanchor is not None:
            params["pageAnchor"] = pageanchor
        headers = {"Accept": "application/ld+json"}
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
        *,
        eid: Union[str, Entity] = None,
        type: str = None,
        attrs: Sequence[str] = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        verbose: bool = False,
        tq: TemporalQuery = None,
        limit: int = 5,
        as_dataframe: bool = False,
    ) -> List[dict]:
        if as_dataframe:
            if is_pandas_installed():
                verbose = False  # force simplified representation
            else:
                raise ValueError("Cannot export to dataframe : pandas not installed.")
        troes = await self._query(eid, type, attrs, q, gq, ctx, verbose, tq, lastn=limit, pagesize=limit).result
        return troes_to_dataframe(troes) if as_dataframe else troes

    async def query(
        self,
        *,
        eid: Union[str, Entity] = None,
        type: str = None,
        attrs: List[str] = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        verbose: bool = False,
        tq: TemporalQuery = None,
        pagesize: int = 0,
        as_dataframe: bool = False,
    ) -> List[dict]:
        """Retrieve Temporal Representation of Entities (TRoE) given id, or type and/or query string.

        Retrieve all TRoEs matching the criteria.
        Do the dirty pagination job for you, sending under the wood as many requests as needed.
        Assume data hold in memory. Should not be an issue except for very large datasets.

        Parameters
        ----------
        eid : Union[str, Entity]
            The entity identifier or the entity instance
        etype : str
            The entity's type
        attrs : Sequence[str]
            The list of the attributes (changing over time) you're interested in
        ctx : str
            The context
        q: str
            The query string (NGSI-LD Query Language)
        gq: str
            The geoquery string (NGSI-LD Geoquery Language)
        verbose: bool
            Default is False, meaning the result is formatted as simplified TRoE.
        tq: TemporalQuery
            The temporal query as a py:class:: TemporalQuery instance
        lastn: int
            Among the temporal values, limit the result to the latest <lastn> values.
            By default returns all values.
        pagesize: int
            By default the broker pagesize default.
        as_dataframe : bool
            Default is false, meaning it returns JSON TRoE.
            If set returns a pandas dataframe. Requires pandas.
        limit: int
            The number of entities retrieved in each request

        Returns
        -------
        list[dict]
            The Temporal Representation of the Entities matching the given criteria

        Example
        -------
        >>> with AsyncClient() as client:
        >>>     troe = await client.temporal.query(type="RoomObserved")
        """
        if as_dataframe:
            if is_pandas_installed():
                verbose = False  # force simplified representation
            else:
                raise ValueError("Cannot export to dataframe : pandas not installed.")
        r: TemporalResult = await self._query(eid, type, attrs, q, gq, ctx, verbose, tq, pagesize=pagesize)
        troes: List[dict] = r.result
        while r.pagination.next_url is not None:
            r: TemporalResult = await self._query(
                eid, type, attrs, q, gq, ctx, verbose, tq, pagesize=pagesize, pageanchor=r.pagination.next_url
            )
            troes.extend(r.result)
        return troes_to_dataframe(troes) if as_dataframe else troes

    async def query_generator(
        self,
        *,
        eid: Union[str, Entity] = None,
        type: str = None,
        attrs: Sequence[str] = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        verbose: bool = False,
        tq: TemporalQuery = None,
        pagesize: int = 0,
    ) -> Awaitable[Generator[List[dict], None, None]]:
        r: TemporalResult = await self._query(eid, type, attrs, q, gq, ctx, verbose, tq, pagesize=pagesize)
        troes = r.result
        for troe in troes:
            yield troe
        while r.pagination.next_url is not None:
            r: TemporalResult = await self._query(
                eid, type, attrs, q, gq, ctx, verbose, tq, pagesize=pagesize, pageanchor=r.pagination.next_url
            )
        for troe in troes:
            yield troe

    async def query_handle(
        self,
        *,
        eid: Union[str, Entity] = None,
        type: str = None,
        attrs: List[str] = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        verbose: bool = False,
        tq: TemporalQuery = None,
        pagesize: int = 0,
        callback: Callable[[Awaitable[Entity]], None],
    ) -> None:
        async for troe in self.query_generator(
            eid=eid, type=type, attrs=attrs, q=q, gq=gq, ctx=ctx, verbose=verbose, tq=tq, pagesize=pagesize
        ):
            callback(troe)

    async def aggregate(
        self,
        *,
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
        methods: Sequence[AggrMethod] = [AggrMethod.AVERAGE],
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
        _addopt(params, "aggregatedValues")
        if count:
            _addopt(params, "count")
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
        headers = {"Accept": "application/ld+json"}
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        r: Response = await self._session.get(
            self.url,
            headers=headers,
            params=params,
        )
        self._client.raise_for_status(r)
        return TemporalResult(r.json(), Pagination.from_headers(r.headers))
