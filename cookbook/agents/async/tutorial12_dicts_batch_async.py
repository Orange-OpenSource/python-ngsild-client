#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import asyncio

from ngsildclient import Entity, AsyncClient


def build_entity(room: dict) -> Entity:
    e = Entity("RoomObserved", room["name"])
    e.prop("temperature", room["temp"])
    e.prop("pressure", room["pressure"])
    return e


async def main():
    client = AsyncClient()
    rooms = [{"name": "Room1", "temp": 23.1, "pressure": 720}, {"name": "Room2", "temp": 21.8, "pressure": 711}]
    entities = [build_entity(room) for room in rooms]
    await client.upsert(entities)


if __name__ == "__main__":
    asyncio.run(main())
