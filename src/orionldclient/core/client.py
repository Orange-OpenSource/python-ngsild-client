#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0

import logging

from requests.sessions import Session
from dataclasses import dataclass

from typing import Optional

from .constants import *
from .exceptions import *
from . import http


logger = logging.getLogger(__name__)


@dataclass
class Broker:
    vendor: Vendor = Vendor.UNKNOWN
    version: str = "N/A"


class Client:
    def __init__(
        self,
        hostname="localhost",
        port=NGSILD_DEFAULT_PORT,
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

        logger.info("Connecting client ...")
        # self._entities = Entities(self, f"{self.url}{ENDPOINT_ENTITIES}", version)

        # get status and retrieve Context Broker information
        status = self.is_connected(raise_for_disconnected=True)
        if status:
            self.broker = Broker(*self.guess_vendor())
            print(self._welcome_message())
        else:
            print(self._fail_message())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def is_connected(self, raise_for_disconnected=False) -> bool:
        url = f"{self.url}/{ENDPOINT_ENTITIES}"
        params = {"type": "None", "limit": 0, "count": "true"}
        try:
            r = self.session.get(
                url,
                headers={
                    "Accept": "application/json",
                    "Content-Type": None,
                },  # overrides session headers
                params=params,
            )
            r.raise_for_status()
        except Exception as e:
            if raise_for_disconnected:
                raise NgsiNotConnectedError("Cannot connect to Context Broker") from e
            else:
                logger.error(e)
                return False
        return True

    def broker_version_orionld(self) -> Optional[str]:
        url = f"{self.url}/version"
        headers = {
            "Accept": "application/json",
            "Content-Type": None,
        }  # overrides session headers
        try:
            r = self.session.get(url, headers=headers)
            r.raise_for_status()
            return r.json()["orionld version"]
        except Exception:
            return None

    def broker_version_scorpio(self) -> Optional[str]:
        url = f"{self.url}/scorpio/v1/info/health"
        headers = {
            "Accept": "application/json",
            "Content-Type": None,
        }  # overrides session headers
        try:
            r = self.session.get(url, headers=headers)
            r.raise_for_status()
            return "N/A"
        except Exception:
            return None

    def broker_version_stellio(self) -> Optional[str]:
        url = f"{self.url}/actuator/health"
        headers = {
            "Accept": "application/json",
            "Content-Type": None,
        }  # overrides session headers
        try:
            r = self.session.get(url, headers=headers)
            r.raise_for_status()
            return "N/A"
        except Exception:
            return None

    def guess_vendor(self) -> tuple[Vendor, Version]:
        if version := self.broker_version_orionld():
            return Vendor.ORIONLD, version
        if version := self.broker_version_scorpio():
            return Vendor.SCORPIO, version
        if version := self.broker_version_stellio():
            return Vendor.STELLIO, version
        return Vendor.UNKNOWN, "N/A"

    @property
    def version(self) -> str:
        return __version__

    @property
    def entities(self):
        return self._entities

    @property
    def subscriptions(self):
        return self._subscriptions

    def _welcome_message(self) -> str:
        return f"Connected to Context Broker at {self.hostname}:{self.port} | vendor={self.broker.vendor.value} version={self.broker.version}"

    def _fail_message(self) -> str:
        return f"Failed to connect to Context Broker at {self.hostname}:{self.port}"

    def close(self):
        self.session.close()
