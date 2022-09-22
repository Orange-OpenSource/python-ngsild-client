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

import logging

if TYPE_CHECKING:
    from .client import Client

from .constants import EntityId, JSONLD_CONTEXT
from ..model.entity import Entity


logger = logging.getLogger(__name__)


class Temporal:
    def __init__(self, client: Client, url: str):
        self._client = client
        self._session = client.session
        self.url = url

    def get(
        self,
        eid: Union[EntityId, Entity],
        ctx: str = None,
        **kwargs,
    ) -> dict:
        eid = eid.id if isinstance(eid, Entity) else eid
        headers = {
            "Accept": "application/ld+json",
            "Content-Type": None,
        }  # overrides session headers
        if ctx is not None:
            headers["Link"] = f'<{ctx}>; rel="{JSONLD_CONTEXT}"; type="application/ld+json"'
        r = self._session.get(f"{self.url}/{eid}", headers=headers, **kwargs)
        self._client.raise_for_status(r)
        return r.json()
