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
from typing import TYPE_CHECKING, Union
from httpx import Response
import logging

if TYPE_CHECKING:
    from .client import AsyncClient

from ..constants import EntityId, JSONLD_CONTEXT
from ...model.entity import Entity

from ..exceptions import rfc7807_error_handle_async

logger = logging.getLogger(__name__)


class Entities:
    def __init__(self, client: AsyncClient, url: str):
        self._client = client.client
        self.url = url

    @rfc7807_error_handle_async
    async def get(
        self,
        eid: Union[EntityId, Entity],
        ctx: str = None,
        asdict: bool = False,
        **kwargs,
    ) -> Entity:
        eid = eid.id if isinstance(eid, Entity) else eid
        headers = {"Accept": "application/ld+json"}  # overrides session headers
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        logger.info(f"{headers=}")
        r: Response = await self._client.get(f"{self.url}/{eid}", headers=headers, **kwargs)
        r.raise_for_status()
        return r.json() if asdict else Entity.from_dict(r.json())
