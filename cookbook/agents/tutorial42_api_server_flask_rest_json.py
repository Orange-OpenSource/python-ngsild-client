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
# Usage : flask --app tutorial42_api_server_flask_rest_json run
# Usage : curl -X POST -H "Content-Type: application/json" -d "@data/room.json" http://127.0.0.1:5000/rooms

from flask import Flask, request, jsonify
from ngsildclient import Entity, Client, iso8601

app = Flask(__name__)
client = Client()


def build_entity(room: dict) -> Entity:
    e = Entity("RoomObserved", f"{room['id']}:{iso8601.utcnow()}")
    e.obs()
    e.prop("temperature", room["temperature"])
    e.prop("pressure", room["pressure"])
    return e


@app.route("/rooms", methods=["POST"])
def post_room():
    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return
    entity = build_entity(request.json)
    client.upsert(entity)
    resp = jsonify(entity.to_dict())
    resp.headers = {"Content-Location": client.entities.to_broker_url(entity)}
    resp.status_code = 201
    return resp
