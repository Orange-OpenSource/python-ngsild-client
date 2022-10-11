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

import logging
import httpx
from httpx._types import AuthTypes
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Generator, List, Union, Callable
from math import ceil

from ...model.entity import Entity
from ..constants import *
from ..exceptions import *
from .entities import Entities
from .batch import Batch, BatchResult
from .types import Types
from .contexts import Contexts
from .subscriptions import Subscriptions
from .temporal import Temporal

if TYPE_CHECKING:
    from ngsildclient.model.constants import EntityOrId

logger = logging.getLogger(__name__)

"""This module contains the definition of the AsyncClient class.
"""


class AsyncClient:
    """An implementation of the NGSI-LD client API.

    It allows to connect to a NGSI-LD Context Broker, check the connection and
    try to identify the vendor.
    As for now it focuses on the /entities/{entityId} endpoint.
    Allowed operations are :
    - create(), update(), upsert()
    - get(), exists()
    - delete()

    Update() and upsert() operations are not atomic, as they
    aren't provided as-is by the API, but require chaining 2 API calls.

    When encountering errors the Client throws enriched
    Exceptions, as NGSI-LD API supports ProblemDetails [IETF RFC 7807].

    Example
    -------
    >>> from ngsildclient import *

    >>> # Here we don't build our own NGSI-LD entity, but grab an example from SmartDatamodels
    >>> farm = Entity.load(SmartDatamodels.SmartAgri.Agrifood.AgriFarm)

    >>> # farm.pprint()

    >>> # Connect to the Context Broker and upsert the entity
    >>> # As we don't provide any arguments to the Client constructor
    >>> # It connects to localhost and default port (without any authentication)
    >>> with Client() as client:
    >>>     client.upsert(farm)
    """

    def __init__(
        self,
        hostname: str = "localhost",
        port: int = NGSILD_DEFAULT_PORT,
        port_temporal: int = NGSILD_TEMPORAL_PORT,
        secure: bool = False,
        useragent: str = UA,
        tenant: str = None,
        overwrite: bool = False,
        ignore_errors: bool = False,
        proxy: str = None,
        custom_auth: AuthTypes = None,
    ):
        """Create a Client instance to interact with the Context Broker.

        The Client allows to retrieve or send entities
        (model.Entity instances) to the Context Broker.
        For example, one can retrieve an entity from the Context Broker,
        modify it (update/delete/add properties),
        and send it back to the Context Broker.

        Parameters
        ----------
        hostname : str, optional
            the hostname to connect to, by default "localhost"
        port : int, optional
            the TCP port to connect to, by default NGSILD_DEFAULT_PORT
        secure : bool, optional
            whether to use TLS, by default False
        useragent : str, optional
            the User Agent string sent in the HTTP headers, by default UA
        tenant : str, optional
            the tenant string in case you make use of multi-tenancy, by default None
        overwrite : bool, optional
            if set create() will behave like upsert(), by default False
        ignore_errors : bool, optional
            if set tests the connection at init time and raisesan exception if failed, by default False
        proxy : str, optional
            proxies all requests to the provided proxy string (for debugging purpose), by default None

        See Also
        --------
        api.model.Entity

        """
        self.hostname = hostname
        self.port = port
        self.port_temporal = port_temporal
        self.secure = secure
        self.scheme = "https" if secure else "http"
        self.url = f"{self.scheme}://{hostname}:{port}"
        self.basepath = f"{self.url}/{NGSILD_PATH}"
        self.useragent = useragent
        self.tenant = tenant
        self.overwrite = overwrite
        self.ignore_errors = ignore_errors
        self.proxy = proxy

        headers = {
            "User-Agent": self.useragent,
            "Accept": "application/ld+json",
            # "Content-Type": "application/ld+json",
        }
        if tenant is not None:
            headers["NGSILD-Tenant"] = tenant
        proxies = {proxy} if proxy else None

        logger.info("Connecting client ...")
        self.client = httpx.AsyncClient(auth=custom_auth, headers=headers, proxies=proxies)
        self._entities = Entities(self, f"{self.url}/{ENDPOINT_ENTITIES}")
        self._batch = Batch(self, f"{self.url}/{ENDPOINT_BATCH}")
        self._types = Types(self, f"{self.url}/{ENDPOINT_TYPES}")
        self._contexts = Contexts(self, f"{self.url}/{ENDPOINT_CONTEXTS}")
        self._subscriptions = Subscriptions(self, f"{self.url}/{ENDPOINT_SUBSCRIPTIONS}")
        url_temporal = f"{self.scheme}://{hostname}:{port_temporal}"
        temporal_path = (
            f"{url_temporal}/{NGSILD_BASEPATH}/temporal/entities"
            if port_temporal == port  # temporal share the same port and basepath
            else f"{url_temporal}/temporal/entities"
        )
        self._temporal = Temporal(self, temporal_path)

    def raise_for_status(self, r: httpx.Response):
        """Raises an exception depending on the API response.

        Parameters
        ----------
        r : Response
            Response from the Context Broker
        """
        if not self.ignore_errors:
            r.raise_for_status()

    @property
    def entities(self):
        return self._entities

    @property
    def batch(self):
        return self._batch

    @property
    def types(self):
        return self._types

    @property
    def contexts(self):
        return self._contexts

    @property
    def subscriptions(self):
        return self._subscriptions

    @property
    def temporal(self):
        return self._temporal

    async def close(self):
        """Terminates the client.

        Closes the underlying httpx.AsyncClient.
        """
        await self.client.aclose()

    async def create(self, *entities) -> Union[bool, BatchResult]:
        """Create one or many entities.

        Facade method backed by Batch.create() or Entities.create()

        Parameters
        ----------
        entities : 
            Entities to be created by the Context Broker
            Either a single Entity, or a list of entities, or comma-separated entities

        Returns
        -------
        Entity
            The entities successfully upserted
        """        
        if len(entities) == 1:
            if isinstance(entities[0], Entity):
                entity = entities[0]
                return await self.entities.create(entity)
            else:
                entities = entities[0]
        return await self.batch.create(entities)

    async def get(
        self,
        entity: EntityOrId,
        ctx: str = None,
        asdict: bool = False,
        **kwargs,
    ) -> Entity:
        """Retrieve an entity given its id.

        Facade method for Entities.retrieve().
        If already dealing with an entity instance one can provide the entity itself instead of its id.

        Parameters
        ----------
        entity : EntityOrId
            The entity identifier or the entity instance
        ctx : str
            The context
        asdict : bool, optional
            If set (instead of returning an Entity) returns the raw API response (a Python dict that represents the JSON response), by default False

        Returns
        -------
        Entity
            The retrieved entity
        """
        return await self.entities.get(entity, ctx, asdict, **kwargs)

    async def delete(self, *entities) -> Union[bool, BatchResult]:
        """Delete one or many entities.

        Facade method backed by Batch.delete() or Entities.delete()

        Parameters
        ----------
        entities : 
            Entities to be deleted by the Context Broker
            Either a single Entity, or a list of entities, or comma-separated entities

        Returns
        -------
        Entity
            The entities successfully upserted
        """        
        if len(entities) == 1:
            if isinstance(entities[0], Entity):
                entity = entities[0]
                return await self.entities.delete(entity)
            else:
                entities = entities[0]
        return await self.batch.delete(entities)
            

    async def delete_from_file(self, filename: str) -> Union[bool, dict]:
        """Delete in the broker all entities present in the JSON file.

        Parameters
        ----------
        filename : str
            Points to the JSON input file that contains entities.
        """
        entities = await Entity.load_async(filename)
        return await self.delete(entities)

    async def exists(self, entity: EntityOrId) -> bool:
        """Tests if an entity exists.

        Facade method for Entities.exists().
        If already dealing with an entity instance one can provide the entity itself instead of its id.

        Parameters
        ----------
        entity : EntityOrId
            The entity identifier or the entity instance

        Returns
        -------
        bool
            True if the entity exists
        """
        return await self.entities.exists(entity)

    async def upsert(self, *entities) -> Union[bool, BatchResult]:
        """Upsert one or many entities.

        Facade method backed by Batch.upsert() or Entities.upsert()

        Parameters
        ----------
        entities : 
            Entities to be upserted by the Context Broker
            Either a single Entity, or a list of entities, or comma-separated entities

        Returns
        -------
        Entity
            The entities successfully upserted
        """        
        if len(entities) == 1:
            if isinstance(entities[0], Entity):
                entity = entities[0]
                return await self.entities.upsert(entity)
            else:
                entities = entities[0]
        return await self.batch.upsert(entities)

    async def bulk_import(self, filename: str) -> Union[bool, dict]:
        """Upsert all entities from a JSON file.

        Parameters
        ----------
        filename : str
            Points to the JSON input file that contains entities.
        """
        entities = await Entity.load_async(filename)
        return await self.upsert(entities)

    async def update(self, *entities) -> Union[bool, BatchResult]:
        """Upsert one or many entities.

        Facade method backed by Batch.update() or Entities.update()

        Parameters
        ----------
        entities : 
            Entities to be upserted by the Context Broker
            Either a single Entity, or a list of entities, or comma-separated entities

        Returns
        -------
        Entity
            The entities successfully updated
        """        
        if len(entities) == 1:
            if isinstance(entities[0], Entity):
                entity = entities[0]
                return await self.entities.update(entity)
            else:
                entities = entities[0]
        return await self.batch.update(entities)

    async def query_head(
        self, type: str = None, q: str = None, gq: str = None, ctx: str = None, n: int = 5
    ) -> List[Entity]:
        """Retrieve entities given its type and/or query string.

        Retrieve up to PAGINATION_LIMIT_MAX entities.
        Use query_all() to retrieve all entities.
        Use entities.query() to deal with limit and offset on your own.

        Parameters
        ----------
        etype : str
            The entity's type
        q: str
            The query string (NGSI-LD Query Language)
        gq: str
            The geoquery string (NGSI-LD Geoquery Language)
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
        >>> with AsyncClient() as client:
        >>>     await client.query(type="AgriFarm") # match a given type

        >>> with AsyncClient() as client:
        >>>     await client.query(type="AgriFarm", q='contactPoint[email]=="wheatfarm@email.com"') # match type and query
        """
        return await self.entities._query(type, q, gq, ctx, limit=n)

    async def query(
        self,
        type: str = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        limit: int = PAGINATION_LIMIT_MAX,
        max: int = 1_000_000,
    ) -> List[Entity]:
        """Retrieve entities given its type and/or query string.

        Retrieve all entities by sending as many requests as needed, using pagination.
        Assume data hold in memory. Should not be an issue except for very large datasets.

        Parameters
        ----------
        etype : str
            The entity's type
        q: str
            The query string (NGSI-LD Query Language)
        gq: str
            The geoquery string (NGSI-LD Geoquery Language)
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
        >>> with AsyncClient() as client:
        >>>     await client.query(type="AgriFarm") # match a given type

        >>> with AsyncClient() as client:
        >>>     await client.query(type="AgriFarm", q='contactPoint[email]=="wheatfarm@email.com"') # match type and query
        """

        entities: list[Entity] = []
        count = await self.entities.count(type, q, gq, ctx=ctx)
        if count > max:
            raise NgsiClientTooManyResultsError(f"{count} results exceed maximum {max}")
        for page in range(ceil(count / limit)):
            entities.extend(await self.entities._query(type, q, gq, ctx, limit, page * limit))
        return entities

    async def query_generator(
        self,
        type: str = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        limit: int = PAGINATION_LIMIT_MAX,
        batch: bool = False,
    ) -> Generator[Entity, None, None]:
        """Retrieve (as a generator) entities given its type and/or query string.

        By returning a generator it allows to process entities on the fly without any risk of exhausting memory.

        Parameters
        ----------
        etype : str
            The entity's type
        q: str
            The query string (NGSI-LD Query Language)
        gq: str
            The geoquery string (NGSI-LD Geoquery Language)
        ctx: str
            The context
        limit: int
            The number of entities retrieved in each request

        Returns
        -------
        list[Entity]
            Retrieved a generator of entities (matching the given type and/or query string)

        Example
        -------
        >>> with AsyncClient() as client:
        >>>     async for entity in await client.query_handle(type="AgriFarm"):
                    print(entity)
        """
        count = await self.entities.count(type, q, gq)
        for page in range(ceil(count / limit)):
            entities = await self.entities._query(type, q, gq, ctx, limit, page * limit)
            if batch:
                yield entities
            else:
                for entity in entities:
                    yield entity

    async def query_handle(
        self,
        type: str = None,
        q: str = None,
        gq: str = None,
        ctx: str = None,
        limit: int = PAGINATION_LIMIT_MAX,
        *,
        callback: Callable[[Entity], None],
    ) -> None:
        """Apply a callback function on entity of the query result.

        Parameters
        ----------
        etype : str
            The entity's type
        q: str
            The query string (NGSI-LD Query Language)
        gq: str
            The geoquery string (NGSI-LD Geoquery Language)
        ctx: str
            The context
        limit: int
            The number of entities retrieved in each request
        callback: Callable[Entity]
            The function to be called on each entity of the result

        Example
        -------
        >>> with AsyncClient() as client:
        >>>     await client.query_handle(type="AgriFarm", lambda e: print(e))
        """
        async for entity in self.query_generator(type, q, gq, ctx, limit, False):
            callback(entity)

    async def count(self, type: str = None, q: str = None, gq: str = None) -> int:
        """Return number of entities matching type and/or query string.

        Facade method for Entities.count().

        Parameters
        ----------
        etype : str
            The entity's type
        q: str
            The query string (NGSI-LD Query Language)
        gq: str
            The geoquery string (NGSI-LD Geoquery Language)

        Returns
        -------
        int
            The number of matching entities

        Example
        -------
        >>> with AsyncClient() as client:
        >>>     await client.count(type="AgriFarm") # match a given type

        >>> with AsyncClient() as client:
        >>>     await client.count(type="AgriFarm", query='contactPoint[email]=="wheatfarm@email.com"') # match type and query
        """
        return await self.entities.count(type, q)

    async def delete_where(self, type: str = None, q: str = None, **kwargs):
        """Batch delete entities matching type and/or query string.

        Parameters
        ----------
        etype : str
            The entity's type
        query: str
            The query string (NGSI-LD Query Language)

        Example
        -------
        >>> with AsyncClient() as client:
        >>>     await client.delete_where(type="AgriFarm", query='contactPoint[email]=="wheatfarm@email.com"') # match type and query
        """
        g = self.query_generator(type, q, batch=True, **kwargs)
        async for batch in g:
            await self.batch.delete(batch)

    async def drop(self, *types: str) -> None:
        """Batch delete entities matching the given type.

        Parameters
        ----------
        type : str
            The entity's type

        Example
        -------
        >>> with AsyncClient() as client:
        >>>     await client.drop("AgriFarm")
        """
        for t in types:
            await self.delete_where(type=t)

    async def purge(self) -> None:
        """Batch delete all entities.

        Example
        -------
        >>> with AsyncClient() as client:
        >>>     await client.purge()
        """
        for type in await self.types.list():
            await self.drop(type)

    async def flush_all(self) -> None:
        """Batch delete all entities and remove all contexts.

        Example
        -------
        >>> with AsyncClient() as client:
        >>>     await client.purge()
        """
        await self.purge(type)
        await self.contexts.cleanup()

    # below the context manager methods

    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback):
        await self.close()
