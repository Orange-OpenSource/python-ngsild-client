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

def test_build_context():
    ctx = ContextBuilder()
    ctx.add("https://example.org/dummy-context.jsonld")
    print(ctx._ctx)
    assert ctx._ctx == ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld", "https://example.org/dummy-context.jsonld"]
    ctx = ContextBuilder()
    assert ctx._ctx == ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]