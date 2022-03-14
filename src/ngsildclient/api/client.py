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
import requests
from dataclasses import dataclass
from typing import Optional, Tuple, Generator, overload
from math import ceil

from ..utils import is_interactive
from ..model.entity import Entity
from .constants import *
from .entities import Entities
from .batch import BatchOp
from .types import Types
from .contexts import Contexts
from .subscriptions import Subscriptions
from .exceptions import *

logger = logging.getLogger(__name__)

"""This module contains the definition of the Client class.
"""


@dataclass
class Broker:
    """Represent a NGSI-LD Context Broker."""

    vendor: Vendor = Vendor.UNKNOWN
    version: str = "N/A"


class Client:
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

        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": self.useragent,
            "Accept": "application/ld+json",
            "Content-Type": "application/ld+json",
        }
        if tenant is not None:
            self.session.headers["NGSILD-Tenant"] = tenant
        if proxy:
            self.session.proxies = {proxy}

        logger.info("Connecting client ...")

        self._entities = Entities(self, f"{self.url}/{ENDPOINT_ENTITIES}")
        self._batch = BatchOp(self, f"{self.url}/{ENDPOINT_BATCH}")
        self._types = Types(self, f"{self.url}/{ENDPOINT_TYPES}")
        self._contexts = Contexts(self, f"{self.url}/{ENDPOINT_CONTEXTS}")
        self._subscriptions = Subscriptions(
            self, f"{self.url}/{ENDPOINT_SUBSCRIPTIONS}"
        )

        self.broker = Broker(Vendor.UNKNOWN, "N/A")

        # get status and retrieve Context Broker information
        status = self.is_connected(raise_for_disconnected=True)
        if status and is_interactive():
            self.broker = Broker(*self.guess_vendor())
            print(self._welcome_message())
        else:
            print(self._fail_message())

    def raise_for_status(self, r: Response):
        """Raises an exception depending on the API response.

        Parameters
        ----------
        r : Response
            Response from the Context Broker
        """
        if not self.ignore_errors:
            r.raise_for_status()

    def is_connected(self, raise_for_disconnected=False) -> bool:
        """Test if connection to Context Broker is established.

        Send a valid test request to the Context Broker and expects a result.

        Parameters
        ----------
        raise_for_disconnected : bool, optional
            throw an exception if connection fails (if not set only return False), by default False

        Returns
        -------
        bool
            True if the Context Broker replies

        Raises
        ------
        NgsiNotConnectedError
        """
        url = f"{self.url}/{ENDPOINT_ENTITIES}"
        params = {"type": "None", "limit": 0, "count": "true"}
        try:
            r = self.session.get(
                url,
                headers={
                    "Accept": "application/json",
                    "Content-Type": None,
                },  # overrides session headers
                params=params,
            )
            r.raise_for_status()
        except Exception as e:
            if is_interactive():
                return False
            if raise_for_disconnected:
                raise NgsiNotConnectedError(
                    f"Cannot connect to Context Broker at {self.hostname}:{self.port}: {e}"
                )
            else:
                logger.error(e)
                return False
        return True

    @property
    def version(self) -> str:
        return __version__

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

    def close(self):
        """Terminates the client.

        Closes the underlying Requests.Session.
        """
        self.session.close()

    @overload
    def create(
        self, entity: Entity, skip: bool = False, overwrite: bool = False
    ) -> Entity:
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
    def create(
        self, entities: List[Entity], skip: bool = False, overwrite: bool = False
    ):
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

    def create(
        self,
        _entities: Union[Entity, List[Entity]],
        skip: bool = False,
        overwrite: bool = False,
    ) -> Optional[Entity]:
        if isinstance(_entities, Entity):
            entity = _entities
            return self.entities.create(entity, skip, overwrite)
        else:
            return self.batch.create(_entities, skip, overwrite)

    def get(
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
        return self.entities.get(eid, ctx, asdict, **kwargs)

    @overload
    def delete(self, eid: Union[EntityId, Entity]) -> bool:
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
    def delete(self, eids: List[Union[EntityId, Entity]]) -> bool:
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

    def delete(
        self, eids: Union[Union[EntityId, Entity], List[Union[EntityId, Entity]]]
    ) -> bool:
        if isinstance(eids, list):
            return self.batch.delete(eids)
        else:
            eid = eids
            return self.entities.delete(eid)

    def exists(self, eid: Union[EntityId, Entity]) -> bool:
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
        return self.entities.exists(eid)

    @overload
    def upsert(self, entity: Entity) -> Entity:
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
    def upsert(self, entities: List[Entity]) -> dict:
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

    def upsert(self, entities: Union[Entity, List[Entity]]) -> Union[Entity, dict]:
        if isinstance(entities, Entity):
            entity = entities
            return self.entities.upsert(entity)
        else:
            return self.batch.upsert(entities)

    @overload
    def update(self, entity: Entity) -> Optional[Entity]:
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
        return self.entities.update(entity)

    @overload
    def update(self, entities: List[Entity]) -> dict:
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

    def update(
        self, entities: Union[Entity, List[Entity]]
    ) -> Union[Optional[Entity], dict]:
        if isinstance(entities, Entity):
            entity = entities
            return self.entities.update(entity)
        else:
            return self.batch.update(entities)

    def query(
        self, type: str = None, q: str = None, ctx: str = None, **kwargs
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
        ctx : str
            The context
        Returns
        -------
        list[Entity]
            Retrieved entities matching the given type and/or query string

        Example:
        --------
        >>> with Client() as client:
        >>>     client.query(type="AgriFarm") # match a given type

        >>> with Client() as client:
        >>>     client.query(type="AgriFarm", q='contactPoint[email]=="wheatfarm@email.com"') # match type and query
        """
        return self.entities.query(type, q, ctx, limit=PAGINATION_LIMIT_MAX)

    def query_all(
        self,
        type: str = None,
        q: str = None,
        ctx: str = None,
        limit: int = PAGINATION_LIMIT_MAX,
        **kwargs,
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
        ctx: str
            The context
        limit: int
            The number of entities retrieved in each request

        Returns
        -------
        list[Entity]
            Retrieved entities matching the given type and/or query string

        Example:
        --------
        >>> with Client() as client:
        >>>     client.query_all(type="AgriFarm") # match a given type

        >>> with Client() as client:
        >>>     client.query_all(type="AgriFarm", q='contactPoint[email]=="wheatfarm@email.com"') # match type and query
        """

        entities: list[Entity] = []
        count = self.entities.count(type, q)
        for page in range(ceil(count / limit)):
            entities.extend(self.entities.query(type, q, ctx, limit, page * limit))
        return entities

    def query_generator(
        self,
        type: str = None,
        q: str = None,
        ctx: str = None,
        limit: int = PAGINATION_LIMIT_MAX,
        **kwargs,
    ) -> Generator[Entity, None, None]:
        count = self.entities.count(type, q)
        for page in range(ceil(count / limit)):
            yield from self.entities.query(type, q, ctx, limit, page * limit)

    def count(self, type: str = None, q: str = None, **kwargs) -> int:
        """Return number of entities matching type and/or query string.

        Facade method for Entities.count().

        Parameters
        ----------
        etype : str
            The entity's type
        query: str
            The query string (NGSI-LD Query Language)

        Returns
        -------
        int
            The number of matching entities

        Example:
        --------
        >>> with Client() as client:
        >>>     client.count(type="AgriFarm") # match a given type

        >>> with Client() as client:
        >>>     client.count(type="AgriFarm", query='contactPoint[email]=="wheatfarm@email.com"') # match type and query
        """
        return self.entities.count(type, q)

    def delete_where(
        self, type: str = None, q: str = None, **kwargs
    ) -> tuple[bool, dict]:
        """Batch delete entities matching type and/or query string.

        Parameters
        ----------
        etype : str
            The entity's type
        query: str
            The query string (NGSI-LD Query Language)

        Example:
        --------
        >>> with Client() as client:
        >>>     client.delete_where(type="AgriFarm", query='contactPoint[email]=="wheatfarm@email.com"') # match type and query
        """
        entities = self.query_all(type, q, **kwargs)
        return self.batch.delete(entities)

    def drop(self, type: str) -> None:
        """Batch delete entities matching the given type.

        Parameters
        ----------
        type : str
            The entity's type

        Example:
        --------
        >>> with Client() as client:
        >>>     client.drop("AgriFarm")
        """
        self.delete_where(type=type)

    def purge(self) -> None:
        """Batch delete all entities.

        Example:
        --------
        >>> with Client() as client:
        >>>     client.purge()
        """
        for type in self.types.list():
            self.drop(type)

    def guess_vendor(self) -> tuple[Vendor, Version]:
        """Try to guess the Context Broker vendor.

        According to its own API, by using version or status endpoint.

        Returns
        -------
        tuple[Vendor, Version]
            A tuple composed of the Vendor (if identified) and the version.

        Example:
        --------
        >>> with Client() as client:
        >>>     print(client.guess_vendor())
        (<Vendor.ORIONLD: 'Orion-LD'>, 'post-v0.8.1')
        """
        if broker := self._broker_version_orionld():
            return broker
        if broker := self._broker_version_java_spring():
            return broker
        return Vendor.UNKNOWN, "N/A"

    def _broker_version_orionld(self) -> Optional[str]:
        """Requests the broker looking for Orion-LD version.

        Targets the /version endpoint.

        Returns
        -------
        Optional[str]
            The Orion-LD version if found
        """
        url = f"{self.url}/version"
        headers = {
            "Accept": "application/json",
            "Content-Type": None,
        }  # overrides session headers
        try:
            r = self.session.get(url, headers=headers)
            r.raise_for_status()
            return Vendor.ORIONLD, r.json()["orionld version"]
        except Exception:
            return None

    def _broker_version_java_spring(self) -> Optional[Tuple[Vendor, str]]:
        """Requests the Java-Spring based broker looking for Vendor and Version.

        Targets the /actuator/info endpoint.

        Returns
        -------
        Optional[Tuple[Vendor, str]]
            A tuple composed of the Vendor and the broker version
        """
        url = f"{self.url}/actuator"
        headers = {
            "Accept": "application/json",
            "Content-Type": None,
        }  # overrides session headers
        try:
            r = self.session.get(f"{url}/health", headers=headers)
            r.raise_for_status()
        except Exception:
            return None
        try:
            r = self.session.get(f"{url}/info", headers=headers)
            r.raise_for_status()
            build = r.json()["build"]
            version = build["version"]
            group = build["group"]
            if group == "eu.neclab.ngsildbroker":
                vendor = Vendor.SCORPIO
            elif group == "com.egm.stellio":
                vendor = Vendor.STELLIO
            else:
                return None
            return vendor, version
        except Exception:
            if is_interactive():
                print(
                    "Java-Spring based Context Broker detected. Try to enable info endpoint."
                )
            return None

    def _welcome_message(self) -> str:
        return f"Connected to Context Broker at {self.hostname}:{self.port} | vendor={self.broker.vendor.value} | version={self.broker.version}"

    def _fail_message(self) -> str:
        return f"Failed to connect to Context Broker at {self.hostname}:{self.port}"

    def _warn_spring_message(self) -> str:
        return "Java-Spring based Context Broker detected. Info endpoint disabled."

    # below the context manager methods

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
