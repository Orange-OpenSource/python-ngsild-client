#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from pytest import fixture
from pytest_mock import MockerFixture
from ngsildclient.api.client import Client


@fixture()
def mocked_connected(mocker: MockerFixture):
    mocker.patch.object(Client, "is_connected", return_value=True)
