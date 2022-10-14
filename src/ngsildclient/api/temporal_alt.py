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
from functools import reduce
from operator import iconcat


import logging

if TYPE_CHECKING:
    from .client import Client
    from .temporal import TemporalResult, Pagination, troes_to_dataframe

from .constants import JSONLD_CONTEXT
from ..utils import _addopt
from .helper.temporal import TemporalQuery
from ..model.entity import Entity
from ngsildclient.utils import is_pandas_installed
from ngsildclient.model.exceptions import NgsiJsonError

logger = logging.getLogger(__name__)

class TemporalAlt:
    """A wrapper for the NGSI-LD API temporal alternative endpoint."""
    def __init__(self, client: Client, url_alt_temporal_query: str):
        self._client = client
        self._session = client.session
        self.url_alt_temporal_query = url_alt_temporal_query

    def _query(
        self,
        query: dict,
        ctx: str = None,
        lastn: int = 0,
        pagesize: int = 0,  # default broker pageSize
        pageanchor: str = None,
    ) -> TemporalResult:
        params = {}
        if query.get("type") != "Query":
            raise NgsiJsonError("Wrong format. Expect JSON-LD Query data type")
        if lastn > 0:
            params["lastN"] = lastn
        if pagesize > 0:
            params["pageSize"] = pagesize
        if pageanchor is not None:
            params["pageAnchor"] = pageanchor
        headers = {
            "Accept": "application/ld+json",
            "Content-Type": "application/json",
        }
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        r = self._session.post(
            self.url_alt_temporal_query,
            headers=headers,
            params=params,
            json=query
        )
        self._client.raise_for_status(r)
        return TemporalResult(r.json(), Pagination.from_headers(r.headers))

    def query_head(
        self,
        *,
        query: dict,
        ctx: str = None,
        limit: int = 5,
        as_dataframe: bool = False,
    ) -> List[dict]:
        if as_dataframe:
            if is_pandas_installed():
                verbose = False  # force simplified representation
            else:
                raise ValueError("Cannot export to dataframe : pandas not installed.")
        troes = self._query(query, ctx, lastn=limit, pagesize=limit).result
        return troes_to_dataframe(troes) if as_dataframe else troes

    def query(
        self,
        *,
        query: dict,
        ctx: str = None,
        lastn: int = 0,
        pagesize: int = 0,
        as_dataframe: bool = False,
    ) -> List[dict]:
        if as_dataframe:
            if is_pandas_installed():
                verbose = False  # force simplified representation
            else:
                raise ValueError("Cannot export to dataframe : pandas not installed.")
        r: TemporalResult = self._query(query, ctx, lastn=lastn, pagesize=pagesize)
        troes: List[dict] = r.result
        while r.pagination.next_url is not None:
            r: TemporalResult = self._query(
                query, ctx, verbose, lastn=lastn, pagesize=pagesize, pageanchor=r.pagination.next_url
            )
            troes.extend(r.result)
        return troes_to_dataframe(troes) if as_dataframe else troes

    def query_generator(
        self,
        *,
        query: dict,
        ctx: str = None,
        pagesize: int = 0,
    ) -> Generator[List[dict], None, None]:
        r: TemporalResult = self._query(query, ctx, pagesize=pagesize)
        troes = r.result
        yield from troes
        while r.pagination.next_url is not None:
            r: TemporalResult = self._query(
               query, ctx, pagesize=pagesize, pageanchor=r.pagination.next_url
            )
            troes = r.result
            yield from troes

    def query_handle(
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
        callback: Callable[[Entity], None],
    ) -> None:
        for troe in self.query_generator(eid, type, attrs, q, gq, ctx, verbose, tq, pagesize):
            callback(troe)
