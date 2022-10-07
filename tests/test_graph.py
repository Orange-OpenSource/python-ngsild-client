#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

from typing import List
from ngsildclient import Client, Entity

class MockedClient(Client):
    def __init__(self):
        self._broker_impl: dict[str, Entity] = {}

    def get(self, eid: str) -> Entity:
        if not eid.startswith("urn:ngsi-ld"):
            eid = "urn:ngsi-ld:" + eid
        return self._broker_impl[eid]

    def upsert(self, entities: List[Entity]):
        self._broker_impl |= {e.id: e for e in entities}

def build_adjmat(client: Client, root: Entity, source: List[str]=[], target: List[str]=[]):
    for _, node in root.relationships: # edges are ignored
        source.append(root.id)
        target.append(node)
        entity = client.get(node)
        source, target = build_adjmat(client, entity, source, target)
    return source, target

def test_broker_impl():
    a1 = Entity("A", "A1")
    b1 = Entity("B", "B1")
    c1 = Entity("C", "C1")
    a1.rel("hasB", b1)
    b1.rel("hasC", c1)
    assert a1.relationships == [("hasB", "urn:ngsi-ld:B:B1")]
    assert b1.relationships == [("hasC", "urn:ngsi-ld:C:C1")]
    client = MockedClient()
    client.upsert([a1, b1, c1])
    x = client.get("urn:ngsi-ld:A:A1")
    y = client.get("urn:ngsi-ld:B:B1")
    z = client.get("urn:ngsi-ld:C:C1")
    assert (x,y,z) == (a1,b1,c1)

def test_graph_1():
    a1 = Entity("A", "A1")
    b1 = Entity("B", "B1")
    c1 = Entity("C", "C1")
    a1.rel("hasB", b1)
    b1.rel("hasC", c1)    
    client = MockedClient()
    client.upsert([a1, b1, c1])
    a1 = client.get("A:A1")
    source, target = client.build_adjmat(a1, [], [])
    assert len(source) == 2
    assert len(target) == 2
    assert source[0] == "A:A1"
    assert target[0] == "B:B1"
    assert source[1] == "B:B1"
    assert target[1] == "C:C1"    
    