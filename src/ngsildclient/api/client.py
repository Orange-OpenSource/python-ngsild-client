#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.
# SPDX-License-Identifier: Apache-2.0

import logging
from dataclasses import dataclass
from typing import Optional

import requests

from ..model.entity import Entity
from .constants import *
from .entities import Entities
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

    It allows to connect to a NGSI-LD Context Broker, check the connection and try to identify the vendor.
    As for now it focuses on the /entities/{entityId} endpoint.
    Allowed operations are :
    - create(), update(), upsert()
    - retrieve(), exists()
    - delete()

    Update() and upsert() operations are not atomic, as they aren't provided as-is by the API, but require chaining 2 API calls.

    When encountering errors the Client throws enriched Exceptions, as NGSI-LD API supports ProblemDetails [IETF RFC 7807].

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

        The Client allows to retrieve or send entities (model.Entity instances) to the Context Broker.
        For example, one can retrieve an entity from the Context Broker, modify it (update/delete/add properties),
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
        self._subscriptions = (
            None  # TODO : create Subscriptions class and implement subscription stuff
        )

        # get status and retrieve Context Broker information
        status = self.is_connected(raise_for_disconnected=True)
        if status:
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
    def subscriptions(self):
        return self._subscriptions

    def close(self):
        """Terminates the client.

        Closes the underlying Requests.Session.
        """
        self.session.close()

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
        return self.entities.create(entity, skip, overwrite)

    def retrieve(
        self, eid: Union[EntityId, Entity], asdict: bool = False, **kwargs
    ) -> Entity:
        """Retrieve an entity given its id.

        Facade method for Entities.retrieve().
        If already dealing with an entity instance one can provide the entity itself instead of its id.

        Parameters
        ----------
        eid : Union[EntityId, Entity]
            The entity identifier or the entity instance
        asdict : bool, optional
            If set (instead of returning an Entity) returns the raw API response (a Python dict that represents the JSON response), by default False

        Returns
        -------
        Entity
            The retrieved entity
        """
        return self.entities.retrieve(eid)

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

    def upsert(self, entity: Entity) -> Entity:
        """Create the entity or update it if already exists.

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
        return self.entities.upsert(entity)

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
        if version := self._broker_version_orionld():
            return Vendor.ORIONLD, version
        if version := self._broker_version_scorpio():
            return Vendor.SCORPIO, version
        if version := self._broker_version_stellio():
            return Vendor.STELLIO, version
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
            return r.json()["orionld version"]
        except Exception:
            return None

    def _broker_version_scorpio(self) -> Optional[str]:
        """Requests the broker looking for Scorpio version.

        Targets the /health endpoint.
        No /version endpoint as for now.

        Returns
        -------
        Optional[str]
            "N/A" if the broker is Scorpio else None
        """
        url = f"{self.url}/scorpio/v1/info/health"
        headers = {
            "Accept": "application/json",
            "Content-Type": None,
        }  # overrides session headers
        try:
            r = self.session.get(url, headers=headers)
            r.raise_for_status()
            return "N/A"
        except Exception:
            return None

    def _broker_version_stellio(self) -> Optional[str]:
        """Requests the broker looking for Stellio version.

        Targets the /actuator/health endpoint.
        No /version endpoint as for now.

        Returns
        -------
        Optional[str]
            "N/A" if the broker is Stellio else None
        """
        url = f"{self.url}/actuator/health"
        headers = {
            "Accept": "application/json",
            "Content-Type": None,
        }  # overrides session headers
        try:
            r = self.session.get(url, headers=headers)
            r.raise_for_status()
            return "N/A"
        except Exception:
            return None

    def _broker_version_cassiopeia(self) -> Optional[str]:
        """Requests the broker looking for Cassiopeia version.

        Raises
        ------
        NotImplemented
        """
        raise NotImplementedError

    def _welcome_message(self) -> str:
        return f"Connected to Context Broker at {self.hostname}:{self.port} | vendor={self.broker.vendor.value} version={self.broker.version}"

    def _fail_message(self) -> str:
        return f"Failed to connect to Context Broker at {self.hostname}:{self.port}"

    # below the context manager methods

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
