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

from typing import Protocol, Any, Union
from functools import reduce
from datetime import datetime
from geojson import Point, LineString, Polygon

from ..utils import iso8601, url
from ..utils.urn import Urn
from .constants import *
from .exceptions import *

import json
import operator


class NgsiFormatter(Protocol):

    # helper methods to build attributes

    def prop(self, *args, **kwargs) -> NgsiFormatter:
        ...

    def gprop(self, *args, **kwargs) -> NgsiFormatter:
        ...

    def tprop(self, *args, **kwargs) -> NgsiFormatter:
        ...

    def rel(self, *args, **kwargs) -> NgsiFormatter:
        ...

    # helper methods to read and write

    def _from_json(self, payload: str) -> NgsiFormatter:
        ...

    def _load(self, payload: str) -> NgsiFormatter:
        ...

    def to_json(self, *args, **kwargs) -> str:
        ...

    def pprint(self) -> None:
        ...

    def _save(self, filename: str) -> None:
        ...


class NgsiDict(dict, NgsiFormatter):
    @classmethod
    def _from_json(cls, payload: str):
        d = json.loads(payload)
        return cls(d)

    def _attr(self, element: str):
        return reduce(operator.getitem, element.split("."), self)

    def _rmattr(self, element: str):
        try:
            nested, k = element.rsplit(".", 1)
        except ValueError:
            del self[element]
        else:
            del self._attr(nested)[k]

    def _setattr(self, element: str, value: Any):
        try:
            nested, k = element.rsplit(".", 1)
        except ValueError:
            self[element] = value
        else:
            self._attr(nested)[k] = value

    @classmethod
    def _load(cls, filename: str):
        with open(filename, "r") as fp:
            d = json.load(fp)
            return cls(d)

    def to_json(self, indent=None) -> str:
        """Returns the dict in json format"""
        return json.dumps(self, default=str, ensure_ascii=False, indent=indent)

    def pprint(self, *args, **kwargs) -> None:
        """Returns the dict pretty-json-formatted"""
        print(self.to_json(indent=2, *args, **kwargs))

    def _save(self, filename: str, indent=2):
        with open(filename, "w") as fp:
            json.dump(self, fp, default=str, ensure_ascii=False, indent=indent)

    def prop(
        self,
        name: str,
        value: Any,
        unitcode: str = None,
        observedat: Union[str, datetime] = None,
        datasetid: str = None,
        userdata: NgsiDict = None,
        escape: bool = False,
    ):
        self[name] = self._build_property(
            value, unitcode, observedat, datasetid, userdata, escape
        )
        return self[name]

    def gprop(self, name: str, value: NgsiGeoType):
        self[name] = self._build_geoproperty(value)
        return self[name]

    def tprop(self, name: str, value: NgsiDateType):
        self[name] = self._build_temporal_property(value)
        return self[name]

    def rel(
        self,
        name: str,
        value: str,
        observedat: Union[str, datetime] = None,
        userdata: NgsiDict = None,
    ):
        self[name] = self._build_relationship(value, observedat, userdata)
        return self[name]

    def _build_property(
        self,
        value: Any,
        unitcode: str = None,
        observedat: Union[str, datetime] = None,
        datasetid: str = None,
        userdata: NgsiDict = None,
        escape: bool = False,
    ) -> NgsiDict:
        property: NgsiDict = NgsiDict()
        property["type"] = AttrType.PROP.value  # set type
        if isinstance(value, (int, float, bool, list, dict)):
            v = value
        elif isinstance(value, str):
            v = url.escape(value) if escape else value
        else:
            raise NgsiUnmatchedAttributeTypeError(
                f"Cannot map {type(value)} to NGSI type. {value=}"
            )
        property["value"] = v  # set value
        if unitcode is not None:
            property[META_ATTR_UNITCODE] = unitcode
        if observedat is not None:
            date_str, temporaltype = iso8601.parse(observedat)
            if temporaltype != TemporalType.DATETIME:
                raise NgsiDateFormatError(f"observedAt must be a DateTime : {date_str}")
            property[META_ATTR_OBSERVED_AT] = date_str
        if datasetid is not None:
            property[META_ATTR_DATASET_ID] = Urn.prefix(datasetid)
        if userdata:
            property |= userdata
        return property

    def _build_geoproperty(self, value: NgsiGeoType) -> NgsiDict:
        property: NgsiDict = NgsiDict()
        property["type"] = AttrType.GEO.value  # set type
        if isinstance(value, (Point, LineString, Polygon)):
            geometry = value
        elif (
            isinstance(value, tuple) and len(value) == 2
        ):  # simple way for a location Point
            lat, lon = value
            geometry = Point((lon, lat))
        else:
            raise NgsiUnmatchedAttributeTypeError(
                f"Cannot map {type(value)} to NGSI type. {value=}"
            )
        property["value"] = geometry  # set value
        return property

    def _build_temporal_property(
        self, value: NgsiDateType
    ) -> NgsiDict:  # TODO => restrict value type
        property: NgsiDict = NgsiDict()
        property["type"] = AttrType.TEMPORAL.value  # set type
        date_str, temporaltype = iso8601.parse(value)
        v = {
            "@type": temporaltype.value,
            "@value": date_str,
        }
        property["value"] = v  # set value
        return property

    def _build_relationship(
        self,
        value: str,
        observedat: Union[str, datetime] = None,
        userdata: NgsiDict = None,
    ) -> NgsiDict:
        property: NgsiDict = NgsiDict()
        property["type"] = AttrType.REL.value  # set type
        property["object"] = Urn.prefix(value)  # set value
        if observedat is not None:
            date_str, temporaltype = iso8601.parse(observedat)
            if temporaltype != TemporalType.DATETIME:
                raise NgsiDateFormatError(f"observedAt must be a DateTime : {date_str}")
            property[META_ATTR_OBSERVED_AT] = date_str
        if userdata:
            property |= userdata
        return property
