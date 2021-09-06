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

import re

NID_PATTERN = re.compile(r"^urn:([0-9a-zA-Z\-]+):")


def get_nid(urn: str) -> str:
    m = NID_PATTERN.match(urn)
    return m.group(1) if m else None


def is_prefixed(uri: str) -> bool:
    return get_nid(uri) is not None


def prefix(nid: str, uri: str) -> str:
    if is_prefixed(uri):
        return uri
    else:
        return f"urn:{nid}:{uri}"
