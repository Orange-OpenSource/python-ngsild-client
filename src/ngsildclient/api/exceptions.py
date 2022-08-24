#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

"""A module that covers NGSI-LD API exceptions.

When possible, Exceptions are mapped from the API Error Types,
and enriched thanks to the ProblemDetails added by the API.
"""

import logging
import httpx

from dataclasses import dataclass

from requests.exceptions import HTTPError, ContentDecodingError, RequestException
from requests import Response
from ..exceptions import NgsiError

logger = logging.getLogger(__name__)


@dataclass
class ProblemDetails:
    type: str
    title: str
    status: int
    detail: str
    instance: str = None
    extension: dict = None


class NgsiApiError(NgsiError):
    pass


class NgsiNotConnectedError(NgsiApiError):
    pass


class NgsiClientTooManyResultsError(NgsiApiError):
    pass


class NgsiHttpError(NgsiApiError):
    def __init__(self, statuscode: int):
        self.statuscode = statuscode
        self.message = f"HTTP {statuscode} error. No Problem Detail provided."
        super().__init__(self.message)


class NgsiContextBrokerError(NgsiApiError):
    def __init__(self, problemdetails: ProblemDetails):
        self.problemdetails = problemdetails
        super().__init__(f"{problemdetails.title} : {problemdetails.detail}")


class NgsiInvalidRequestError(NgsiContextBrokerError):
    pass


class NgsiBadRequestDataError(NgsiContextBrokerError):
    pass


class NgsiAlreadyExistsError(NgsiContextBrokerError):
    pass


class NgsiOperationNotSupportedError(NgsiContextBrokerError):
    pass


class NgsiResourceNotFoundError(NgsiContextBrokerError):
    pass


class NgsiInternalError(NgsiContextBrokerError):
    pass


class NgsiLdContextNotAvailableError(NgsiContextBrokerError):
    pass


class NgsiTooComplexQueryError(NgsiContextBrokerError):
    pass


class NgsiTooManyResultsError(NgsiContextBrokerError):
    pass


class NgsiNoMultiTenantSupportError(NgsiContextBrokerError):
    pass


class NgsiNonexistentTenantError(NgsiContextBrokerError):
    pass


ERRORTYPES = {
    "https://uri.etsi.org/ngsi-ld/errors/InvalidRequest": NgsiInvalidRequestError,
    "https://uri.etsi.org/ngsi-ld/errors/BadRequestData": NgsiBadRequestDataError,
    "https://uri.etsi.org/ngsi-ld/errors/AlreadyExists": NgsiAlreadyExistsError,
    "https://uri.etsi.org/ngsi-ld/errors/OperationNotSupported": NgsiOperationNotSupportedError,
    "https://uri.etsi.org/ngsi-ld/errors/ResourceNotFound": NgsiResourceNotFoundError,
    "https://uri.etsi.org/ngsi-ld/errors/InternalError": NgsiInternalError,
    "https://uri.etsi.org/ngsi-ld/errors/TooComplexQuery": NgsiTooComplexQueryError,
    "https://uri.etsi.org/ngsi-ld/errors/TooManyResults": NgsiTooManyResultsError,
    "https://uri.etsi.org/ngsi-ld/errors/LdContextNotAvailable": NgsiLdContextNotAvailableError,
    "https://uri.etsi.org/ngsi-ld/errors/NoMultiTenantSupport": NgsiNoMultiTenantSupportError,
    "https://uri.etsi.org/ngsi-ld/errors/NonexistentTenant": NgsiNonexistentTenantError,
}


def rfc7807_error_handle(func):
    """A decorator function to handle enriched Exceptions that accept a ProblemDetails instance.

    See Also
    --------
    api.entities.create
    api.entities.retrieve
    """

    def inner_function(*args, **kwargs):
        problemdetails: dict = {}
        try:
            return func(*args, **kwargs)
        except HTTPError as e:
            r: Response = e.response
            try:
                problemdetails = r.json()
                logger.info(f"{problemdetails=}")
            except ContentDecodingError:
                raise NgsiHttpError(r.status_code) from e
            try:
                pd_type = problemdetails.pop("type").rstrip()
                logger.info(f"{pd_type=}")
                exception: NgsiContextBrokerError = ERRORTYPES.get(pd_type)
                logger.info(f"{exception=}")
                pd = ProblemDetails(
                    pd_type,
                    problemdetails.pop("title", None),
                    r.status_code,
                    problemdetails.pop("detail", None),
                    problemdetails.pop("instance", None),
                    problemdetails,  # extension
                )
                raise exception(pd)
            except HTTPError as e:
                raise NgsiApiError(f"Error while requesting the broker API. Status code = {r.status_code}") from e
        except RequestException as e:
            raise NgsiApiError("Error while requesting the broker API") from e

    return inner_function


def rfc7807_error_handle_async(func):
    """A decorator function to handle enriched Exceptions that accept a ProblemDetails instance.

    See Also
    --------
    api.entities.create
    api.entities.retrieve
    """

    async def inner_function(*args, **kwargs):
        problemdetails: dict = {}
        try:
            return await func(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            r: httpx.Response = e.response
            try:
                problemdetails = r.json()
                logger.info(f"{problemdetails=}")
            except httpx.DecodingError:
                raise NgsiHttpError(r.status_code) from e
            try:
                pd_type = problemdetails.pop("type").rstrip()
                logger.info(f"{pd_type=}")
                exception: NgsiContextBrokerError = ERRORTYPES.get(pd_type)
                logger.info(f"{exception=}")
                pd = ProblemDetails(
                    pd_type,
                    problemdetails.pop("title", None),
                    r.status_code,
                    problemdetails.pop("detail", None),
                    problemdetails.pop("instance", None),
                    problemdetails,  # extension
                )
                raise exception(pd)
            except httpx.HTTPStatusError as e:
                raise NgsiApiError(f"Error while requesting the broker API. Status code = {r.status_code}") from e
        except httpx.RequestError as e:
            raise NgsiApiError("Error while requesting the broker API") from e

    return inner_function
