#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from datetime import time

from ngsildclient.model.helper.openinghours import (
    WEEK,
    OpeningHoursBuilder,
)


def test_build_opening_hours_set_days():
    builder = OpeningHoursBuilder()
    openinghours = builder.monday(time(9), time(17)).tuesday("09:00", "18:00").build()
    assert openinghours == [
        {"opens": "09:00", "closes": "17:00", "dayOfWeek": "Monday"},
        {"opens": "09:00", "closes": "18:00", "dayOfWeek": "Tuesday"},
    ]


def test_build_opening_hours_set_all_week_1():
    builder = OpeningHoursBuilder()
    openinghours = builder.wholeweek("08:00", "12:00").build()
    assert openinghours == [
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Monday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Tuesday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Wednesday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Thursday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Friday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Saturday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Sunday"},
    ]


def test_build_opening_hours_set_all_week_2():
    builder = OpeningHoursBuilder()
    openinghours = builder.days("08:00", "12:00", *WEEK).build()
    assert openinghours == [
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Monday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Tuesday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Wednesday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Thursday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Friday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Saturday"},
        {"opens": "08:00", "closes": "12:00", "dayOfWeek": "Sunday"},
    ]
