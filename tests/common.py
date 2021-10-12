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

from pytest import fixture
from pytest_mock import MockerFixture
from datetime import datetime
from orionldclient.model.entity import Entity
from orionldclient.core.client import Client

sample_entity = Entity("AirQualityObserved:RZ:Obsv4567", "AirQualityObserved")
sample_entity.tprop("dateObserved", datetime(2018, 8, 7, 12))
sample_entity.prop("NO2", 22, unitcode="GP")
sample_entity.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")


@fixture()
def mock_connected(mocker: MockerFixture):
    mocker.patch.object(Client, "is_connected", return_value=True)
