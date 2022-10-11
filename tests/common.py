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

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from ngsildclient.model.constants import EntityOrId

from datetime import datetime, timezone
from ngsildclient.model.entity import Entity
from ngsildclient.api.client import Client
from ngsildclient.utils.urn import Urn

sample_entity = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
sample_entity.tprop("dateObserved", datetime(2018, 8, 7, 12, tzinfo=timezone.utc))
sample_entity.prop("NO2", 22, unitcode="GP")
sample_entity.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")

class MockedClient(Client):
    def __init__(self):
        self._broker_impl: dict[str, Entity] = {}

    def get(self, entity: EntityOrId) -> Entity:
        eid = entity.id if isinstance(entity, Entity) else entity
        return self._broker_impl[Urn.prefix(eid)]

    def upsert(self, entities: List[Entity]):
        self._broker_impl |= {e.id: e for e in entities}