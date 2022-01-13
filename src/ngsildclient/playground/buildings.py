#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.
# SPDX-License-Identifier: Apache-2.0

import itertools
import logging

from typing import Generator

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from random import triangular, gauss

from ngsildclient.model.constants import Auto

from .walker import RandomWalker, shortuuid
from ..model.entity import Entity

logger = logging.getLogger(__name__)


@dataclass
class RoomSensorObserved:
    building: str
    number: int
    ts: datetime
    temperature: float
    humidity: float

    def _to_ngsild(self) -> Entity:
        room = Entity(
            "Room",
            f"{self.building}:RoomSensorObserved:Room{self.number}"
        )
        room.tprop("dateObserved", self.ts)
        room.prop("temperature", self.temperature, observedat=Auto)
        room.prop("relativeHumidity", self.humidity, observedat=Auto)
        room.rel("isLocatedIn", self.building)
        return room


class RoomSensorWalker:
    def __init__(
        self,
        room: RoomSensorObserved,
        delta: timedelta = timedelta(minutes=5),
    ):
        self.room = room
        self.delta = delta
        self._temperature = RandomWalker(room.temperature)
        self._humidity = RandomWalker(room.humidity, 0.05)

    def __repr__(self):
        return self.room.__repr__()

    def walk(self):
        r = self.room
        new = RoomSensorObserved(
            r.building,
            r.number,
            r.ts + self.delta,
            self._temperature.walk(),
            self._humidity.walk(),
        )
        self.room = new
        return new


class RoomSensorGenerator:
    def __init__(
        self,
        nrooms: int = 1,
        start: timedelta = timedelta(hours=1),
        step: timedelta = timedelta(minutes=5),
    ):
        self.building = f"FakeBuilding-{shortuuid()}"
        self.nrooms = nrooms
        self.period = start
        self.step = step

        start = datetime.utcnow() - start
        # init rooms sensors
        self.rooms: list[RoomSensorObserved] = [
            RoomSensorObserved(
                self.building,
                x,
                start,
                round(triangular(18, 26, 22), 2),
                round(gauss(0.4, 0.2), 2),
            )
            for x in range(1, nrooms + 1)
        ]

        # init walkers
        self.walkers: list[RoomSensorWalker] = [
            RoomSensorWalker(room, step) for room in self.rooms
        ]

    @property
    def generator(self):
        return self._itermeasures()

    def _itermeasures(self) -> Generator[Entity, None, None]:
        yield from (room for room in self.rooms)  # initial values
        # walk
        for _ in range(int(self.period / self.step) - 1):
            yield from (walker.walk() for walker in self.walkers)

    def history(self, upto: datetime = datetime.utcnow()) -> list[Entity]:
        return [*itertools.takewhile(lambda room: room.ts < upto, self.generator)]
