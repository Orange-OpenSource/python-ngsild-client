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
from typing import TYPE_CHECKING, Tuple, List
from dataclasses import dataclass, field

import logging

from rich.console import Console
from rich.text import Text

if TYPE_CHECKING:
    from .client import Client

from .constants import BATCHSIZE
from ngsildclient.utils.console import Console
from .exceptions import NgsiApiError, rfc7807_error_handle
from ..model.entity import Entity


logger = logging.getLogger(__name__)

@dataclass
class BatchResult:
    success: List = field(default_factory=list)
    errors: List = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.errors == []

    @property
    def n_ok(self) -> int:
        return len(self.success)

    @property
    def n_err(self) -> int:
        return len(self.errors)

    @property
    def ratio(self) -> float:
        r = self.n_ok / (self.n_ok + self.n_err)
        return round(r, 2)

    @property
    def level(self) -> str:
        if self.ratio == 0.0:
            return "error"
        elif self.ratio < 1.0:
            return "warning"
        else:
            return "success"

    def __iadd__(self, r: BatchResult):
        self.success.extend(r.success)
        self.errors.extend(r.errors)
        return self


class BatchOp:
    """A wrapper for the NGSI-LD API batch endpoint."""    

    def __init__(self, client: Client, url: str):
        self._client = client
        self._session = client.session
        self.url = url
        self.console = Console()

    @rfc7807_error_handle
    def _create(
        self, entities: List[Entity]) -> BatchResult:
        r = self._session.post(
            f"{self.url}/create/", json=[entity._payload for entity in entities]
        )
        self._client.raise_for_status(r)
        if r.status_code == 201:
            success, errors = r.json(), []
        elif r.status_code == 207:
            content = r.json()
            success, errors = content["success"], content["errors"]
        else:
            raise NgsiApiError("Batch Create : Unkown HTTP response code {}", r.status_code)
        return BatchResult(success, errors)

    @rfc7807_error_handle
    def create(self, entities: List[Entity], batchsize: int = BATCHSIZE) -> BatchResult:
        r = BatchResult()
        for i in range(0, len(entities), batchsize):
            r += self._create(entities[i:i+batchsize])
        self.console.message(f"Entities created : {r.n_ok}/{r.n_err} [{r.ratio:.2f}]", level=r.level)
        return r
    
    @rfc7807_error_handle
    def _upsert(self, entities: List[Entity]) -> BatchResult:
        r = self._session.post(
            f"{self.url}/upsert/", json=[entity._payload for entity in entities]
        )
        self._client.raise_for_status(r)
        if r.status_code == 201:
            success, errors = r.json(), []
        elif r.status_code == 204:
            success, errors = [e.id for e in entities], []
        elif r.status_code == 207:
            content = r.json()
            success, errors = content["success"], content["errors"]
        else:
            raise NgsiApiError("Batch Upsert : Unkown HTTP response code {}", r.status_code)
        return BatchResult(success, errors)

    @rfc7807_error_handle
    def upsert(self, entities: List[Entity], batchsize: int = BATCHSIZE) -> BatchResult:
        r = BatchResult()
        for i in range(0, len(entities), batchsize):
            r += self._upsert(entities[i:i+batchsize]) 
        self.console.message(f"Entities upserted : {r.n_ok}/{r.n_err} [{r.ratio:.2f}]", level=r.level)
        return r

    @rfc7807_error_handle
    def _update(self, entities: List[Entity]) -> tuple[bool, dict]:
        r = self._session.post(
            f"{self.url}/update/", json=[entity._payload for entity in entities]
        )
        self._client.raise_for_status(r)
        if r.status_code == 204:
            success, errors = [e.id for e in entities], []
        elif r.status_code == 207:
            content = r.json()
            success, errors = content["success"], content["errors"]
        else:
            raise NgsiApiError("Batch Update : Unkown HTTP response code {}", r.status_code)
        return BatchResult(success, errors)

    @rfc7807_error_handle
    def update(self, entities: List[Entity], batchsize: int = BATCHSIZE) -> BatchResult:
        r = BatchResult()
        for i in range(0, len(entities), batchsize):
            r += self._update(entities[i:i+batchsize]) 
        self.console.message(f"Entities updated : {r.n_ok}/{r.n_err} [{r.ratio:.2f}]", level=r.level)
        return r

    @rfc7807_error_handle
    def _delete(self, entities: List[Entity]) -> tuple[bool, dict]:
        r = self._session.post(
            f"{self.url}/delete/", json=[entity.id for entity in entities]
        )
        self._client.raise_for_status(r)
        if r.status_code == 204:
            success, errors = [e.id for e in entities], []
        elif r.status_code == 207:
            content = r.json()
            success, errors = content["success"], content["errors"]
        else:
            raise NgsiApiError("Batch Delete : Unkown HTTP response code {}", r.status_code)
        return BatchResult(success, errors)

    @rfc7807_error_handle
    def delete(self, entities: List[Entity], batchsize: int = BATCHSIZE) -> BatchResult:
        r = BatchResult()
        for i in range(0, len(entities), batchsize):
            r += self._delete(entities[i:i+batchsize]) 
        self.console.message(f"Entities deleted : {r.n_ok}/{r.n_err} [{r.ratio:.2f}]", level=r.level)
        return r
