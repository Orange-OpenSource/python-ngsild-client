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

"""
This module contains a few helper functions to deal with UUIDs.
"""

import uuid
from base64 import b64encode

def uuidshortener(uuid: uuid.UUID) -> str:
    # like in urlsafe_base64encode() but ~ replaces -
    return b64encode(uuid.bytes, altchars=b'~_').decode().rstrip("=")


def shortuuid(random: bool = False) -> str:
    uid = uuid.uuid1() if random else uuid.uuid4()
    return uuidshortener(uid)