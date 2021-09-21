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

from typing import Protocol, runtime_checkable
from abc import ABCMeta, abstractmethod
from orionldclient.model.entity import Entity


@runtime_checkable
class NgsiProtocol(Protocol):
    _ngsi_id: str = None
    _ngsi_type: str = None
    _ngsi_ctx = [Entity.DEFAULT_CONTEXT]

    @property
    def _ngsi_interface(self):
        return self._ngsi_id, self._ngsi_type, self._ngsi_ctx


class NgsiSerializer(metaclass=ABCMeta):
    def __init__(self, type: str, ctx: list = [Entity.DEFAULT_CONTEXT]):
        self.type = type
        self.ctx = ctx

    @abstractmethod
    def dump(self, obj: NgsiProtocol) -> Entity:
        if not isinstance(obj, NgsiProtocol):
            raise ValueError(f"Object {obj} must implement the NgsiLdProtocol")
        _id, _type, _ctx = obj._ngsi_interface
        if _type != self.type:
            raise ValueError(f"Serializer cannot handle type {_type}")
        if _ctx is None:
            _ctx = self.ctx
        e = Entity(_id, _type, _ctx)
        return e

    @abstractmethod
    def load(self, e: Entity) -> NgsiProtocol:
        raise NotImplementedError
