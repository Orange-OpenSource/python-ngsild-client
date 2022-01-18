#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.
# SPDX-License-Identifier: Apache-2.0

import http.client
import logging

__version__ = "0.1.1"

from .utils import iso8601
from .utils.uuid import shortuuid
from .model.entity import Entity
from .model.helper.postal import PostalAddressBuilder
from .model.helper.openinghours import OpeningHoursBuilder
from .model.constants import CORE_CONTEXT, NESTED, Auto, SmartDataModels, Rel
from .api.client import Client
from .exceptions import NgsiError
from .model.exceptions import NgsiModelError
from .api.exceptions import NgsiApiError, NgsiContextBrokerError, NgsiAlreadyExistsError


__all__ = [
    "iso8601",
    "shortuuid",
    "Entity",
    "PostalAddressBuilder",
    "OpeningHoursBuilder",
    "CORE_CONTEXT",
    "NESTED",
    "Auto",
    "Rel",
    "Client",
    "SmartDataModels",
    "NgsiError",
    "NgsiModelError",
    "NgsiApiError",
    "NgsiContextBrokerError",
    "NgsiAlreadyExistsError",
]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

http.client.HTTPConnection.debuglevel = 1


def print_to_log(*args):
    logger.debug(" ".join(args))


# monkey patch the http.client's print() function
http.client.print = print_to_log
