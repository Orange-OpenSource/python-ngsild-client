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

from collections.abc import Mapping

from .prop import AttrProp
from .geo import AttrGeo
from .temporal import AttrTemporal
from .rel import AttrRel
from ..utils import guess_ngsild_type
from ..ngsidict import NgsiDict


class AttrFactory:

    @classmethod
    def create(self, attr: Mapping) -> NgsiDict:
        try:
            type = guess_ngsild_type(attr)
        except ValueError as e:
            return attr
        if type == "Property":
            return AttrProp(attr)
        elif type == "TemporalProperty":
            return AttrTemporal(attr)
        elif type == "GeoProperty":
            return AttrGeo(attr)
        elif type == "Relationship":
            return AttrRel(attr)
        else:
            return NgsiDict(attr) # should never happen
