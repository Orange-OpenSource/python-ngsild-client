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

import json

from copy import deepcopy
from datetime import datetime
from typing import Any, Union

from .exceptions import *
from .constants import *
from .attribute import *
from .ngsidict import NgsiDict


class Context:

    DEFAULT = [
        "https://schema.lab.fiware.org/ld/context",
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    ]

    _data: list[str] = None

    @property
    def data(self):
        return self._data

    def __init__(self, ctx: list[str] = DEFAULT):
        self._data = ctx

    def add(self, uri: str):
        self._data.append(uri)

    def remove(self, uri: str):
        self._data.remove(uri)

    def __repr__(self):
        return self._data.__repr__()


class Entity:
    def __init__(
        self,
        id: str,
        type: str,
        ctx: Context = Context(),
    ):
        self.id = id = Urn.prefix(id)
        self.type = type
        self.ctx = ctx
        self._entity: NgsiDict = NgsiDict({"id": id, "type": type})

    def getattr(self, attr: str):
        return self._entity.get(attr)

    def setattr(self, attr: str, value: Any):
        self._entity[attr] = value

    def prop(
        self,
        name: str,
        value: Any,
        unitcode: str = None,
        observed_at: Union[str, datetime] = None,
        dataset_id: str = None,
        userdata: NgsiDict = NgsiDict(),
    ):
        self._entity.prop(name, value, unitcode, observed_at, dataset_id, userdata)
        return self._entity[name]

    def gprop(self, name: str, value: Any):
        self._entity.gprop(name, value)
        return self._entity[name]

    def tprop(self, name: str, value: Any):
        # TODO : handle Date and Time
        self._entity.tprop(name, value)
        return self._entity[name]

    def rel(
        self,
        name: str,
        value: str,
        observed_at: Union[str, datetime] = None,
        userdata: NgsiDict = NgsiDict(),
    ):
        self._entity.rel(name, value, observed_at, userdata)
        return self._entity[name]

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self.type == other.type and self.id == other.id

    def __repr__(self):
        return self._entity.__repr__()

    def to_json(self, indent=None):
        """Returns the datamodel in json format"""
        entity_with_context = deepcopy(self._entity)
        entity_with_context[META_ATTR_CONTEXT] = self.ctx.data
        return json.dumps(
            entity_with_context, default=str, ensure_ascii=False, indent=indent
        )

    def pprint(self):
        """Returns the datamodel pretty-json-formatted"""
        print(self.to_json(indent=2))
