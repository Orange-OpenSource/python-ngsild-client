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

from typing import TYPE_CHECKING, Union, Callable, Any, List, Tuple, Optional
from datetime import timedelta

if TYPE_CHECKING:
    from .client import Client
    from .constants import EntityId

from .constants import *
from .http import *
from ..model.entity import Entity


logger = logging.getLogger(__name__)


class Entities:
    def __init__(self, client: "Client", url: str):
        self._client = client
        self.url = url

    @property
    def session(self):
        return self._client.session

    def create(self, entity: Entity) -> 'EntityId':
        payload = entity.to_json()
        logger.info(f"{self.session.headers}")
        location = post(
            self.session,
            f"{self.url}/",
            payload,
            headers={"Content-Type": "application/ld+json", "Accept": None},
        )
        logger.debug(f"{location=}")
        return location.rsplit("/", 1)[-1]
