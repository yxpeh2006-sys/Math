import networkx as nx
import matplotlib.pyplot as plt
from setup import *

def load_graph(graph):
    G = nx.Graph()
    for label in graph.nodes:
        G.add_node(label, area=graph.nodes[label].area)
    for label in graph.nodes:
        for neighbour in graph.nodes[label].neighbours:
            if neighbour is None:
                continue
            G.add_edge(label, neighbour.label)
    return G

def display_graph(G):
    outside_labels = {node: node for node in G.nodes}
    inside_labels = {node: G.nodes[node]['area'] for node in G.nodes}
    pos = nx.planar_layout(G)
    nx.draw(
        G,
        pos,
        labels=inside_labels,
        with_labels=True,
        node_size=1200,
        font_size=10
    )
    pos_higher = {node: (x, y + 0.08) for node, (x, y) in pos.items()}
    nx.draw_networkx_labels(
        G,
        pos_higher,
        labels=outside_labels
    )
    plt.show()

def display_path(graph):
    path = graph.path()[:-1]
    special_edges = {(path[i], path[i+1]) for i in range(graph.size)} | {(path[i+1], path[i]) for i in range(graph.size)}
    edge_colours = []
    G = load_graph(graph)
    for edge in G.edges:
        if edge in special_edges:
            edge_colours.append('red')
        else:
            edge_colours.append('gray')
    outside_labels = {node: node for node in G.nodes}
    inside_labels = {node: G.nodes[node]['area'] for node in G.nodes}
    pos = nx.planar_layout(G)
    nx.draw(
        G,
        pos,
        labels=inside_labels,
        with_labels=True,
        edge_color=edge_colours,
        width=2.5,
        node_size=1200,
        font_size=10
    )
    pos_higher = {node: (x, y + 0.08) for node, (x, y) in pos.items()}
    nx.draw_networkx_labels(
        G,
        pos_higher,
        labels=outside_labels
    )
    plt.show()