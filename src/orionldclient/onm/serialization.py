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

from typing import Protocol

from orionldclient.model.ngsidict import NgsiDict


class NgsiSerializationProtocol(Protocol):
    def __ngsild__to__(self) -> str:
        ...

    @classmethod
    def __ngsild__from__(payload: NgsiDict):
        ...
