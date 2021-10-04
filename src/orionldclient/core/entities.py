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

from .constants import *
from .http import *
from ..model.entity import Entity
from ..model.ngsidict import NgsiDict


logger = logging.getLogger(__name__)


class Entities:
    def __init__(self, client: "Client", url: str):
        self._client = client
        self._session = client.session
        self.url = url

    def create(self, entity: Entity) -> EntityId:
        payload = entity.to_json()
        logger.info(f"{self._session.headers}")
        location = post(
            self._session,
            f"{self.url}/",
            payload,
            # headers={"Content-Type": "application/ld+json", "Accept": None},
        )
        logger.debug(f"{location=}")
        return location.rsplit("/", 1)[-1]

    def retrieve(self, id: EntityId) -> Entity:
        payload = get(self._session, f"{self.url}/{id}")
        return Entity.from_dict(payload)

    def exists(self, id: EntityId) -> bool:
        return False

    def delete(self, id: Union[EntityId, Entity]):
        id = id.id if isinstance(id, Entity) else id
        pass
