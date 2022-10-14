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
import importlib.util


def is_interactive() -> bool:
    return hasattr(sys, "ps1") or sys.flags.interactive


def is_pandas_installed() -> bool:
    return importlib.util.find_spec("pandas") is not None

def _addopt(params: dict, newopt: str):
    if params.get("options", "") == "":
        params["options"] = newopt
    else:
        params["options"] += f",{newopt}"    
