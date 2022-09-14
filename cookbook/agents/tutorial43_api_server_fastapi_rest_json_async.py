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
# Usage : curl -X POST -H "Content-Type: application/json" -d "@data/room.json" http://127.0.0.1:8000/rooms

from fastapi import FastAPI, Request
from ngsildclient import Entity, AsyncClient, iso8601

app = FastAPI()
client = AsyncClient()


def build_entity(room: dict) -> Entity:
    e = Entity("RoomObserved", f"{room['id']}:{iso8601.utcnow()}")
    e.obs()
    e.prop("temperature", room["temperature"])
    e.prop("pressure", room["pressure"])
    return e


@app.post("/rooms")
async def post_room(request: Request):
    payload = await request.json()
    rooms = payload["rooms"]
    entities = [build_entity(room) for room in rooms]
    await client.upsert(entities)
    return "CSV file processed"
