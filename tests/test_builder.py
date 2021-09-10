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
from orionldclient.model.builder import PostalAddressBuilder


def test_build_context():
    builder = ContextBuilder()
    builder.add("https://example.org/dummy-context.jsonld")
    assert builder._ctx == [
        "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        "https://example.org/dummy-context.jsonld",
    ]
    builder = ContextBuilder()
    assert builder._ctx == ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]


def test_build_postal_address():
    builder = PostalAddressBuilder()
    addr = (
        builder.street("C/ La Pereda 14")
        .locality("Santander")
        .region("Cantabria")
        .country("Spain")
        .build()
    )
    assert addr == {
        "streetAddress": "C/ La Pereda 14",
        "addressLocality": "Santander",
        "addressRegion": "Cantabria",
        "addressCountry": "Spain",
    }