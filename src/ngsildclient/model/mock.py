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


def mock_id(e: Entity) -> Entity:
    mock_id = shortuuid()
    e.id = f"{e.id}:Mocked:{mock_id}"
    e.prop("mocked", True)


class MockerNgsi:
    def __init__(self, entity: Entity):
        self.src = entity

    def _mock(
        self, mock_id: Callable = mock_id, mock_payload: Callable = None
    ) -> Entity:
        dst: Entity = self.src.copy()
        mock_id(dst)
        if mock_payload is not None:
            mock_payload(dst)
        return dst

    def mock(
        self,
        n: int = 1,
        mock_id: Callable = mock_id,
        mock_payload: Callable = None,
    ) -> list[Entity]:
        return [self._mock() for _ in range(n)]
