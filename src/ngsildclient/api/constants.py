#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

"""This module contains constants used in the api package.
"""

from typing import TYPE_CHECKING, Union, Sequence
from enum import Enum, unique

from ngsildclient import __version__

Version = str

@unique
class Vendor(Enum):
    ORIONLD = "Orion-LD"
    SCORPIO = "Scorpio"
    STELLIO = "Stellio"
    CASSIOPEIA = "Cassiopeia"
    UNKNOWN = None


@unique
class AttrsFormat(Enum):
    NORMALIZED = "normalized"
    KEYVALUES = "keyValues"
    VALUES = "values"


@unique
class LogLevel(Enum):
    NONE = "NONE"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"


@unique
class TimeProperty(Enum):
    OBSERVED_AT = "observedAt"
    MODIFIED_AT = "modifiedAt"
    CREATED_AT = "createdAt"

@unique
class AggrMethod(Enum):
    TOTAL_COUNT = "totalCount"
    DISTINCT_COUNT = "distinctCount"
    SUM = "sum"  
    AVERAGE = "avg"
    MINIMUM = "min"
    MAXIMUM = "max"
    STANDARD_DEVIATION = "stddev"
    SUM_SQUARES = "sumsq"


UA = f"ngsildclient v{__version__}"

NGSILD_PATH = "ngsi-ld"
NGSILD_VERSION = "v1"
NGSILD_BASEPATH = f"{NGSILD_PATH}/{NGSILD_VERSION}"
TEMPORAL_BASEPATH = "temporal"
NGSILD_DEFAULT_PORT_ORIONLD = 1026
NGSILD_DEFAULT_PORT_SCORPIO = 9090
NGSILD_DEFAULT_PORT_STELLIO = 8080
NGSILD_DEFAULT_PORT = NGSILD_DEFAULT_PORT_ORIONLD
NGSILD_TEMPORAL_PORT = NGSILD_DEFAULT_PORT

# JSON-LD Vocabulary at w3.org
JSONLD_CONTEXT = "http://www.w3.org/ns/json-ld#context"

# endpoints MUST NOT end with a slash
ENDPOINT_STATUS = "version"
ENDPOINT_ADMIN = "admin"
ENDPOINT_LOG = f"{ENDPOINT_ADMIN}/log"
ENDPOINT_ENTITIES = f"{NGSILD_BASEPATH}/entities"
ENDPOINT_BATCH = f"{NGSILD_BASEPATH}/entityOperations"
ENDPOINT_ALT_QUERY_ENTITIES = f"{ENDPOINT_BATCH}/query"
ENDPOINT_TYPES = f"{NGSILD_BASEPATH}/types"
ENDPOINT_CONTEXTS = f"{NGSILD_BASEPATH}/jsonldContexts"
ENDPOINT_SUBSCRIPTIONS = f"{NGSILD_BASEPATH}/subscriptions"
ENDPOINT_TEMPORAL = f"temporal/entities"
ENDPOINT_ALT_QUERY_TEMPORAL = "temporal/entityOperations/query"

PAGINATION_LIMIT_MAX = 100  # pagination
BATCHSIZE = 100  # maximum number of entities sent per batch operation

DEFAULT_ATTR_FORMAT = None  # Let Orion default value => AttrsFormat.NORMALIZED
DEFAULT_LOGLEVEL = LogLevel.WARN

WRITE_MODE_UPSERT = True
WRITE_MODE_IGNORE = False
DEFAULT_WRITE_MODE = WRITE_MODE_UPSERT

NOW = None
