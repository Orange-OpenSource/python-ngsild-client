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

import pytest

from orionldclient.utils.urn import Urn, UrnError


def test_is_valid_nid_true():
    assert Urn.is_valid_nid("ngsi-ld")


def test_is_valid_nid_false():
    assert not Urn.is_valid_nid("ngsi*ld")


def test_constructor():
    urn = Urn("test")
    assert urn.scheme == "urn"
    assert urn.nid == "ngsi-ld"
    assert urn.nss == "test"


def test_constructor_with_nid():
    urn = Urn("test", nid="my-nid")
    assert urn.scheme == "urn"
    assert urn.nid == "my-nid"
    assert urn.nss == "test"


def test_valid_urn():
    urn = Urn.from_fully_qualified_string("urn:ngsi-ld:test")
    assert urn.scheme == "urn"
    assert urn.nid == "ngsi-ld"
    assert urn.nss == "test"


def test_invalid_urn_bad_nid():
    with pytest.raises(UrnError):
        urn = Urn.from_fully_qualified_string("urn:ngsi*ld:test")


def test_invalid_urn_missing_nss():
    with pytest.raises(UrnError):
        urn = Urn.from_fully_qualified_string("urn:ngsi-ld:")


def test_guess_from_string():
    urn1 = Urn.from_string("test")  # built from nss only
    urn2 = Urn.from_string("urn:ngsi-ld:test")  # built from fully qualified string
    assert urn1 == urn2
