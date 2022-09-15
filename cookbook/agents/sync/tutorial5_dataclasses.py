#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from dataclasses import dataclass
from ngsildclient import Entity, Client


@dataclass
class Room:
    name: str
    temperature: float
    pressure: int


def build_entity(room: Room) -> Entity:
    e = Entity("RoomObserved", room.name)
    e.prop("temperature", room.temperature)
    e.prop("pressure", room.pressure)
    return e


def main():
    client = Client()
    rooms = [Room("Room1", 23.1, 720), Room("Room2", 21.8, 711)]
    for room in rooms:
        entity = build_entity(room)
        client.upsert(entity)


if __name__ == "__main__":
    main()
