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
from typing import TYPE_CHECKING, Optional
import re
import json
import logging

if TYPE_CHECKING:
    from .client import Client

from ngsildclient.model.constants import CORE_CONTEXT
from .exceptions import rfc7807_error_handle


logger = logging.getLogger(__name__)


class Contexts:
    """A wrapper for the NGSI-LD API context endpoint."""
    def __init__(self, client: Client, url: str):
        self._client = client
        self._session = client.session
        self.url = url

    @rfc7807_error_handle
    def list(self, pattern: str = None) -> Optional[dict]:
        r = self._session.get(f"{self.url}")
        contexts = r.json()
        if pattern is not None:
            contexts = [x for x in contexts if re.search(pattern, x, re.IGNORECASE)]
        return contexts

    @rfc7807_error_handle
    def get(self, ctx: str) -> dict:
        r = self._session.get(f"{self.url}/{ctx}")
        self._client.raise_for_status(r)
        return r.json()

    @rfc7807_error_handle
    def _delete(self, ctx: str) -> bool:
        r = self._session.delete(f"{self.url}/{ctx}")
        self._client.raise_for_status(r)
        return bool(r)

    @rfc7807_error_handle
    def delete(self, ctx: str, pattern: str = None) -> bool:
        if pattern is None:
            return self._delete(ctx)
        deleted = False
        for ctx in self.list():
            if re.search(pattern, ctx, re.IGNORECASE):
                deleted |= self.delete(ctx)
        return deleted

    @rfc7807_error_handle
    def exists(self, ctx: str) -> bool:
        r = self._session.get(f"{self.url}/{ctx}")
        if r:
            payload = r.json()
            return "@context" in payload
        return False

    @rfc7807_error_handle
    def cleanup(self) -> None:
        """Delete all contexts except the Core context."""
        for ctx in self.list():
            if ctx != CORE_CONTEXT:
                self.delete(ctx)

    @rfc7807_error_handle
    def add(self, ctx: dict):
        if not ctx.get("@context"):
            raise ValueError("Expect a JSON object that has a top-level field named @context.")
        r = self._session.post(f"{self.url}/", json=ctx)
        self._client.raise_for_status(r)

    @rfc7807_error_handle
    def add_file(self, ctxfilename: str):
        with open(ctxfilename, "r") as fp:
            ctx = json.load(fp)
        self.add(ctx)
