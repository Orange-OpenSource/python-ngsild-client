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
import aiofiles
import json
from ngsildclient import Entity, AsyncClient, iso8601


def build_entity(room: dict) -> Entity:
    e = Entity("RoomObserved", f"{room['id']}:{iso8601.utcnow()}")
    e.obs()
    e.prop("temperature", room["temperature"])
    e.prop("pressure", room["pressure"])
    return e


async def main():
    client = AsyncClient()
    async with aiofiles.open("data/rooms.json") as f:
        content = await f.read()
        payload: dict = json.loads(content)
    for room in payload["rooms"]:
        entity = build_entity(room)
        await client.upsert(entity)


if __name__ == "__main__":
    asyncio.run(main())
