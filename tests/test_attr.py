#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import pytest

from datetime import datetime
from dateutil.tz import UTC
from ngsildclient.model.entity import Entity
from ngsildclient.model.attr.prop import AttrPropValue


def test_observedat():
    e = Entity("OffStreetParking", "Downtown1")
    e.prop("availableSpotNumber", 121, observedat=datetime(2017, 7, 29, 12, 5, 2))
    p = e["availableSpotNumber"]
    assert isinstance(p, AttrPropValue)
    dt = p.observedat
    assert dt == datetime(2017, 7, 29, 12, 5, 2, tzinfo=UTC)
