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

from typing import TYPE_CHECKING, Optional, Tuple, Generator, List, Sequence, Union, Callable, Set

if TYPE_CHECKING:
    from ngsildclient.model.constants import EntityOrId

import logging
import requests
from requests.auth import AuthBase
from dataclasses import dataclass
from math import ceil
import networkx as nx

from ngsildclient import __version__ as __version__
from ..utils import is_interactive
from ..utils.urn import Urn
from ..model.entity import Entity
from .constants import *
from .entities import Entities
from .batch import Batch, BatchResult
from .types import Types
from .contexts import Contexts
from .subscriptions import Subscriptions
from .temporal import Temporal
from .alt import Alt
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
        custom_auth: AuthBase = None,
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
            if set tests the connection at init time and raises an exception if failed, by default False
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
        self.url_temporal = f"{self.scheme}://{hostname}:{port_temporal}"

        self.session = requests.Session()
        if custom_auth:
            self.session.auth = custom_auth
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

        self._entities = Entities(self, f"{self.url}/{ENDPOINT_ENTITIES}", f"{self.url}/{ENDPOINT_ALT_QUERY_ENTITIES}")
        self._batch = Batch(self, f"{self.url}/{ENDPOINT_BATCH}")
        self._types = Types(self, f"{self.url}/{ENDPOINT_TYPES}")
        self._contexts = Contexts(self, f"{self.url}/{ENDPOINT_CONTEXTS}")
        self._subscriptions = Subscriptions(self, f"{self.url}/{ENDPOINT_SUBSCRIPTIONS}")
        self._temporal = Temporal(self, f"{self.url_temporal}/{ENDPOINT_TEMPORAL}", f"{self.url_temporal}/{ENDPOINT_ALT_QUERY_TEMPORAL}")
        self._alt = Alt(self)
        self.broker = Broker(Vendor.UNKNOWN, "N/A")

        # get status and retrieve Context Broker information
        status = self.is_connected(raise_for_disconnected=True)
        if status:
            self.broker = Broker(*self.guess_vendor())
            if is_interactive():
                print(self._welcome_message())
        else:
            if is_interactive():
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
                raise NgsiNotConnectedError(f"Cannot connect to Context Broker at {self.hostname}:{self.port}: {e}")
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

    @property
    def temporal(self):
        return self._temporal

    @property
    def alt(self):
        return self._alt        

    def close(self):
        """Terminates the client.

        Closes the underlying Requests.Session.
        """
        self.session.close()

    def create(self, *entities) -> Union[bool, BatchResult]:
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
                return self.entities.create(entity)
            else:
                entities = entities[0]
        return self.batch.create(entities)


    def get(
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
        return self.entities.get(entity, ctx, asdict, **kwargs)

    def delete(self, *entities) -> Union[bool, BatchResult]:
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
                return self.entities.delete(entity)
            else:
                entities = entities[0]
        return self.batch.delete(entities)            

    def delete_from_file(self, filename: str) -> Union[bool, BatchResult]:
        """Delete in the broker all entities present in the JSON file.

        Parameters
        ----------
        filename : str
            Points to the JSON input file that contains entities.
        """
        entities = Entity.load(filename)
        return self.delete(entities)

    def exists(self, entity: EntityOrId) -> bool:
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
        return self.entities.exists(entity)

    def upsert(self, *entities) -> Union[bool, BatchResult]:
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
                return self.entities.upsert(entity)
            else:
                entities = entities[0]
        return self.batch.upsert(entities)

    def bulk_import(self, filename: str) -> Union[bool, dict]:
        """Upsert all entities from a JSON file.

        Parameters
        ----------
        filename : str
            Points to the JSON input file that contains entities.
        """
        entities = Entity.load(filename)
        return self.upsert(entities)

    def update(self, *entities) -> Union[bool, BatchResult]:
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
                return self.entities.update(entity)
            else:
                entities = entities[0]
        return self.batch.update(entities)

    def query_head(self, type: str = None, q: str = None, gq: str = None, ctx: str = None, n: int = 5) -> List[Entity]:
        """Retrieve entities given its type and/or query string.

        Retrieve up to PAGINATION_LIMIT_MAX entities.
        Use query() to retrieve all entities.
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
        >>> with Client() as client:
        >>>     client.query(type="AgriFarm") # match a given type

        >>> with Client() as client:
        >>>     client.query(type="AgriFarm", q='contactPoint[email]=="wheatfarm@email.com"') # match type and query
        """
        return self.entities._query(type, q, gq, ctx, limit=n)

    def query(
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
        >>> with Client() as client:
        >>>     client.query(type="AgriFarm") # match a given type

        >>> with Client() as client:
        >>>     client.query(type="AgriFarm", q='contactPoint[email]=="wheatfarm@email.com"') # match type and query
        """

        entities: list[Entity] = []
        count = self.entities.count(type, q, gq, ctx=ctx)
        if count > max:
            raise NgsiClientTooManyResultsError(f"{count} results exceed maximum {max}")
        for page in range(ceil(count / limit)):
            entities.extend(self.entities._query(type, q, gq, ctx, limit, page * limit))
        return entities

    def query_generator(
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
        >>> with Client() as client:
        >>>     for entity in client.query_handle(type="AgriFarm"):
                    print(entity)
        """
        count = self.entities.count(type, q)
        for page in range(ceil(count / limit)):
            if batch:
                yield self.entities._query(type, q, gq, ctx, limit, page * limit)
            else:
                yield from self.entities._query(type, q, gq, ctx, limit, page * limit)

    def query_handle(
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
        >>> with Client() as client:
        >>>     client.query_handle(type="AgriFarm", lambda e: print(e))
        """
        for entity in self.query_generator(type, q, gq, ctx, limit, False):
            callback(entity)

    def count(self, type: str = None, q: str = None, gq: str = None) -> int:
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
        >>> with Client() as client:
        >>>     client.count(type="AgriFarm") # match a given type

        >>> with Client() as client:
        >>>     client.count(type="AgriFarm", query='contactPoint[email]=="wheatfarm@email.com"') # match type and query
        """
        return self.entities.count(type, q, gq)

    def delete_where(self, type: str = None, q: str = None, gq: str = None):
        """Batch delete entities matching type and/or query string.

        Parameters
        ----------
        etype : str
            The entity's type
        q: str
            The query string (NGSI-LD Query Language)
        gq: str
            The geoquery string (NGSI-LD Geoquery Language)

        Example
        -------
        >>> with Client() as client:
        >>>     client.delete_where(type="AgriFarm", query='contactPoint[email]=="wheatfarm@email.com"') # match type and query
        """
        g = self.query_generator(type, q, gq, batch=True)
        for batch in g:
            self.batch.delete(batch)

    def drop(self, *types: str) -> None:
        """Batch delete entities matching the given type.

        Parameters
        ----------
        type : str
            The entity's type

        Example
        -------
        >>> with Client() as client:
        >>>     client.drop("AgriFarm")
        """
        for t in types:
            self.delete_where(type=t)

    def purge(self) -> None:
        """Batch delete all entities.

        Example
        -------
        >>> with Client() as client:
        >>>     client.purge()
        """
        for type in self.types.list():
            self.drop(type)

    def flush_all(self) -> None:
        """Batch delete all entities and remove all contexts.

        Example
        -------
        >>> with Client() as client:
        >>>     client.purge()
        """
        self.purge(type)
        self.contexts.cleanup()

    def guess_vendor(self) -> tuple[Vendor, Version]:
        """Try to guess the Context Broker vendor.

        According to its own API, by using version or status endpoint.

        Returns
        -------
        tuple[Vendor, Version]
            A tuple composed of the Vendor (if identified) and the version.

        Example
        -------
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
                print("Java-Spring based Context Broker detected. Try to enable info endpoint.")
            return None

    def _welcome_message(self) -> str:
        return f"Connected to Context Broker at {self.hostname}:{self.port} | vendor={self.broker.vendor.value} | version={self.broker.version}"

    def _fail_message(self) -> str:
        return f"Failed to connect to Context Broker at {self.hostname}:{self.port}"

    def _warn_spring_message(self) -> str:
        return "Java-Spring based Context Broker detected. Info endpoint disabled."

    def _create_network(self, root: Entity, G: nx.Graph, nodecache: dict, edgecache: Set):
        source: Tuple = Urn.split(root.id)
        for _, nodeid in root.relationships:
            target: Tuple = Urn.split(nodeid)
            if (source,target) in edgecache or (target,source) in edgecache:
                continue
            edgecache.add((source, target))
            G.add_edge(source, target)
            logger.debug(f"cache lookup : {nodeid}")
            entity = nodecache.get(nodeid)
            logger.debug(f"{entity=}")
            if entity is None: # cache miss
                try:
                    entity = self.get(nodeid)
                    nodecache[nodeid] = entity
                except NgsiResourceNotFoundError:
                    pass
            G = self._create_network(entity, G, nodecache, edgecache)
        return G

    def network(self, root: Entity):
        G = nx.Graph()
        nodecache: dict[str, Entity] = {} # hash table
        edgecache: Set[Tuple[str,str]] = set() # membership testing
        return self._create_network(root, G, nodecache, edgecache)

    # below the context manager methods

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
