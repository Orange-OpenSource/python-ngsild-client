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

from typing import Protocol
from abc import ABCMeta, abstractmethod
from orionldclient.model.entity import Entity


class NgsiLdInterface(Protocol):
    def __ngsi_ld__interface__(self) -> tuple[str, str, list]:
        ...


class NgsiLdSerializer(metaclass=ABCMeta):

    @abstractmethod
    def dump(self, obj: NgsiLdInterface) -> Entity:
        _id, _type, _ctx = obj.__ngsi_ld__interface__()
        if _ctx is None:
            _ctx = Entity.DEFAULT_CONTEXT
        e = Entity(_id, _type, _ctx)
        return e
