#!/usr/bin/env python3

# Software Name: python-orion-client
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battelo@orange.com> et al.
# SPDX-License-Identifier: Apache-2.0

import logging

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client

#from. import api
import requests

from .constants import *
from ..model.entity import Entity


logger = logging.getLogger(__name__)


class Entities:
    def __init__(self, client: "Client", url: str):
        self._client = client
        self._session = client.session
        self.url = url

    def create(self, entity: Entity) -> EntityId:
        logger.info(f"{self._session.headers}")
        r = self._session.post(
            f"{self.url}/",
            entity.to_json(),
        )
        r.raise_for_status()
        location = r.headers.get("Location")
        logger.info(f"{r.status_code=}")
        logger.info(f"{location=}")
        return location.rsplit("/", 1)[-1]

    def retrieve(self, eid: EntityId, **kwargs) -> Entity:
        r = self._session.get(f"{self.url}/{eid}", **kwargs)
        r.raise_for_status()
        return Entity.from_dict(r.json())

    # def exists(self, eid: EntityId) -> bool:
    #     params = {"id": eid, "limit": 0, "count": "true"}
    #     linkheader = f'<https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    #     return api.get(self._session, f"{self.url}", headers={"Link": linkheader}, params=params)

    def exists(self, eid: EntityId) -> bool:
        r = self._session.get(f"{self.url}/{eid}")
        if r:
            payload = r.json()
            return "@context" in payload
        return False

    def delete(self, eid: Union[EntityId, Entity]) -> bool:
        eid = eid.id if isinstance(id, Entity) else eid
        r = self._session.delete(f"{self.url}/{eid}")
        return bool(r)

