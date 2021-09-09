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

import pkg_resources
import json
from pytest import fixture

from datetime import datetime
from orionldclient.model.entity import *
from orionldclient.model.attribute import *
from orionldclient.utils import urnprefix

def test_agrifood__animal():
    ctx = ContextBuilder().add("https://smartdatamodels.org/context.jsonld").build()
    e = Entity("Animal:ca3f1295-500c-4aa3-b745-d143097d5c01", "Animal", ctx)
    e.prop("legalId", "ES142589652140")
    e.prop("locatedAt", urnprefix("AgriParcel:1ea0f120-4474-11e8-9919-672036642081"))
    e.tprop("birthdate", datetime(2017, 1, 1, 1, 20))
    e.prop("breed", "Merina")
    e.prop("calvedBy", urnprefix("Animal:aa9f1295-425c-8ba3-b745-b653097d5a87"))
    e.prop("feedWith", urnprefix("FEED:1ea0f120-4474-11e8-9919-0000000081"))
    e.prop("healthCondition", "healthy")
    e.pprint()
