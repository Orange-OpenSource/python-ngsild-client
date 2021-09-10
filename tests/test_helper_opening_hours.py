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

from datetime import time

from orionldclient.model.helper.openinghours import (
    OpeningHoursSpecificationBuilder,
    WeekDay,
)


def test_build_opening_hours_specification():
    builder = OpeningHoursSpecificationBuilder()
    openinghours = builder.monday(time(9), time(17)).tuesday("09:00", "18:00").build()
    assert openinghours == [
        {"opens": "09:00", "closes": "17:00", "dayOfWeek": "Monday"},
        {"opens": "09:00", "closes": "18:00", "dayOfWeek": "Tuesday"},
    ]


def test_build_opening_hours_specification_batch():
    builder = OpeningHoursSpecificationBuilder()
    openinghours = builder.set_days(
        "08:00", "12:00", WeekDay.MONDAY, WeekDay.TUESDAY, WeekDay.THURSDAY
    ).build()
    assert openinghours == [
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Monday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Tuesday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Thursday"},
    ]
