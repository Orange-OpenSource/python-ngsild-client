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

from typing import TYPE_CHECKING, List, Literal, Sequence
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from ngsildclient.model.constants import EntityOrId

import logging

if TYPE_CHECKING:
    from .client import Client

from .constants import BATCHSIZE
from ngsildclient.utils.console import Console, MsgLvl
from .exceptions import NgsiApiError, rfc7807_error_handle
from ..model.entity import Entity

BatchOp = Literal["create", "upsert", "update", "delete"]

logger = logging.getLogger(__name__)

@dataclass
class BatchResult:
    op: BatchOp = "N/A"
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
    def n_tot(self) -> int:
        return self.n_ok + self.n_err

    @property
    def ratio(self) -> float:
        r = self.n_ok / (self.n_ok + self.n_err)
        return round(r, 2)

    @property
    def level(self) -> MsgLvl:
        if self.ratio == 0.0:
            return "error"
        elif self.ratio < 1.0:
            return "warning"
        else:
            return "success"

    def raise_for_status(self):
        if not self.ok:
            raise NgsiApiError(f"Error while processing batch {self.op} operation", self)

    def __iadd__(self, r: BatchResult):
        self.success.extend(r.success)
        self.errors.extend(r.errors)
        return self


class Batch:
    """A wrapper for the NGSI-LD API batch endpoint."""    

    def __init__(self, client: Client, url: str):
        self._client = client
        self._session = client.session
        self.url = url
        self.console = Console()

    @rfc7807_error_handle
    def _create(
        self, entities: Sequence[Entity]) -> BatchResult:
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
        return BatchResult("create", success, errors)

    @rfc7807_error_handle
    def create(self, entities: Sequence[Entity], *, batchsize: int = BATCHSIZE) -> BatchResult:
        r = BatchResult("create")
        for i in range(0, len(entities), batchsize):
            r += self._create(entities[i:i+batchsize])
        self.console.message(f"Entities created : {r.n_ok}/{r.n_tot} [{r.ratio:.2f}]", level=r.level)
        return r
    
    @rfc7807_error_handle
    def _upsert(self, entities: Sequence[Entity]) -> BatchResult:
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
        return BatchResult("upsert", success, errors)

    @rfc7807_error_handle
    def upsert(self, entities: Sequence[Entity], *, batchsize: int = BATCHSIZE) -> BatchResult:
        r = BatchResult("upsert")
        for i in range(0, len(entities), batchsize):
            r += self._upsert(entities[i:i+batchsize]) 
        self.console.message(f"Entities upserted : {r.n_ok}/{r.n_tot} [{r.ratio:.2f}]", level=r.level)
        return r

    @rfc7807_error_handle
    def _update(self, entities: Sequence[Entity]) -> BatchResult:
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
        return BatchResult("update", success, errors)

    @rfc7807_error_handle
    def update(self, entities: Sequence[Entity], *, batchsize: int = BATCHSIZE) -> BatchResult:
        r = BatchResult("update")
        for i in range(0, len(entities), batchsize):
            r += self._update(entities[i:i+batchsize]) 
        self.console.message(f"Entities updated : {r.n_ok}/{r.n_tot} [{r.ratio:.2f}]", level=r.level)
        return r

    @rfc7807_error_handle
    def _delete(self, entities: Sequence[EntityOrId]) -> BatchResult:
        r = self._session.post(
            f"{self.url}/delete/", json=[e.id if isinstance(e, Entity) else e for e in entities]
        )
        self._client.raise_for_status(r)
        if r.status_code == 204:
            success, errors = [e.id for e in entities], []
        elif r.status_code == 207:
            content = r.json()
            success, errors = content["success"], content["errors"]
        else:
            raise NgsiApiError("Batch Delete : Unkown HTTP response code {}", r.status_code)
        return BatchResult("delete", success, errors)

    @rfc7807_error_handle
    def delete(self, entities: Sequence[EntityOrId], *, batchsize: int = BATCHSIZE) -> BatchResult:
        r = BatchResult("delete")
        for i in range(0, len(entities), batchsize):
            r += self._delete(entities[i:i+batchsize]) 
        self.console.message(f"Entities deleted : {r.n_ok}/{r.n_tot} [{r.ratio:.2f}]", level=r.level)
        return r
