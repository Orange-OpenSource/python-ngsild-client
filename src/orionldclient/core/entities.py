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

from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from requests import Response

if TYPE_CHECKING:
    from .client import Client

from .constants import *
from .exceptions import NgsiApiError, rfc7807_error_handle
from ..model.entity import Entity


logger = logging.getLogger(__name__)


class Entities:
    def __init__(self, client: Client, url: str):
        self._client = client
        self._session = client.session
        self.url = url

    #@rfc7807_error_handle
    def create(self, entity: Entity) -> Entity:
        #logger.info(f"{self._session.headers}")
        r = self._session.post(
            f"{self.url}/",
            entity.to_json(),
        )
        self._client.raise_for_status(r)
        location = r.headers.get("Location")
        if location is None:
            if self._client.ignore_errors:
                return None
            else:
                raise NgsiApiError("Missing Location header")
        logger.info(f"{r.status_code=}")
        logger.info(f"{location=}")
        id_returned_from_broker = location.rsplit("/", 1)[-1]
        if entity.id != id_returned_from_broker:
            raise NgsiApiError(
                f"Broker returned wrong id. Expected={entity.id} Returned={id_returned_from_broker}"
            )
        return entity

    @rfc7807_error_handle
    def retrieve(self, eid: Union[EntityId, Entity], asdict: bool = False, **kwargs) -> Entity:
        eid = eid.id if isinstance(eid, Entity) else eid
        r = self._session.get(f"{self.url}/{eid}", **kwargs)
        self._client.raise_for_status(r)
        return r.json() if asdict else Entity.from_dict(r.json())

    # def exists(self, eid: EntityId) -> bool:
    #     params = {"id": eid, "limit": 0, "count": "true"}
    #     linkheader = f'<https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    #     return api.get(self._session, f"{self.url}", headers={"Link": linkheader}, params=params)

    @rfc7807_error_handle
    def exists(self, eid: Union[EntityId, Entity]) -> bool:
        eid = eid.id if isinstance(eid, Entity) else eid
        r = self._session.get(f"{self.url}/{eid}")
        if r:
            payload = r.json()
            return "@context" in payload
        return False

    @rfc7807_error_handle
    def delete(self, eid: Union[EntityId, Entity]) -> bool:
        eid = eid.id if isinstance(eid, Entity) else eid
        logger.info(f"{eid=}")
        logger.info(f"url={self.url}/{eid}")
        r = self._session.delete(f"{self.url}/{eid}")
        logger.info(f"requests: {r.request.url}")
        self._client.raise_for_status(r)
        return bool(r)
