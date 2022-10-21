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

from .prop import AttrPropValue
from .geo import AttrGeoValue
from .temporal import AttrTemporalValue
from .rel import AttrRelValue
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
            return AttrPropValue(attr)
        elif type == "TemporalProperty":
            return AttrTemporalValue(attr)
        elif type == "GeoProperty":
            return AttrGeoValue(attr)
        elif type == "Relationship":
            return AttrRelValue(attr)
        else:
            return NgsiDict(attr) # should happen only for json arrays
