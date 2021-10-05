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

import requests
import logging

from requests.sessions import Session
from .exceptions import *

EMPTY_JSON = "{}"

logger = logging.getLogger(__name__)

def _request(session: Session, method: str, url: str, **kwargs) -> requests.Response:

    logger.info("entering requests !!")
    response = EMPTY_JSON

    data = kwargs.get("data")
    is_post = data is not None

    logger.info(f"{data=}")
    is_delete = not is_post and method == "DELETE"
    proxy = kwargs.pop("proxy", None)
    proxies = {proxy} if proxy else None
    logger.info(f"{proxies=}")

    try:
        logger.info(f"{session.headers=}")
        
        r = session.request(method, url, **kwargs, proxies=proxies)

    except requests.exceptions.HTTPError as e:
        if is_post:
            raise NgsiHttpError(f"API HTTP error:\n{data=}", e)
        else:
            raise NgsiHttpError(f"API HTTP error", e)
    except Exception as e:
        raise NgsiNotConnectedError("Cannot connect to Context Broker", e)

    if r is None:
        raise NgsiContextBrokerError("No response")

    if is_delete:
        if r.status_code == 204:
            return True
        elif r.status_code == 404:
            return False

    r.raise_for_status()

    if is_post:
        return r.headers.get("Location")

    if not r.ok:
        raise NgsiContextBrokerError("A problem occured")

    if not r.content:
        return EMPTY_JSON

    try:

        response = r.json()

    except Exception as e:
        raise NgsiContextBrokerError("No JSON response")

    return response


def get(session: Session, url, **kwargs) -> requests.Response:
    headers = kwargs.get("headers", {})
    headers |= {"Content-Type": None}
    return _request(session, "GET", url, **kwargs)


def post(session: Session, url: str, payload: str, **kwargs) -> requests.Response:
    headers = kwargs.get("headers", {})
    headers |= {"Accept": None}
    return _request(session, "POST", url, data=payload, **kwargs)


def put(session: Session, url: str, payload: str, **kwargs) -> requests.Response:
    headers = kwargs.get("headers", {})
    headers |= {"Accept": None}

    return _request(session, "PUT", url, data=payload, **kwargs)


def patch(session: Session, url: str, payload: str, **kwargs) -> requests.Response:
    headers = kwargs.get("headers")
    headers |= {"Accept": None}
    return _request(session, "PATCH", url, data=payload, **kwargs)


def delete(session: Session, url: str, **kwargs) -> requests.Response:
    return _request(session, "DELETE", url, **kwargs)
