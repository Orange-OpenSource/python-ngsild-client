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

from typing import Any, List, Literal, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ngsildclient.model.attr.prop import AttrProp
    from ngsildclient.model.attr.geo import AttrGeo
    from ngsildclient.model.attr.temporal import AttrTemporal
    from ngsildclient.model.attr.rel import AttrRel
    from ngsildclient.model.entity import Entity

from collections.abc import MutableMapping, Mapping

from datetime import datetime
from scalpl import Cut

from ..utils import iso8601, url
from .constants import *
from .exceptions import *
from ngsildclient.settings import globalsettings
from ngsildclient.model.utils import tuple_to_point

import json

"""This module contains the definition of the NgsiDict class.
"""

class NgsiDict(Cut, MutableMapping):
    """This class is a custom dictionary that backs an entity.

    Attr is used to build and hold the entity properties, as well as the entity's root.
    It's not exposed to the user but intended to be used by the Entity class.
    NgsiDict provides methods that allow to build a dictionary compliant with a NGSI-LD structure.

    See Also
    --------
    model.Entity
    """

    def __init__(self, data: dict = None, name: str = None):
        super().__init__(data)
        self.name = name

    def is_root(self) -> bool:
        return self.get("@context") is not None

    def __getitem__(self, path: str):
        item = super().__getitem__(path)
        if isinstance(item, Mapping) and not isinstance(item, NgsiDict):
            from ngsildclient.model.attr.factory import AttrFactory
            return AttrFactory.create(item)
        return item

    def __repr__(self):
        return self.data.__repr__()

    def __ior__(self, prop: Mapping):
        prop = prop.data if isinstance(prop, NgsiDict) else prop
        self.data |= prop
        return self

    @property
    def value(self):
        raise NotImplementedError()

    @value.setter
    def value(self, v: Any):
        raise NotImplementedError()

    @property
    def type(self) -> Literal["Property", "GeoProperty", "TemporalProperty", "Relationship"]:
        raise NotImplementedError()

    @classmethod
    def _from_json(cls, payload: str):
        d = json.loads(payload)
        return cls(d)

    @classmethod
    def _load(cls, filename: str):
        with open(filename, "r") as fp:
            d = json.load(fp)
            return cls(d)

    def to_dict(self) -> dict:
        return self.data
        
    def to_json(self, indent=None) -> str:
        """Returns the dict in json format"""
        return json.dumps(self,  ensure_ascii=False, indent=indent, 
            default = lambda x: x.data if isinstance(x, NgsiDict) else str)

    def pprint(self, *args, **kwargs) -> None:
        """Returns the dict pretty-json-formatted"""
        globalsettings.f_print(self.to_json(indent=2, *args, **kwargs))

    def _save(self, filename: str, indent=2):
        with open(filename, "w") as fp:
            json.dump(self, fp, ensure_ascii=False, indent=indent,
                default = lambda x: x.data if isinstance(x, NgsiDict) else str)

    @classmethod
    def prop(
        cls,
        name: str,
        value: Any,
        *,  # keyword-only arguments after this
        datasetid: str = None,
        observedat: Union[str, datetime] = None,
        unitcode: str = None,
        userdata: NgsiDict = None,
        escape: bool = False,
        fq: bool = False
    ) -> AttrProp:
        from ngsildclient.model.attr.prop import AttrProp
        if isinstance(value, MultAttr):
            if len(value) == 0:
                raise ValueError("MultAttr is empty")
            p: List[AttrProp] = [AttrProp.build(v) for v in value]
        else:
            value = url.escape(value) if escape and isinstance(value, str) else value
            attrvalue = AttrValue(value, datasetid, observedat, unitcode, userdata)
            p = AttrProp.build(attrvalue)
        return {name: p} if fq else p

    @classmethod
    def gprop(
        cls,
        name: str,
        value: Union[Tuple[float], NgsiGeometry],
        *,  # keyword-only arguments after this
        datasetid: str = None,
        observedat: Union[str, datetime] = None,
        fq: bool = False
    ) -> AttrGeo:
        from ngsildclient.model.attr.geo import AttrGeo
        if isinstance(value, Tuple):
            if len(value) == 2:
                lat, lon = value
                value = Point((lon, lat))
            else:
                raise ValueError("lat, lon tuple expected")
        attrvalue = AttrValue(value, datasetid, observedat)
        p = AttrGeo.build(attrvalue)
        return {name: p} if fq else p

    @classmethod
    def tprop(
        cls,
        name: str,
        value: NgsiDate = iso8601.utcnow(),
        *,  # keyword-only arguments after this
        fq: bool = False
    ) -> AttrTemporal:
        from ngsildclient.model.attr.temporal import AttrTemporal
        attrvalue = AttrValue(value)
        p = AttrTemporal.build(attrvalue)
        return {name: p} if fq else p

    @classmethod
    def rel(
        cls,
        name: str,
        value: Union[str, List[str], Entity, List[Entity]],
        *,  # keyword-only arguments after this
        datasetid: str = None,
        observedat: Union[str, datetime] = None,
        fq: bool = False
    ) -> AttrRel:
        from ngsildclient.model.attr.rel import AttrRel
        if isinstance(value, MultAttr):
            if len(value) == 0:
                raise ValueError("MultAttr is empty")
            p: List[AttrRel] = [AttrRel.build(v.id if hasattr(v, "id") else v) for v in value]
        else:
            value = value.id if hasattr(value, "id") else value
            attrvalue = AttrValue(value, datasetid, observedat)
            p = AttrRel.build(attrvalue)
        return {name: p} if fq else p
