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

from datetime import datetime


def datetime_to_iso8601(date: datetime) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")


def utcnow_to_iso8601() -> str:
    return datetime_to_iso8601(datetime.utcnow())
