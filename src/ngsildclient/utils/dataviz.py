#!/usr/bin/env python3

# Software Name: ngsildclient
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache 2.0
#
# This software is distributed under the Apache 2.0;
# see the NOTICE file for more details.
#
# Author: Fabien BATTELLO <fabien.battello@orange.com> et al.


"""
This module contains functions to visualize NGSI-LD graphs.

"""

from typing import Tuple

import networkx as nx
import plotly.graph_objects as go

def _compute_node_metadata(G: nx.Graph) -> Tuple:
    pos = nx.shell_layout(G)
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    current_color: int = 0
    maptypecolor: dict[str, int] = {}
    for node in G.nodes():
        x, y = G.nodes[node]["pos"]= pos[node]
        node_x.append(x)
        node_y.append(y)
        #print(node)
        type, shortid = node
        node_text.append(shortid)
        color = maptypecolor.get(type)
        if color is None:
            color = current_color
            maptypecolor[type] = color
            current_color += 1
        node_color.append(color)
        node_size.append(15)
    node_size[0] = 20
    return node_x, node_y, node_text, node_color, node_size

def _compute_node_trace(node_x, node_y, node_text, node_color, node_size) -> go.Scatter:
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            reversescale=True,
            line_width=2))
    node_trace.text = node_text
    node_trace.marker.color = node_color
    node_trace.marker.size = node_size
    return node_trace

def _compute_edge_trace(G: nx.Graph) -> go.Scatter:
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    return edge_trace

def _mk_graph_fig(edge_trace, node_trace) -> go.Figure:
    fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Entities network graph",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig

def mk_graph_fig(G: nx.Graph) -> go.Figure:
    node_metadata = _compute_node_metadata(G)
    node_trace = _compute_node_trace(*node_metadata)
    edge_trace = _compute_edge_trace(G)
    return _mk_graph_fig(edge_trace, node_trace)

def show_graph(G: nx.Graph) -> None:
    fig = mk_graph_fig(G)
    fig.show()
