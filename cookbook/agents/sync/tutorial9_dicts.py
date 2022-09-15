#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from ngsildclient import Entity, Client


def build_entity(room: dict) -> Entity:
    e = Entity("RoomObserved", room["name"])
    e.prop("temperature", room["temp"])
    e.prop("pressure", room["pressure"])
    return e


def main():
    client = Client()
    rooms = [{"name": "Room1", "temp": 23.1, "pressure": 720}, {"name": "Room2", "temp": 21.8, "pressure": 711}]
    for room in rooms:
        entity = build_entity(room)
        client.upsert(entity)


if __name__ == "__main__":
    main()
