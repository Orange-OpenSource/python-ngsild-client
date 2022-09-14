#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

# Requires : fastapi, uvicorn
# Usage : uvicorn tutorial41_api_server_fastapi_upload_csv_async:app
# Usage : curl -v -F "file=@data/room.csv" http://127.0.0.1:8000

import io

from fastapi import FastAPI, UploadFile
from ngsildclient import Entity, AsyncClient, iso8601

app = FastAPI()
client = AsyncClient()


def build_entity(csvline: str) -> Entity:
    room = csvline.rstrip().split(";")
    e = Entity("RoomObserved", f"{room[0]}:{iso8601.utcnow()}")
    e.obs()
    e.prop("temperature", room[1])
    e.prop("pressure", float(room[1]))
    return e


@app.post("/")
async def upload_file(file: UploadFile):
    file = file.file._file
    csvlines = io.TextIOWrapper(file).readlines()
    entities = [build_entity(csvline) for csvline in csvlines]
    await client.upsert(entities)
    return "CSV file processed"
