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

from dataclasses import dataclass
from ngsildclient import Entity, AsyncClient


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


async def main():
    client = AsyncClient()
    rooms = [Room("Room1", 23.1, 720), Room("Room2", 21.8, 711)]
    entities = [build_entity(room) for room in rooms]
    await client.upsert(entities)


if __name__ == "__main__":
    asyncio.run(main())
