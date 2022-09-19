#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

# Requires : flask
# Usage : uvicorn tutorial43_api_server_fastapi_rest_json_async:app
# Usage : curl -X POST -H "Content-Type: application/json" -d "@room.json" http://127.0.0.1:8000/rooms

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from ngsildclient import Entity, AsyncClient, iso8601

app = FastAPI()
client = AsyncClient()


class RoomObserved(BaseModel):
    id: str
    temperature: float
    pressure: int


def build_entity(room: RoomObserved) -> Entity:
    e = Entity("RoomObserved", f"{room.id}:{iso8601.utcnow()}")
    e.obs()
    e.prop("temperature", room.temperature)
    e.prop("pressure", room.pressure)
    return e


@app.post("/rooms")
async def post_room(room: RoomObserved):
    entity = build_entity(room)
    await client.upsert(entity)
    return JSONResponse(
        status_code=201, content=entity.to_dict(), headers={"Content-Location": client.entities.to_broker_url(entity)}
    )
