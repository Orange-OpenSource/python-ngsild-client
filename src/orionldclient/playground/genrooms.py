#!/usr/bin/env python3

# Software Name: python-orion-client
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battelo@orange.com> et al.
# SPDX-License-Identifier: Apache-2.0

from typing import Generator

from dataclasses import dataclass
from datetime import datetime, timedelta
from random import triangular, gauss

from .walker import RandomWalker
from ..model.entity import Entity


@dataclass
class RoomObserved:
    number: int
    ts: datetime
    temperature: float
    humidity: float

    def to_ngsild(self) -> Entity:
        room: Entity = Entity(
            f"urn:ngsi-ld:Building:building-a85e3da145c1:RoomObserved:Room{self.number}",
            "Room",
        )
        room.prop("temperature", self.temperature, observedat=self.ts)
        room.prop("relativeHumidity", self.humidity, observedat=self.ts)
        return room


class RoomWalker:
    def __init__(self, room: RoomObserved, delta: timedelta = timedelta(minutes=5)):
        self.room = room
        self.delta = delta
        self._temperature = RandomWalker(room.temperature)
        self._humidity = RandomWalker(room.humidity, 0.05)

    def __repr__(self):
        return self.room.__repr__()

    def walk(self):
        self.room.ts += self.delta
        self.room.temperature = self._temperature.walk()
        self.room.humidity = self._humidity.walk()
        return self


def gen_fake_room_entities(
    nrooms: int = 9,
    start: datetime = datetime.utcnow(),
    step: timedelta = timedelta(minutes=5),
) -> Generator[Entity, None, None]:

    # init rooms
    rooms: list[RoomObserved] = [
        RoomObserved(
            x, start, round(triangular(18, 26, 22), 2), round(gauss(0.4, 0.2), 2)
        )
        for x in range(1, nrooms + 1)
    ]
    roomwalkers: list[RoomWalker] = [RoomWalker(room, step) for room in rooms]

    # walk
    while True:
        yield from (wroom.room.to_ngsild() for wroom in roomwalkers)
        for wroom in roomwalkers:
            wroom.walk()
