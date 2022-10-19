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

import ngsildclient.model.entity as entity
import ngsildclient.model.ngsidict as ngsidict

from json import JSONEncoder

class NgsiEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (ngsidict.NgsiDict, entity.Entity)):
            return o.to_dict()
        return str

