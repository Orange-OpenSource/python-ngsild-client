#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from dataclasses import dataclass
from ...model.constants import CORE_CONTEXT


@dataclass
class NotificationParams:
    uri: str
    attrs: list[str] = None
    format: str = "normalized"

    def to_dict(self) -> dict:
        d = {}
        if self.attrs:
            d["attributes"] = self.attrs
        d["format"] = self.format
        d["endpoint"] = {"uri": self.uri, "accept": "application/ld+json"}
        return d


@dataclass
class Subscription:
    notification: NotificationParams
    id: str = None
    type: str = "Subscription"
    name: str = None
    description: str = None
    entities: list[dict] = None  # id, idPattern, or type
    watched_attrs: list[str] = None
    # time_interval: int = 0
    query: str = None
    # gquery: str = None
    # csf: str = None
    active: bool = True
    # expiresat: datetime = None
    # throttling: int = 0
    # tquery: str = None
    # scope: str = None
    # lang: str = None
    ctx: str = CORE_CONTEXT

    def to_dict(self) -> dict:
        d = {}
        if self.id:
            d["id"] = self.id
        d["type"] = self.type
        if self.name:
            d["name"] = self.name
        if self.description:
            d["description"] = self.description
        if self.entities:
            d["entities"] = self.entities
        if self.watched_attrs:
            d["watchedAttributes"] = self.watched_attrs
        if self.query:
            d["q"] = self.query
        d["isActive"] = self.active
        d["notification"] = self.notification.to_dict()
        d["@context"] = self.ctx
        return d


class SubscriptionBuilder:
    def __init__(
        self,
        uri: str,
    ):
        notification = NotificationParams(uri)
        self._subscr = Subscription(notification)
        self._subscr.entities = []

    def id(self, value: str):
        if not isinstance(value, str):
            raise ValueError("id shall be a string")
        self._subscr.id = value
        return self

    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("name shall be a string")
        self._subscr.name = value
        return self

    def description(self, value: str):
        if not isinstance(value, str):
            raise ValueError("description shall be a string")
        self._subscr.description = value
        return self

    def select_id(self, value: str):
        if not isinstance(value, str):
            raise ValueError("EntitySelector id shall be a string")
        self._subscr.entities.append({"id": value})
        return self

    def select_idpattern(self, value: str):
        if not isinstance(value, str):
            raise ValueError("EntitySelector idPattern shall be a string")
        self._subscr.entities.append({"idPattern": value})
        return self

    def select_type(self, value: str):
        if not isinstance(value, str):
            raise ValueError("EntitySelector type shall be a string")
        self._subscr.entities.append({"type": value})
        return self

    def watch(self, value: list[str]):
        if not isinstance(value, list):
            raise ValueError("watchedAttributes shall be a list of strings")
        if value == []:
            raise ValueError("Empty array is not allowed")
        self._subscr.watched_attrs = value
        return self

    def query(self, value: str):
        if not isinstance(value, str):
            raise ValueError("query shall be a string")
        self._subscr.query = value
        return self

    def notif(self, value: list[str]):
        if not isinstance(value, list):
            raise ValueError("attribute names shall be a list of strings")
        if value == []:
            raise ValueError("Empty array is not allowed")
        self._subscr.notification.attrs = value
        return self

    def context(self, value: str):
        if not isinstance(value, str):
            raise ValueError("context shall be a string")
        self._subscr.ctx = value
        return self

    def build(self) -> dict:
        if self._subscr.entities == [] and self._subscr.watched_attrs is None:
            raise ValueError(
                "At least one of (a) entities or (b) watchedAttributes shall be present."
            )
        return self._subscr.to_dict()
