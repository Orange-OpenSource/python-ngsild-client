#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.

import networkx as nx

from typing import List
from ngsildclient import Client, Entity
from ngsildclient.utils.urn import Urn

class MockedClient(Client):
    def __init__(self):
        self._broker_impl: dict[str, Entity] = {}

    def get(self, eid: str) -> Entity:
        eid = eid.id if isinstance(eid, Entity) else eid
        return self._broker_impl[Urn.prefix(eid)]

    def upsert(self, entities: List[Entity]):
        self._broker_impl |= {e.id: e for e in entities}

def test_relationships():
    a1 = Entity("A", "A1")
    b1 = Entity("B", "B1")
    c1 = Entity("C", "C1")
    a1.rel("hasB", b1)
    a1.rel("hasC", c1)
    assert a1.relationships == [("hasB", "urn:ngsi-ld:B:B1"), ("hasC", "urn:ngsi-ld:C:C1")]

def test_relationships_multi():
    a1 = Entity("A", "A1")
    b1 = Entity("B", "B1")
    c1 = Entity("C", "C1")
    d1 = Entity("D", "D1")
    d2 = Entity("D", "D2")
    a1.rel("hasB", b1)
    a1.rel("hasC", c1)
    a1.rel("hasMultiD", [d1, d2])
    assert a1.relationships == [
        ("hasB", "urn:ngsi-ld:B:B1"), 
        ("hasC", "urn:ngsi-ld:C:C1"), 
        ("hasMultiD", "urn:ngsi-ld:D:D1"), 
        ("hasMultiD", "urn:ngsi-ld:D:D2")
    ]    

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
    root = client.get("A:A1")
    G: nx.Graph = client.network(root)
    assert len(G.nodes) == 3
    assert len(G.edges) == 2
    nodes = [*G.nodes]
    assert nodes[0] == ('A', 'A:A1')
    assert nodes[1] == ('B', 'B:B1')
    assert nodes[2] == ('C', 'C:C1')
    edges = [*G.edges]
    assert edges[0] == (('A', 'A:A1'), ('B', 'B:B1'))
    assert edges[1] == (('B', 'B:B1'), ('C', 'C:C1'))

def test_graph_2():
    a1 = Entity("A", "A1")
    b1 = Entity("B", "B1")
    c1 = Entity("C", "C1")
    a1.rel("hasB", b1)
    b1.rel("hasC", c1)
    c1.rel("hasA", a1)    
    client = MockedClient()
    client.upsert([a1, b1, c1])
    root = client.get(a1)
    G: nx.Graph = client.network(root)
    assert len(G.nodes) == 3
    assert len(G.edges) == 3
    nodes = [*G.nodes]
    assert nodes[0] == ('A', 'A:A1')
    assert nodes[1] == ('B', 'B:B1')
    assert nodes[2] == ('C', 'C:C1')
    edges = [*G.edges]
    assert edges[0] == (('A', 'A:A1'), ('B', 'B:B1'))
    assert edges[1] == (('A', 'A:A1'), ('C', 'C:C1'))
    assert edges[2] == (('B', 'B:B1'), ('C', 'C:C1'))

# def test_graph_3():
#     a1 = Entity("A", "A1")
#     b1 = Entity("B", "B1")
#     c1 = Entity("C", "C1")
#     d1 = Entity("D", "D1")
#     d2 = Entity("D", "D2")
#     a1.rel("hasB", b1)
#     a1.rel("hasD", [d1, d2]) # TODO : do multiple relationships now require datasetId ?
#     b1.rel("hasC", c1)
#     c1.rel("hasA", a1)    
#     client = MockedClient()
#     client.upsert([a1, b1, c1, d1, d2])
#     root = client.get("A:A1")
#     G: nx.Graph = client.network(root)
#     assert len(G.nodes) == 5
#     assert len(G.edges) == 3
#     nodes = [*G.nodes]
#     assert nodes[0] == ('A', 'A:A1')
#     assert nodes[1] == ('B', 'B:B1')
#     assert nodes[2] == ('C', 'C:C1')
#     edges = [*G.edges]
#     assert edges[0] == (('A', 'A:A1'), ('B', 'B:B1'))
#     assert edges[1] == (('A', 'A:A1'), ('C', 'C:C1'))
#     assert edges[2] == (('B', 'B:B1'), ('C', 'C:C1'))

# def test_graph_4():
#     a1 = Entity("A", "A1")
#     b1 = Entity("B", "B1")
#     c1 = Entity("C", "C1")
#     d1 = Entity("D", "D1")
#     d2 = Entity("D", "D2")
#     a1.rel("hasB", b1)
#     a1.rel("hasD", [d1, d2])
#     a1.rel("hasC", c1)
#     b1.rel("hasC", c1)
#     c1.rel("hasA", a1)    
#     client = MockedClient()
#     client.upsert([a1, b1, c1, d1, d2])
#     a1 = client.get("A:A1")
#     source, target = client.adjvec(a1)
#     assert len(source) == 5
#     assert len(target) == 5
#     assert source[0] == "A:A1"
#     assert target[0] == "B:B1"
#     assert source[1] == "B:B1"
#     assert target[1] == "C:C1"
#     assert source[2] == "C:C1"
#     assert target[2] == "A:A1"
#     assert source[3] == "A:A1"
#     assert target[3] == "D:D1"
#     assert source[4] == "A:A1"
#     assert target[4] == "D:D2"    
