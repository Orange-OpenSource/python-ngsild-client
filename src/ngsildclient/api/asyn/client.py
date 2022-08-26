#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import logging
import httpx
from httpx._types import AuthTypes
from dataclasses import dataclass
from typing import Optional, Tuple, Generator, List, Union, overload
from math import ceil

from ...model.entity import Entity
from ..constants import *
from ..exceptions import *
from .entities import Entities
from .batch import BatchOp
from .types import Types
from .contexts import Contexts
from .subscriptions import Subscriptions

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

    Example:
    --------
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
        self._batch = BatchOp(self, f"{self.url}/{ENDPOINT_BATCH}")
        self._types = Types(self, f"{self.url}/{ENDPOINT_TYPES}")
        self._contexts = Contexts(self, f"{self.url}/{ENDPOINT_CONTEXTS}")
        self._subscriptions = Subscriptions(self, f"{self.url}/{ENDPOINT_SUBSCRIPTIONS}")

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

    async def close(self):
        """Terminates the client.

        Closes the underlying httpx.AsyncClient.
        """
        await self.client.aclose()

    @overload
    async def create(self, entity: Entity, skip: bool = False, overwrite: bool = False) -> Entity:
        """Create an entity.

        Facade method for Entities.create().

        Parameters
        ----------
        entity : Entity
            the entity to be created by the Context Broker
        skip : bool, optional
            if set, skips creation (do nothing) if already exists, by default False
        overwrite : bool, optional
            if set, force upsert the entity if already exists, by default False

        Returns
        -------
        Entity
            the entity succesfully created
        """
        ...

    @overload
    async def create(self, entities: List[Entity], skip: bool = False, overwrite: bool = False):
        """Create a batch of entities.

        Facade method for Batch.create().

        Parameters
        ----------
        entities : List[Entity]
            the entity to be created by the Context Broker
        skip : bool, optional
            if set, skips creation (do nothing) if already exists, by default False
        overwrite : bool, optional
            if set, force upsert the entity if already exists, by default False

        Returns
        -------
        BatchOperationResult
            TODO
        """
        ...

    async def create(
        self,
        _entities: Union[Entity, List[Entity]],
        skip: bool = False,
        overwrite: bool = False,
    ) -> Optional[Entity]:
        if isinstance(_entities, Entity):
            entity = _entities
            return await self.entities.create(entity, skip, overwrite)
        else:
            return await self.batch.create(_entities, skip, overwrite)

    async def get(
        self,
        eid: Union[EntityId, Entity],
        ctx: str = None,
        asdict: bool = False,
        **kwargs,
    ) -> Entity:
        """Retrieve an entity given its id.

        Facade method for Entities.retrieve().
        If already dealing with an entity instance one can provide the entity itself instead of its id.

        Parameters
        ----------
        eid : Union[EntityId, Entity]
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
        return await self.entities.get(eid, ctx, asdict, **kwargs)

    @overload
    async def delete(self, eid: Union[EntityId, Entity]) -> bool:
        """Delete an entity given its id.

        Facade method for Entities.delete().
        If already dealing with an entity instance one can provide the entity itself instead of its id.

        Parameters
        ----------
        eid : Union[EntityId, Entity]
            The entity identifier or the entity instance

        Returns
        -------
        bool
            True if the entity has been succefully deleted
        """
        ...

    @overload
    async def delete(self, eids: List[Union[EntityId, Entity]]) -> bool:
        """Delete entities given its id.

        Facade method for Batch.delete().
        If already dealing with entity instances one can provide the entities instead of ids.

        Parameters
        ----------
        eids : List[Union[EntityId, Entity]]
            The entities ids or instances

        Returns
        -------
        bool
            True if the entity has been succefully deleted
        """
        ...

    async def delete(self, eids: Union[Union[EntityId, Entity], List[Union[EntityId, Entity]]]) -> bool:
        if isinstance(eids, list):
            return await self.batch.delete(eids)
        else:
            eid = eids
            return await self.entities.delete(eid)

    async def delete_from_file(self, filename: str) -> Union[Entity, dict]:
        """Delete in the broker all entities present in the JSON file.

        Parameters
        ----------
        filename : str
            Points to the JSON input file that contains entities.
        """
        entities = await Entity.load_async(filename)
        return await self.delete(entities)

    async def exists(self, eid: Union[EntityId, Entity]) -> bool:
        """Tests if an entity exists.

        Facade method for Entities.exists().
        If already dealing with an entity instance one can provide the entity itself instead of its id.

        Parameters
        ----------
        eid : Union[EntityId, Entity]
            The entity identifier or the entity instance

        Returns
        -------
        bool
            True if the entity exists
        """
        return await self.entities.exists(eid)

    @overload
    async def upsert(self, entity: Entity) -> Entity:
        """Upsert the entity or update it if already exists.

        Facade method for Entities.upsert().

        Parameters
        ----------
        entity : Entity
            The entity to be upserted by the Context Broker

        Returns
        -------
        Entity
            The entity successfully upserted
        """
        ...

    @overload
    async def upsert(self, entities: List[Entity]) -> dict:
        """Upsert a batch of entities.

        Facade method for Batch.upsert().

        Parameters
        ----------
        entity : Entity
            The entity to be upserted by the Context Broker

        Returns
        -------
        Entity
            The entities successfully upserted
        """
        ...

    async def upsert(self, entities: Union[Entity, List[Entity]]) -> Union[Entity, dict]:
        if isinstance(entities, Entity):
            entity = entities
            return await self.entities.upsert(entity)
        else:
            return await self.batch.upsert(entities)

    async def bulk_import(self, filename: str) -> Union[Entity, dict]:
        """Upsert all entities from a JSON file.

        Parameters
        ----------
        filename : str
            Points to the JSON input file that contains entities.
        """
        entities = await Entity.load_async(filename)
        return await self.upsert(entities)

    @overload
    async def update(self, entity: Entity) -> Optional[Entity]:
        """Update the entity.

        Facade method for Entities.update().

        Parameters
        ----------
        entity : Entity
            The entity to be updated by the Context Broker

        Returns
        -------
        Optional[Entity]
            The entity successfully updated (or None if not found)
        """
        ...

    @overload
    async def update(self, entities: List[Entity]) -> dict:
        """Update a batch of entities.

        Facade method for Batch.update().

        Parameters
        ----------
        entities : List[Entity]
            The entities to be updated by the Context Broker

        Returns
        -------
        Optional[Entity]
            The entity successfully updated (or None if not found)
        """
        ...

    async def update(self, entities: Union[Entity, List[Entity]]) -> Union[Optional[Entity], dict]:
        if isinstance(entities, Entity):
            entity = entities
            return await self.entities.update(entity)
        else:
            return await self.batch.update(entities)

    # below the context manager methods

    async def __aenter__(self):
        return self

    async def __aexit__(self, type, value, traceback):
        await self.close()