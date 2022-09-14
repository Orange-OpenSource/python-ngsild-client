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
# Usage : flask --app tutorial40_api_server_flask_upload_csv run
# Usage : curl -v -F "file=@data/room.csv" http://127.0.0.1:5000

import io

from flask import Flask, request, Response
from ngsildclient import Entity, Client, iso8601

app = Flask(__name__)
client = Client()


def build_entity(csvline: str) -> Entity:
    room = csvline.rstrip().split(";")
    e = Entity("RoomObserved", f"{room[0]}:{iso8601.utcnow()}")
    e.obs()
    e.prop("temperature", room[1])
    e.prop("pressure", float(room[1]))
    return e


@app.route("/", methods=["POST"])
def upload_file():
    file = request.files["file"]
    csvlines = io.TextIOWrapper(file).readlines()
    entities = [build_entity(csvline) for csvline in csvlines]
    client.upsert(entities)
    return Response("CSV file processed", status=200)
