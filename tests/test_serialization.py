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

from orionldclient.onm.serialization import NgsiLdInterface, NgsiLdSerializer
from orionldclient.model.entity import Entity
from orionldclient.utils import urnprefix


class Room(NgsiLdInterface):
    def __init__(self, id: int, temperature: float):
        self.id = id
        self.temperature = temperature

    def __repr__(self):
        return f"Room{self.id} : {self.temperature}"

    def __ngsi_ld__interface__(self) -> tuple[str, str, list]:
        return urnprefix(f"Room{self.id}"), "Room", None


class RoomSerializer(NgsiLdSerializer):
    def dump(self, room: Room) -> Entity:
        e = super().dump(room)
        e.prop("temperature", room.temperature)
        return e


def test_serialize_room():
    room = Room(1, 22.5)
    serializer = RoomSerializer()
    e = serializer.dump(room)
    assert e.to_dict() == {
        "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
        "id": "urn:ngsi-ld:urn:ngsi-ld:Room1",
        "type": "Room",
        "temperature": {"type": "Property", "value": 22.5},
    }
