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
from typing import Protocol

import json

class NgsiFormatter(Protocol):
    def prop(self, *args, **kwargs) -> NgsiFormatter:
        ...

    def gprop(self, *args, **kwargs) -> NgsiFormatter:
        ...

    def tprop(self, *args, **kwargs) -> NgsiFormatter:
        ...

    def rel(self, *args, **kwargs) -> NgsiFormatter:
        ...

    def json(self, *args, **kwargs) -> str:
        ...

    def pprint(self) -> None:
        ...         


class NgsiDict(dict, NgsiFormatter):
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

    def json(self, indent=None):
        """Returns the dict in json format"""
        return json.dumps(
            self, default=str, ensure_ascii=False, indent=indent
        )

    def pprint(self) -> None:
        """Returns the dict pretty-json-formatted"""
        print(self.json(indent=2))        
