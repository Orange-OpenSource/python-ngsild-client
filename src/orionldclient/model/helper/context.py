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


DEFAULT_CONTEXT = ["https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"]
EMPTY_CONTEXT = []


class ContextBuilder:
    def __init__(self, ctx: list[str] = None):
        self._ctx = list(DEFAULT_CONTEXT) if ctx is None else ctx

    def add(self, uri: str):
        self._ctx.append(uri)
        return self

    def remove(self, uri: str):
        self._ctx.remove(uri)
        return self

    def __repr__(self):
        return self._ctx.__repr__()

    def build(self):
        return self._ctx
