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

from __future__ import annotations

import json
import requests

from copy import deepcopy
from functools import partialmethod

from datetime import datetime
from typing import Any, Union

from .exceptions import *
from .constants import *
from ._attribute import *
from .ngsidict import NgsiDict
from orionldclient.utils.url import isurl
from orionldclient.utils.urn import Urn


class Entity:
    def __init__(self, id: str, type: str, context: list = [CORE_CONTEXT]):
        """Create a NGSI-LD compliant entity

        Parameters
        ----------
        id : str
            entity identifier
        type : str
            entity type
        context : list, optional
            the NGSI-LD context, by default the NGSI-LD Core Context
        """        
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
        if isurl(filename):
            resp = requests.get(filename)
            d = resp.json()
        else:
            with open(filename, "r") as fp:
                d = json.load(fp)
        return cls.from_dict(d)

    @staticmethod
    def duplicate(other) -> Entity:
        new = deepcopy(other)
        return new

    @property
    def id(self):
        return self._payload["id"]

    @id.setter
    def id(self, eid: str):
        self._payload["id"] = eid

    @property
    def type(self):
        return self._payload["type"]

    @type.setter
    def type(self, etype: str):
        self._payload["type"] = etype

    @property
    def context(self):
        return self._payload["@context"]

    @context.setter
    def context(self, ctx: list):
        self._payload["@context"] = ctx

    def __getitem__(self, item):
        return self._payload._attr(item)

    def __setitem__(self, key, item):
        self._payload[key] = item

    def rm(self, item):
        self._payload._rmattr(item)
        return self

    def prop(
        self,
        name: str,
        value: Any,
        /,  # positional-only arguments before this
        *,  # keyword-only arguments after this
        unitcode: str = None,
        observedat: Union[str, datetime] = None,
        datasetid: str = None,
        userdata: NgsiDict = NgsiDict(),
    ):
        self._payload.prop(name, value, unitcode, observedat, datasetid, userdata)
        return self._payload[name]

    def gprop(self, name: str, value: Any):
        if value is None:
            raise AttributeError("missing value")
        self._payload.gprop(name, value)
        return self._payload[name]

    loc = partialmethod(gprop, "location")

    def tprop(self, name: str, value: Any, /):
        self._payload.tprop(name, value)
        return self._payload[name]

    def rel(
        self,
        name: Union[str, PredefinedRelationship],
        value: str,
        /,
        *,
        observedat: Union[str, datetime] = None,
        userdata: NgsiDict = NgsiDict(),
    ):
        if isinstance(name, Enum):
            name = name.value
        self._payload.rel(name, value, observedat, userdata)
        return self._payload[name]

    rel_haspart = partialmethod(rel, PredefinedRelationship.HAS_PART)
    rel_hasdirectpart = partialmethod(rel, PredefinedRelationship.HAS_DIRECT_PART)
    rel_iscontainedin = partialmethod(rel, PredefinedRelationship.IS_CONTAINED_IN)

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

    def to_json(self, kv=False, *args, **kwargs):
        """Returns the datamodel in json format"""
        payload: NgsiDict = self.to_dict(kv)
        return payload.to_json(*args, **kwargs)

    def pprint(self, kv=False, *args, **kwargs):
        """Returns the datamodel pretty-json-formatted"""
        print(self.to_json(kv, indent=2, *args, **kwargs))

    def save(self, filename: str, *, indent=2):
        with open(filename, "w") as fp:
            json.dump(self._payload, fp, default=str, ensure_ascii=False, indent=indent)
