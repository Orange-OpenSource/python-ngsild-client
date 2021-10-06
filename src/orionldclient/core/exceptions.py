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

from dataclasses import dataclass
from requests.exceptions import HTTPError, ContentDecodingError, RequestException
from requests import Response
from ..exceptions import NgsiError


@dataclass
class ProblemDetails:  # rfc7807
    type: str = ""
    title: str = ""
    detail: str = ""
    status: int = 400
    instance: str = None
    extension: dict = None


class NgsiApiError(NgsiError):
    pass


class NgsiContextBrokerError(NgsiApiError):
    def __init__(self, pd: ProblemDetails):
        self.pd = pd
        self.message = f"{pd.title} : {pd.detail}"
        super().__init__(self.message)


class NgsiHttpError(NgsiApiError):
    def __init__(self, statuscode: int):
        self.statuscode = statuscode
        self.message = f"HTTP {statuscode} error"
        super().__init__(self.message)


class NgsiNotConnectedError(NgsiError):
    pass


def rfc7807_error_handle(func):
    def inner_function(*args, **kwargs):
        err = {}
        try:
            return func(*args, **kwargs)
        except HTTPError as e:
            r: Response = e.response
            try:
                err: dict = r.json()
            except ContentDecodingError:
                raise NgsiHttpError(r.status_code) from e
            pd = ProblemDetails(
                err.pop("type", "about:blank"),
                err.pop("title", ""),
                err.pop("detail", ""),
                r.status_code,
                err.pop("instance", None),
            )
            pd.extension = err | {"internal_client_funcname": func.__qualname__}
            raise NgsiContextBrokerError(pd) from e
        except RequestException as e:
            raise NgsiApiError("Error while requesting the broker API") from e

    return inner_function
