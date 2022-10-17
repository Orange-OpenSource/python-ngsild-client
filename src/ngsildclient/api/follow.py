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
from typing import TYPE_CHECKING, Generator, Callable

if TYPE_CHECKING:
    from .client import Client
    from ngsildclient.model.entity import Entity

class LinkFollower:
    def __init__(self, client: Client):
        self._client = client

    def follow(self, urn: str) -> Entity:
        return self._client.get(urn)
