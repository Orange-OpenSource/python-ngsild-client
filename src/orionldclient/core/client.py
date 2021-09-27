#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0

import logging

from requests.sessions import Session
from dataclasses import dataclass

from typing import Optional
from datetime import datetime, timedelta

from .constants import *
from .exceptions import *
from . import http


logger = logging.getLogger(__name__)


@dataclass
class Broker:
    type: Vendor
    version: str
    starttime: datetime
    _laststatus: dict = {}


class Client:
    def __init__(
        self,
        hostname="127.0.0.1",
        port="1026",
        secure=False,
        useragent=UA,
        tenant=None,
        upsert=False,
        proxy=None,
    ):
        self.hostname = hostname
        self.port = port
        self.secure = secure
        self.scheme = "https" if secure else "http"
        self.url = f"{self.scheme}://{hostname}:{port}"
        self.basepath = f"{self.url}/{NGSILD_PATH}"
        self.useragent = useragent
        self.tenant = tenant
        self.upsert = upsert
        self.proxy = proxy
        # self.headers = {"User-Agent": self.useragent, "Accept": "application/json"}
        # self.headers_ngsi_get = {
        #     "User-Agent": self.useragent,
        #     "Accept": "application/ld+json",
        # }
        # self.headers_ngsi_post = {
        #     "User-Agent": self.useragent,
        #     "Content-Type": "application/ld+json",
        # }

        self.session = Session()
        self.session.headers = {
            "User-Agent": self.useragent,
            "Accept": "application/ld+json",
            "Content-Type": "application/ld+json",
        }
        if tenant is not None:
            self.session.headers["NGSILD-Tenant"] = tenant
        if proxy:
            self.session.proxies = {proxy}

        self.broker: Broker = None

        logger.info("Connecting client ...")
        # self._entities = Entities(self, f"{self.url}{ENDPOINT_ENTITIES}", version)

        self.starttime = datetime.now()
        self._broker_version = "N/A"
        self._broker_starttime: datetime = None

        # get status and check connection
        status = self.status(raise_for_disconnected=True)
        if status:
            self._broker_starttime = datetime.now() - self.uptime(status)
            self._broker_version = status["orionld version"]
            print(self._welcome_message())
        else:
            print(self._fail_message())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        logger.info("close session 1")
        self.close()

    @property
    def version(self) -> str:
        return __version__

    @property
    def broker_version(self) -> str:
        return self._broker_version

    @property
    def broker_starttime(self) -> Optional[datetime]:
        return self._broker_starttime

    @property
    def entities(self):
        return self._entities

    @property
    def subscriptions(self):
        return self._subscriptions

    def status_OLD(self, raise_for_disconnected=False) -> Optional[dict]:
        logger.info(f"{self.url=}")
        url = f"{self.url}{ENDPOINT_STATUS}"
        logger.info(url)
        _status = None
        try:
            _status = http.get(
                self.session,
                url,
                headers={"Accept": "application/json", "Content-Type": None}, # overrides session headers
                proxy=self.proxy,
            )
            print(_status)
        except Exception as e:
            logger.error(e)
            if raise_for_disconnected:
                raise NgsiNotConnectedError("Cannot connect to Context Broker") from e
        if isinstance(_status, dict) and "orionld version" in _status:
            return _status
        return None

    def status(self, raise_for_disconnected=False) -> Optional[Broker]:
        logger.info(f"{self.url=}")
        url = f"{self.url}{ENDPOINT_STATUS}"
        logger.info(url)
        _status = None
        try:
            _status = http.get(
                self.session,
                url,
                headers={"Accept": "application/json", "Content-Type": None}, # overrides session headers
                proxy=self.proxy,
            )
            print(_status)
        except Exception as e:
            logger.error(e)
            if raise_for_disconnected:
                raise NgsiNotConnectedError("Cannot connect to Context Broker") from e
        if isinstance(_status, dict):
            if "orionld version" in _status:
                broker = Broker(Vendor.ORIONLD, _status["uptime"], _status["orionld version"], _status)
            else:
                broker = Broker(Vendor.UNKNOWN, None, None)
            return broker
        return None

    def is_connected(self) -> bool:
        return self.status() is not None

    def uptime(self, status: dict = None) -> timedelta:
        if status is None:
            status = self.status()
        uptime = status["uptime"]
        d, h, m, s = [int(x.split(" ")[0]) for x in uptime.split(", ")]
        return timedelta(days=d, hours=h, minutes=m, seconds=s)

    def _welcome_message(self) -> str:
        return f"Connected to Context Broker at {self.hostname}:{self.port} [{self.broker_version}]"

    def _fail_message(self) -> str:
        return f"Failed to connect to Context Broker at {self.hostname}:{self.port}"

    def close(self):
        logger.info("close session 2")
        self.session.close()
