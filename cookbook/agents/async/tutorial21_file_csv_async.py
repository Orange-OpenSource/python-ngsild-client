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
from ngsildclient import Entity, AsyncClient, iso8601


def build_entity(csvline: str) -> Entity:
    room = csvline.rstrip().split(";")
    e = Entity("RoomObserved", f"{room[0]}:{iso8601.utcnow()}")
    e.obs()
    e.prop("temperature", room[1])
    e.prop("pressure", float(room[1]))
    return e


async def main():
    client = AsyncClient()
    async with aiofiles.open("../data/rooms.csv", "r") as f:
        async for csvline in f:
            entity = build_entity(csvline)
            await client.upsert(entity)


if __name__ == "__main__":
    asyncio.run(main())
