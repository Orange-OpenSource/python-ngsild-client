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
import requests

from copy import deepcopy
from datetime import datetime
from typing import Any, Union
from functools import reduce

from .exceptions import *
from .constants import *
from ._attribute import *
from .ngsidict import NgsiDict
from orionldclient.utils.url import isurl


class Entity:

    DEFAULT_CONTEXT = "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"

    def __init__(
        self,
        id: str,
        type: str,
        context: list = [DEFAULT_CONTEXT]
    ):
        self._payload: NgsiDict = NgsiDict(
            {"@context": context, "id": urnprefix(id), "type": type}
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
        if isurl(filename):
            resp = requests.get(filename)
            d = resp.json()
        else:
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

    def __getitem__(self, item):
        return self._payload._attr(item)

    def __setitem__(self, key, item):
        self._payload[key] = item

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

    def to_dict(self, kv=False) -> NgsiDict:
        return self._to_keyvalues() if kv else self._payload
        

    def _to_keyvalues(self) -> NgsiDict:
        d = NgsiDict()
        for k, v in self._payload.items():
            if isinstance(v, dict):
                if (
                    v["type"] == AttrType.PROP.value
                ):  # apply to Property and TemporalProperty
                    value = v["value"]
                    if isinstance(value, dict):
                        value = value.get("@value", value)  # for Temporal Property only
                    d[k] = value
                elif v["type"] == AttrType.GEO.value:
                    d[k] = v["value"]
                elif v["type"] == AttrType.REL.value:
                    d[k] = v["object"]
            else:
                d[k] = v
        return d

    def to_json(self, simplified=False, *args, **kwargs):
        """Returns the datamodel in json format"""
        payload: NgsiDict = self.to_dict(simplified)
        return payload.to_json(*args, **kwargs)

    def pprint(self, simplified=False, *args, **kwargs):
        """Returns the datamodel pretty-json-formatted"""
        print(self.to_json(simplified, indent=2, *args, **kwargs))

    def save(self, filename: str, indent=2):
        with open(filename, "w") as fp:
            json.dump(self._payload, fp, default=str, ensure_ascii=False, indent=indent)
