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

from orionldclient.model.serialization import NgsiSerializationProtocol
from orionldclient.model.entity import Entity
from orionldclient.model.ngsidict import NgsiDict


class Room(NgsiSerializationProtocol):
    def __init__(self, id: int, temperature: float):
        self.id = f"Room{id}"
        self.type = "Room"
        self.temperature = temperature

    def __repr__(self):
        return f"{self.id} {self.type} {self.temperature}"

    def __ngsild__to__(self) -> str:
        e = Entity(self.id, self.type)
        e.prop("temperature", self.temperature)
        return e

    @classmethod
    def __ngsild__from__(cls, payload: NgsiDict):
        id_str = payload["id"]
        id = int(id_str[16:]) # TODO : unprefix()
        temp_str = payload["temperature"]["value"]
        temp = float(temp_str)
        return cls(id, temp)


def test_to_ngsi():
    o = Room(1, 22.5)
    print(o.__ngsild__to__())


def test_from_ngsi():
    payload = {
        "id": "urn:ngsi-ld:Room1",
        "type": "Room",
        "temperature": {"type": "Property", "value": 22.5},
    }
    o = Room.__ngsild__from__(payload)
    print(o)
