#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from datetime import datetime
from ngsildclient.api.temporal import troes_to_dict

troes1 = [
    {
        "id": "urn:ngsi-ld:RoomObserved:Room1",
        "type": "RoomObserved",
        "temperature": {
            "type": "Property",
            "values": [[21.7, "2022-09-29T04:16:10Z"], [21.6, "2022-09-29T06:16:10Z"]],
        },
    },
    {
        "id": "urn:ngsi-ld:RoomObserved:Room2",
        "type": "RoomObserved",
        "temperature": {
            "type": "Property",
            "values": [[22.7, "2022-09-29T04:16:10Z"], [22.6, "2022-09-29T06:16:10Z"]],
        },
    },
]

troes2 = [
    {
        "id": "urn:ngsi-ld:RoomObserved:Room1",
        "type": "RoomObserved",
        "temperature": {
            "type": "Property",
            "values": [[21.7, "2022-09-29T04:16:10Z"], [21.6, "2022-09-29T06:16:10Z"]],
        },
        "pressure": {
            "type": "Property",
            "values": [[721, "2022-09-29T04:16:10Z"], [720, "2022-09-29T06:16:10Z"]],
        },
    },
    {
        "id": "urn:ngsi-ld:RoomObserved:Room2",
        "type": "RoomObserved",
        "temperature": {
            "type": "Property",
            "values": [[22.7, "2022-09-29T04:16:10Z"], [22.6, "2022-09-29T06:16:10Z"]],
        },
        "pressure": {
            "type": "Property",
            "values": [[731, "2022-09-29T04:16:10Z"], [730, "2022-09-29T06:16:10Z"]],
        },
    },
]


def test_to_tuples_two_entities():
    packed = troes_to_dict(troes2)
    assert packed == {
        "RoomObserved": ["Room1", "Room1", "Room2", "Room2"],
        "observed": [
            datetime(2022, 9, 29, 4, 16, 10),
            datetime(2022, 9, 29, 6, 16, 10),
            datetime(2022, 9, 29, 4, 16, 10),
            datetime(2022, 9, 29, 6, 16, 10),
        ],
        "temperature": [21.7, 21.6, 22.7, 22.6],
        "pressure": [721, 720, 731, 730],
    }
