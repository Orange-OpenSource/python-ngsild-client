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
from typing import List
from ngsildclient import Client, Entity

broker_impl: dict[str, Entity] = {}

def broker_get(eid: str) -> Entity:
    if not eid.startswith("urn:ngsi-ld"):
        eid = "urn:ngsi-ld:" + eid
    return broker_impl[eid]

def broker_upsert(entities: List[Entity]):
    global broker_impl
    broker_impl |= {e.id: e for e in entities}

@fixture()
def mocked_get(mocker: MockerFixture):
    mocker.patch.object(Client, "get", side_effect=broker_get)

@fixture()
def mocked_upsert(mocker: MockerFixture):
    mocker.patch.object(Client, "upsert", side_effect=broker_upsert) 

def build_adjmat(client: Client, root: Entity, source: List[str]=[], target: List[str]=[]):
    for edge, node in root.relationships:
        source.append(edge)
        target.append(node)
        entity = client.get(node)
        source, target = build_adjmat(client, entity, source, target)
    return source, target

def test_broker_impl(mocked_connected, mocked_get, mocked_upsert):
    global broker_impl
    a1 = Entity("A", "A1")
    b1 = Entity("B", "B1")
    c1 = Entity("C", "C1")
    a1.rel("hasB", b1)
    b1.rel("hasC", c1)
    assert a1.relationships == [("hasB", "urn:ngsi-ld:B:B1")]
    assert b1.relationships == [("hasC", "urn:ngsi-ld:C:C1")]
    client = Client()
    client.upsert([a1, b1, c1])
    x = client.get("urn:ngsi-ld:A:A1")
    y = client.get("urn:ngsi-ld:B:B1")
    z = client.get("urn:ngsi-ld:C:C1")
    assert (x,y,z) == (a1,b1,c1)

def test_graph_1(mocked_connected, mocked_get, mocked_upsert):
    global broker_impl
    a1 = Entity("A", "A1")
    b1 = Entity("B", "B1")
    c1 = Entity("C", "C1")
    a1.rel("hasB", b1)
    b1.rel("hasC", c1)    
    client = Client()
    a1 = client.get("A:A1")
    source, target = build_adjmat(client, a1, [], [])
    assert source is not None
    