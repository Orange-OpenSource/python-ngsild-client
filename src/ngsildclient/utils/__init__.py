#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

"""Contains helper modules to handle iso8601 dates, URLs, NGSI-LD URNs, and generate short uuids.
"""

import sys


def is_interactive() -> bool:
    return hasattr(sys, "ps1") or sys.flags.interactive
