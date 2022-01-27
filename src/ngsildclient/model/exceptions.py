#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from ..exceptions import NgsiError


class NgsiModelError(NgsiError):
    pass


class NgsiMissingIdError(NgsiModelError):
    pass


class NgsiMissingTypeError(NgsiModelError):
    pass


class NgsiMissingContextError(NgsiModelError):
    pass


class NgsiUnmatchedAttributeTypeError(NgsiModelError):
    pass


class NgsiDateFormatError(NgsiModelError):
    pass


class NgsiJsonError(NgsiModelError):
    pass


class NgsiUnsupportedFormatError(NgsiModelError):
    pass
