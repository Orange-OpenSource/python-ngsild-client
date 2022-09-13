#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

# TODO

import io

from ngsildclient import Entity, Client, iso8601, Auto

from flask import Flask, flash, request, redirect, url_for, Response
from werkzeug.utils import secure_filename

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
