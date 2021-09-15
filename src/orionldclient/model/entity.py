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
from ._attribute import *
from .ngsidict import NgsiDict


class Entity:

    DEFAULT_CONTEXT = "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"

    def __init__(
        self,
        id: str,
        type: str,
        context: list = [DEFAULT_CONTEXT],
        contextfirst: bool = False,
    ):
        self.contextfirst = contextfirst  # TODO : move at api level
        self._payload: NgsiDict = NgsiDict(
            {"@context": context, "id": Urn.prefix(id), "type": type}
        )

    @classmethod
    def from_dict(cls, entity: dict):
        if not entity.get("id", None):
            raise NgsiMissingIdError()
        if not entity.get("type", None):
            raise NgsiMissingTypeError()
        if not entity.get("@context", None):
            raise NgsiMissingContextError()
        instance = cls(None, None)  # id and type will be overwritten next line
        instance._payload |= entity
        return instance

    @classmethod
    def load(cls, filename: str):
        with open(filename, "r") as fp:
            d = json.load(fp)
            return cls.from_dict(d)

    @property
    def id(self):
        return self._payload["id"]

    @property
    def type(self):
        return self._payload["type"]

    @property
    def context(self):
        return self._payload["@context"]

    def attr(self, name: str) -> NgsiDict:
        return self._payload.get(name)

    def prop(
        self,
        name: str,
        value: Any,
        unitcode: str = None,
        observedat: Union[str, datetime] = None,
        datasetid: str = None,
        userdata: NgsiDict = NgsiDict(),
    ):
        self._payload.prop(name, value, unitcode, observedat, datasetid, userdata)
        return self._payload[name]

    def gprop(self, name: str, value: Any):
        self._payload.gprop(name, value)
        return self._payload[name]

    def tprop(self, name: str, value: Any):
        # TODO : handle Date and Time
        self._payload.tprop(name, value)
        return self._payload[name]

    def rel(
        self,
        name: str,
        value: str,
        observedat: Union[str, datetime] = None,
        userdata: NgsiDict = NgsiDict(),
    ):
        self._payload.rel(name, value, observedat, userdata)
        return self._payload[name]

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self.type == other.type and self.id == other.id

    def __repr__(self):
        return self._payload.__repr__()

    def to_dict(self) -> NgsiDict:
        return self._payload

    def to_json(self, contextfirst=False, *args, **kwargs):
        """Returns the datamodel in json format"""
        if contextfirst:
            payload: NgsiDict = self._payload
        else:
            ctx = self._payload[META_ATTR_CONTEXT]
            payload: NgsiDict = deepcopy(self._payload)
            del payload[META_ATTR_CONTEXT]
            payload[META_ATTR_CONTEXT] = ctx
        return payload.to_json(*args, **kwargs)

    def pprint(self, *args, **kwargs):
        """Returns the datamodel pretty-json-formatted"""
        print(self.to_json(indent=2, *args, **kwargs))

    def save(self, filename: str, indent=2):
        payload = self.to_dict(self.contextfirst)
        with open(filename, "w") as fp:
            json.dump(payload, fp, default=str, ensure_ascii=False, indent=indent)
