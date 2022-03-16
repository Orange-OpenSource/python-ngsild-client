#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from ngsildclient.api.helper.subscription import SubscriptionBuilder

NOTIF_URI = "http://tutorial:3000/subscription/low-stock-farm001-ngsild"


def test_build_subscription():
    builder = (
        SubscriptionBuilder(NOTIF_URI)
        .description("Notify me of low feedstock on Farm:001")
        .select_type("FillingLevelSensor")
        .watch(["filling"])
        .query("filling>0.4;filling<0.6;controlledAsset==urn:ngsi-ld:Building:farm001")
        .notif(["filling", "controlledAsset"])
    )
    subscription = builder.build()
    assert subscription == {
        "type": "Subscription",
        "description": "Notify me of low feedstock on Farm:001",
        "entities": [{"type": "FillingLevelSensor"}],
        "watchedAttributes": ["filling"],
        "q": "filling>0.4;filling<0.6;controlledAsset==urn:ngsi-ld:Building:farm001",
        "isActive": True,
        "notification": {
            "attributes": ["filling", "controlledAsset"],
            "format": "normalized",
            "endpoint": {
                "uri": "http://tutorial:3000/subscription/low-stock-farm001-ngsild",
                "accept": "application/ld+json",
            },
        },
        "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    }
