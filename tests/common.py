#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from datetime import datetime
from ngsildclient.model.entity import Entity

sample_entity = Entity("AirQualityObserved", "AirQualityObserved:RZ:Obsv4567")
sample_entity.tprop("dateObserved", datetime(2018, 8, 7, 12))
sample_entity.prop("NO2", 22, unitcode="GP")
sample_entity.rel("refPointOfInterest", "PointOfInterest:RZ:MainSquare")


# @fixture()
# def mocked_connected(mocker: MockerFixture):
#     mocker.patch.object(Client, "is_connected", return_value=True)
