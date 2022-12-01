#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import http.client
import logging
import sys

__version__ = "0.5.2"

from ngsildclient.settings import globalsettings as settings
from .utils import iso8601, is_interactive
from .utils.uuid import shortuuid
from .model.entity import Entity, mkprop, mktprop, mkgprop, mkrel
from .model.helper.postal import PostalAddressBuilder
from .model.helper.openinghours import OpeningHoursBuilder
from .model.constants import CORE_CONTEXT, SmartDataModels, Rel, UTC, MultAttrValue
from .api.client import Client
from .api.asyn.client import AsyncClient
from .api.helper.subscription import SubscriptionBuilder
from .exceptions import NgsiError
from .model.exceptions import NgsiModelError
from .api.exceptions import NgsiApiError, NgsiContextBrokerError, NgsiAlreadyExistsError


__all__ = [
    "settings",
    "iso8601",
    "shortuuid",
    "mkprop",
    "mkgprop",
    "mktprop",
    "mkrel",
    "Entity",
    "AttrValue",
    "PostalAddressBuilder",
    "OpeningHoursBuilder",
    "CORE_CONTEXT",
    "Rel",
    "UTC",
    "MultAttrValue",
    "Client",
    "AsyncClient",
    "SubscriptionBuilder",
    "SmartDataModels",
    "NgsiError",
    "NgsiModelError",
    "NgsiApiError",
    "NgsiContextBrokerError",
    "NgsiAlreadyExistsError",
]

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
if is_interactive():
    logging.disable(logging.CRITICAL)
    sys.tracebacklimit = 0

logger = logging.getLogger(__name__)

http.client.HTTPConnection.debuglevel = 1


def print_to_log(*args):
    logger.debug(" ".join(args))


# monkey patch the http.client's print() function
http.client.print = print_to_log
