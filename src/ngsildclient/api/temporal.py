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

from .constants import JSONLD_CONTEXT, AggrMethod
from ..utils.urn import Urn
from .helper.temporal import TemporalQuery
from ..model.entity import Entity
from ngsildclient.utils import iso8601, is_pandas_installed, _addopt
from .temporal_alt import TemporalAlt

logger = logging.getLogger(__name__)

def _troes_to_dfdict(troes: dict):
    # the result dictionary is independant of the number of attributes !
    d = {}
    if not isinstance(troes, List):
        troes = [troes]
    troe: dict = troes[0]
    nentities = len(troes)
    attrs = [str(k) for k in troe.keys() if k not in ("id", "type", "@context")]
    attr0 = attrs[0]
    datetimes = [x[1] for x in troe[attr0]["values"]]
    nmeasures: int = len(datetimes)
    for attr in attrs[1:]:
        if [x[1] for x in troe[attr]["values"]] != datetimes:
            raise ValueError("Cannot pack result : attributes have distinct observedAt values.")
    etype = troe["type"]
    d[etype] = reduce(iconcat, [[troe["id"].rsplit(":")[-1]] * nmeasures for troe in troes], [])
    d["observed"] = [iso8601.parse(x)[2] for x in datetimes] * nentities
    for attr in attrs:
        d[attr] = []
        for troe in troes:
            for value in troe[attr]["values"]:
                d[attr].append(value[0])
    return d


def troes_to_dataframe(troes: dict):
    d = _troes_to_dfdict(troes)
    try:
        import pandas
    except ImportError:
        raise ValueError("Cannot export to dataframe : pandas not installed.")
    return pandas.DataFrame(d)


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
    """A wrapper for the NGSI-LD API temporal endpoint."""
    def __init__(self, client: Client, url: str, url_alt_temporal_query: str):
        self._client = client
        self._session = client.session
        self.url = url
        self.url_alt_temporal_query = url_alt_temporal_query
        self._alt = TemporalAlt(self._client, url_alt_temporal_query)

    @property
    def alt(self):
        return self._alt

    def _get(
        self,
        eid: Union[str, Entity],
        attrs: List[str] = None,
        ctx: str = None,
        verbose: bool = False,
        lastn: int = 0,
        pagesize: int = 0,  # default broker pageSize
        pageanchor: str = None,
        count: bool = True,
    ) -> TemporalResult:
        eid = eid.id if isinstance(eid, Entity) else Urn.prefix(eid)
        params = {}
        headers = {
            "Accept": "application/ld+json",
            "Content-Type": None,
        }  # overrides session headers
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
        r = self._session.get(f"{self.url}/{eid}", headers=headers, params=params)
        self._client.raise_for_status(r)
        return TemporalResult(r.json(), Pagination.from_headers(r.headers))

    #  equivalent to get_all()
    def get(
        self,
        eid: Union[str, Entity],
        attrs: List[str] = None,
        ctx: str = None,
        verbose: bool = False,
        pagesize: int = 0,
        as_dataframe: bool = False,
    ) -> List[dict]:
        """Retrieve the Temporal Representation of (an) Entity (TRoE) given its id.

        If already dealing with an entity instance one can provide the entity itself instead of its id.

        Parameters
        ----------
        eid : Union[str, Entity]
            The entity identifier or the entity instance
        attrs : List[str]
            The list of the attributes (changing over time) you're interested in
        ctx : str
            The context
        verbose: bool
            Default is False, meaning the result is formatted as simplified TRoE.
        as_dataframe : bool
            Default is false, meaning it returns JSON TRoE.
            If set returns a pandas dataframe. Requires pandas.

        Returns
        -------
        dict
            A dict equivalent to the Temporal Representation of the Entity
        """

        if as_dataframe:
            if is_pandas_installed():
                verbose = False  # force simplified representation
            else:
                raise ValueError("Cannot export to dataframe : pandas not installed.")
        r: TemporalResult = self._get(eid, attrs, ctx, verbose, pagesize=pagesize)
        troes: List[dict] = r.result
        while r.pagination.next_url is not None:
            r: TemporalResult = self._get(eid, attrs, ctx, verbose, pagesize=pagesize, pageanchor=r.pagination.next_url)
            troes.extend(r.result)
        return troes_to_dataframe(troes) if as_dataframe else troes

    def _query(
        self,
        eid: Union[str, Entity] = None,
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
        headers = {
            "Accept": "application/ld+json",
            "Content-Type": None,
        }  # overrides session headers
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        r = self._session.get(
            self.url,
            headers=headers,
            params=params,
        )
        self._client.raise_for_status(r)
        return TemporalResult(r.json(), Pagination.from_headers(r.headers))

    def query_head(
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
        limit: int = 5,
        as_dataframe: bool = False,
    ) -> List[dict]:
        if as_dataframe:
            if is_pandas_installed():
                verbose = False  # force simplified representation
            else:
                raise ValueError("Cannot export to dataframe : pandas not installed.")
        troes = self._query(eid, type, attrs, q, gq, ctx, verbose, tq, lastn=limit, pagesize=limit).result
        return troes_to_dataframe(troes) if as_dataframe else troes

    def query(
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
        lastn: int = 0,
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
        attrs : List[str]
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
        >>> with Client() as client:
        >>>     troe = client.temporal.query(type="RoomObserved")
        """
        if as_dataframe:
            if is_pandas_installed():
                verbose = False  # force simplified representation
            else:
                raise ValueError("Cannot export to dataframe : pandas not installed.")
        r: TemporalResult = self._query(eid, type, attrs, q, gq, ctx, verbose, tq, lastn=lastn, pagesize=pagesize)
        troes: List[dict] = r.result
        while r.pagination.next_url is not None:
            r: TemporalResult = self._query(
                eid, type, attrs, q, gq, ctx, verbose, tq, lastn=lastn, pagesize=pagesize, pageanchor=r.pagination.next_url
            )
            troes.extend(r.result)
        return troes_to_dataframe(troes) if as_dataframe else troes

    def query_generator(
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
    ) -> Generator[List[dict], None, None]:
        r: TemporalResult = self._query(eid, type, attrs, q, gq, ctx, verbose, tq, pagesize=pagesize)
        troes = r.result
        yield from troes
        while r.pagination.next_url is not None:
            r: TemporalResult = self._query(
                eid, type, attrs, q, gq, ctx, verbose, tq, pagesize=pagesize, pageanchor=r.pagination.next_url
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

    def aggregate(
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
        headers = {
            "Accept": "application/ld+json",
            "Content-Type": None,
        }  # overrides session headers
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        r = self._session.get(
            self.url,
            headers=headers,
            params=params,
        )
        self._client.raise_for_status(r)
        return TemporalResult(r.json(), Pagination.from_headers(r.headers))
