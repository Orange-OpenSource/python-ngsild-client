#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from __future__ import annotations
from typing import Union
from dataclasses import dataclass
from datetime import time
from enum import Enum

TimeOrStr = Union[time, str]  # type alias


class WeekDay(Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


WEEK = [day for day in WeekDay]
WEEK_END = [WeekDay.SATURDAY, WeekDay.SUNDAY]
WORKING_DAYS = [day for day in WEEK if day not in WEEK_END]


@dataclass
class OpeningHoursSpecification:
    """An OpeningHoursSpecification as described here : https://schema.org/OpeningHoursSpecification

    Simplified. Support a single open timeslot per day.
    """

    opens: str
    closes: str
    dayofweek: str

    def to_dict(self):
        return {"opens": self.opens, "closes": self.closes, "dayOfWeek": self.dayofweek}


class OpeningHoursBuilder:
    """A helper class that allows to easily build an openingHours property.

    Simplified. Support a single open timeslot per day.

    Example
    -------
    >>> from ngsildclient import *
    >>> builder = OpeningHoursBuilder()
    >>> openinghours = builder.businessdays("10:00", "17:30").saturday("10:00", "14:00").build()
    >>> # Add an openingHours property to the entity you're creating
    >>> library = Entity("Library", "MyLibrary")
    >>> library.prop("openingHours", openinghours)
    >>> library.pprint()
    {
        "@context": [
            "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
        ],
        "id": "urn:ngsi-ld:Library:MyLibrary",
        "type": "Library",
        "openingHours": {
            "type": "Property",
            "value": [
            {
                "opens": "10:00",
                "closes": "17:30",
                "dayOfWeek": "Monday"
            },
            {
                "opens": "10:00",
                "closes": "17:30",
                "dayOfWeek": "Tuesday"
            },
            {
                "opens": "10:00",
                "closes": "17:30",
                "dayOfWeek": "Wednesday"
            },
            {
                "opens": "10:00",
                "closes": "17:30",
                "dayOfWeek": "Thursday"
            },
            {
                "opens": "10:00",
                "closes": "17:30",
                "dayOfWeek": "Friday"
            },
            {
                "opens": "10:00",
                "closes": "14:00",
                "dayOfWeek": "Saturday"
            }
            ]
        }
    }
    """

    def __init__(self):
        self._oh: dict = {}

    @staticmethod
    def _converttimes(opens, closes) -> tuple[str, str]:
        opens = opens if isinstance(opens, str) else opens.strftime("%H:%M")
        closes = closes if isinstance(closes, str) else closes.strftime("%H:%M")
        return opens, closes

    def monday(self, opens: TimeOrStr, closes: TimeOrStr):
        opens, closes = OpeningHoursBuilder._converttimes(opens, closes)
        self._oh[WeekDay.MONDAY] = OpeningHoursSpecification(
            opens, closes, WeekDay.MONDAY.value
        )
        return self

    def tuesday(self, opens: TimeOrStr, closes: TimeOrStr):
        opens, closes = OpeningHoursBuilder._converttimes(opens, closes)
        self._oh[WeekDay.TUESDAY] = OpeningHoursSpecification(
            opens, closes, WeekDay.TUESDAY.value
        )
        return self

    def wednesday(self, opens: TimeOrStr, closes: TimeOrStr):
        opens, closes = OpeningHoursBuilder._converttimes(opens, closes)
        self._oh[WeekDay.WEDNESDAY] = OpeningHoursSpecification(
            opens, closes, WeekDay.WEDNESDAY.value
        )
        return self

    def thursday(self, opens: TimeOrStr, closes: TimeOrStr):
        opens, closes = OpeningHoursBuilder._converttimes(opens, closes)
        self._oh[WeekDay.THURSDAY] = OpeningHoursSpecification(
            opens, closes, WeekDay.THURSDAY.value
        )
        return self

    def friday(self, opens: TimeOrStr, closes: TimeOrStr):
        opens, closes = OpeningHoursBuilder._converttimes(opens, closes)
        self._oh[WeekDay.FRIDAY] = OpeningHoursSpecification(
            opens, closes, WeekDay.FRIDAY.value
        )
        return self

    def saturday(self, opens: TimeOrStr, closes: TimeOrStr):
        opens, closes = OpeningHoursBuilder._converttimes(opens, closes)
        self._oh[WeekDay.SATURDAY] = OpeningHoursSpecification(
            opens, closes, WeekDay.SATURDAY.value
        )
        return self

    def sunday(self, opens: TimeOrStr, closes: TimeOrStr):
        opens, closes = OpeningHoursBuilder._converttimes(opens, closes)
        self._oh[WeekDay.SUNDAY] = OpeningHoursSpecification(
            opens, closes, WeekDay.SUNDAY.value
        )
        return self

    def days(self, opens: TimeOrStr, closes: TimeOrStr, *days):
        opens, closes = OpeningHoursBuilder._converttimes(opens, closes)
        for day in days:
            self._oh[day] = OpeningHoursSpecification(opens, closes, day.value)
        return self

    def weekend(self, opens: TimeOrStr, closes: TimeOrStr):
        return self.days(opens, closes, *WEEK_END)

    def businessdays(self, opens: TimeOrStr, closes: TimeOrStr, *exceptdays):
        openingdays = [day for day in WORKING_DAYS if day not in exceptdays]
        return self.days(opens, closes, *openingdays)

    def wholeweek(self, opens: TimeOrStr, closes: TimeOrStr, *exceptdays):
        return self.days(opens, closes, *WEEK)

    def build(self) -> dict:
        openingdays = []
        for day in WeekDay:
            if oh := self._oh.get(day, None):
                openingdays.append(oh.to_dict())
        return openingdays
