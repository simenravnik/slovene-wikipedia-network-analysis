import networkx as nx
import os
from collections import defaultdict
import numpy as np


def read_net(folder, graph_name):
    """Read network"""
    file_name = graph_name + '.net'
    G = nx.DiGraph(name = file_name)
    with open(os.path.join(folder, file_name), 'r', encoding='utf8') as f:
        f.readline()
        # add nodes
        for line in f:
            if line.startswith("*"):
                break
            else:
                node_info = line.split("\"")
                node = int(node_info[0]) - 1
                label = node_info[1]
                G.add_node(node, label=label)

        # add edges
        for line in f:
            node1_str, node2_str = line.split()[:2]
            G.add_edge(int(node1_str)-1, int(node2_str)-1)
    return G


def to_adjacency(data):
    id_to_idx_map = defaultdict(int)
    ids = list(data.keys())
    for i in range(len(data)):
        id_to_idx_map[ids[i]] = i

    adj_mtx = np.zeros((len(ids), len(ids)))

    for id_from, links in data.items():
        for id_to in links:
            adj_mtx[id_to_idx_map[id_from]][id_to_idx_map[str(id_to)]] = 1
    return adj_mtx