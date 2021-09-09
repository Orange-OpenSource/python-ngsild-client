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

from orionldclient.model.entity import ContextBuilder

def test_build_cootext():
    ctx = ContextBuilder()
    ctx.add("nimp")
    print(ctx._ctx)
    assert ctx._ctx == ['https://schema.lab.fiware.org/ld/context', 'https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld', 'nimp']
    ctx = ContextBuilder()
    assert ctx._ctx == ['https://schema.lab.fiware.org/ld/context', 'https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld']