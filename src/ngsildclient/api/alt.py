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
from typing import TYPE_CHECKING, Generator, Callable

import logging

if TYPE_CHECKING:
    from .client import Client

from typing import List
from math import ceil
from ngsildclient.model.entity import Entity
from ngsildclient.api.constants import PAGINATION_LIMIT_MAX
from ngsildclient.api.exceptions import NgsiClientTooManyResultsError


logger = logging.getLogger(__name__)


class Alt:
    def __init__(self, client: Client):
        self._client = client
        self._session = client.session

    def count(self, query: dict, ctx: str = None) -> int:
        return self._client.entities._count_alt(query, ctx)

    def query_head(self, query: dict, ctx: str = None, n: int = 5) -> List[Entity]:
        """Retrieve entities given its type and/or query string.

        Retrieve up to PAGINATION_LIMIT_MAX entities.
        Use query() to retrieve all entities.
        Use entities.query() to deal with limit and offset on your own.

        Parameters
        ----------
        query: dict
            The query in JSON-LD format
        ctx: str
            The context
        n: int
            The first n entities to be retrieved
        Returns
        -------
        list[Entity]
            Retrieved entities matching the given type and/or query string

        Example
        -------
        >>> query = {"type": "Query", "entities": [{"type": "Farm"}], "q": "fillingLevel>0.8"}
        >>> with Client() as client:
        >>>     client.alt.query_head(query)
        """
        return self._client.entities._query_alt(query, ctx, limit=n)

    def query(
        self,
        query: dict,
        ctx: str = None,
        limit: int = PAGINATION_LIMIT_MAX,
        max: int = 1_000_000,
    ) -> List[Entity]:
        """Retrieve entities given its type and/or query string.

        Retrieve all entities by sending as many requests as needed, using pagination.
        Assume data hold in memory. Should not be an issue except for very large datasets.

        Parameters
        ----------
        query: dict
            The query in JSON-LD format
        ctx: str
            The context
        limit: int
            The number of entities retrieved in each request

        Returns
        -------
        list[Entity]
            Retrieved entities matching the given type and/or query string

        Example
        -------
        >>> query = {"type": "Query", "entities": [{"type": "Farm"}], "q": "fillingLevel>0.8"}
        >>> with Client() as client:
        >>>     client.alt.query(query)
        """
        entities: list[Entity] = []
        count = self.count(query, ctx=ctx)
        if count > max:
            raise NgsiClientTooManyResultsError(f"{count} results exceed maximum {max}")
        for page in range(ceil(count / limit)):
            entities.extend(self._client.entities._query_alt(query, ctx, limit, page * limit))
        return entities

    def query_generator(
        self,
        query: dict,
        ctx: str = None,
        limit: int = PAGINATION_LIMIT_MAX,
        batch: bool = False,
    ) -> Generator[Entity, None, None]:
        """Retrieve (as a generator) entities given its type and/or query string.

        By returning a generator it allows to process entities on the fly without any risk of exhausting memory.

        Parameters
        ----------
        query: dict
            The query in JSON-LD format
        ctx: str
            The context
        limit: int
            The number of entities retrieved in each request

        Returns
        -------
        list[Entity]
            Retrieved a generator of entities (matching the given type and/or query string)
        """
        count = self.count(query)
        for page in range(ceil(count / limit)):
            if batch:
                yield self._client.entities._query_alt(query, ctx, limit, page * limit)
            else:
                yield from self._client.entities._query_alt(query, ctx, limit, page * limit)

    def query_handle(
        self,
        query: dict,
        ctx: str = None,
        limit: int = PAGINATION_LIMIT_MAX,
        *,
        callback: Callable[[Entity], None],
    ) -> None:
        """Apply a callback function on entity of the query result.

        Parameters
        ----------
        query: dict
            The query in JSON-LD format
        ctx: str
            The context
        limit: int
            The number of entities retrieved in each request
        callback: Callable[Entity]
            The function to be called on each entity of the result

        Example
        -------
        >>> query = {"type": "Query", "entities": [{"type": "Farm"}], "q": "fillingLevel>0.8"}
        >>> with Client() as client:
        >>>     client.alt.query_handle(query, lambda e: print(e))
        """
        for entity in self.query_generator(type, query, ctx, limit, False):
            callback(entity)
