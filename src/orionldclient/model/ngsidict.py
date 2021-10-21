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
from typing import Protocol, Any
from functools import reduce

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

    def prop(self, name, *args, **kwargs):
        from .attribute import build_property

        self[name] = build_property(*args, **kwargs)
        return self[name]

    def gprop(self, name, *args, **kwargs):
        from .attribute import build_geoproperty

        self[name] = build_geoproperty(*args, **kwargs)
        return self[name]

    def tprop(self, name, *args, **kwargs):
        from .attribute import build_temporal_property

        self[name] = build_temporal_property(*args, **kwargs)
        return self[name]

    def rel(self, name, *args, **kwargs):
        from .attribute import build_relationship

        self[name] = build_relationship(*args, **kwargs)
        return self[name]
