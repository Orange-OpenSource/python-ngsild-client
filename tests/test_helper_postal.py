#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.
# SPDX-License-Identifier: Apache-2.0

from ngsildclient.model.helper.postal import PostalAddressBuilder


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
