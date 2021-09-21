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

from datetime import datetime
from orionldclient.onm.serialization import NgsiProtocol, NgsiSerializer
from orionldclient.model.entity import Entity
from orionldclient.utils.urn import Urn


class Room(NgsiProtocol):
    def __init__(self, id: int, temperature: float, ts: datetime):
        self.id = id
        self.temperature = temperature
        self.ts = ts

    def __repr__(self):
        return f"Room{self.id} : {self.temperature}"


class RoomSerializer(NgsiSerializer):
    def dump(self, room: Room) -> Entity:
        room._ngsi_id = f"Room{room.id}"
        room._ngsi_type = "Room"
        e = super().dump(room)
        e.prop("temperature", room.temperature, observedat=room.ts)
        return e

    def load(self, e: Entity) -> Room:
        _ngsi__id = e["id"]
        _id = int(Urn.unprefix(_ngsi__id)[4:])
        temp: float = e["temperature"]["value"]
        ts: datetime = datetime.strptime(
            e["temperature"]["observedAt"], "%Y-%m-%dT%H:%M:%SZ"
        )
        room = Room(_id, temp, ts)
        room._ngsi_id = _ngsi__id
        room._ngsi_type = "Room"
        room._ngsi_ctx = e["@context"]
        return room


def test_serialize_room():
    room = Room(1, 22.5, datetime(2021, 9, 21, 16, 16))
    serializer = RoomSerializer("Room")
    e = serializer.dump(room)
    assert e.to_dict() == {
        "@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"],
        "id": "urn:ngsi-ld:Room1",
        "type": "Room",
        "temperature": {
            "type": "Property",
            "value": 22.5,
            "observedAt": "2021-09-21T16:16:00Z",
        },
    }


def test_deserialize_room():
    e = {
        "@context": ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"],
        "id": "urn:ngsi-ld:Room2",
        "type": "Room",
        "temperature": {
            "type": "Property",
            "value": 19.0,
            "observedAt": "2021-09-21T16:20:00Z",
        },
    }
    serializer = RoomSerializer("Room")
    room = serializer.load(e)
    assert room.id == 2
    assert room.temperature == 19.0
    assert room.ts == datetime(2021, 9, 21, 16, 20)
