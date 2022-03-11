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
from typing import Callable
from ngsildclient import Entity
from ngsildclient.utils.uuid import shortuuid

logger = logging.getLogger(__name__)


def mock_id(e: Entity):
    mock_id = shortuuid()
    e.id = f"{e.id}:Mocked:{mock_id}"


def mock_payload(e: Entity):
    e.prop("mocked", True)


class MockerNgsi:
    def __init__(
        self,
        f_mock_id: Callable = mock_id,
        f_mock_payload: Callable = mock_payload,
    ):
        self.f_mock_id = f_mock_id
        self.f_mock_payload = f_mock_payload

    def _mock(self, entity: Entity) -> Entity:
        dst: Entity = entity.copy()
        self.f_mock_id(dst)
        self.f_mock_payload(dst)
        return dst

    def mock(self, entity: Entity, n: int = 10) -> list[Entity]:
        return [self._mock(entity) for _ in range(n)]
