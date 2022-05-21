from importlib.resources import read_binary
import networkx as nx
from helper_functions import read_net
import os
import json

PWD = os.getcwd()
filename = "wikilinks_ids"

G = read_net(os.path.join(PWD, "data"), filename)

PR = nx.pagerank(G)
with open(os.path.join(PWD, "data", "out", "PR.json"), "w") as f:
    json.dump(PR, f)

DC = nx.degree_centrality(G)
with open(os.path.join(PWD, "data", "out", "DC.json"), "w") as f:
    json.dump(DC, f)

CC = nx.closeness_centrality(G)
with open(os.path.join(PWD, "data", "out", "CC.json"), "w") as f:
    json.dump(CC, f)

BC = nx.betweenness_centrality(G)
with open(os.path.join(PWD, "data", "out", "BC.json"), "w") as f:
    json.dump(BC, f)

C = nx.clustering(nx.Graph(G))
with open(os.path.join(PWD, "data", "out", "C.json"), "w") as f:
    json.dump(C, f)