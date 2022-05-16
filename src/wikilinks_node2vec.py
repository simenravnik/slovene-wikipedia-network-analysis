from node2vec import Node2Vec
import networkx as nx
import os
from helper_functions import read_net

PWD = os.getcwd()

EMBEDDING_FILENAME = os.path.join(PWD, "data", "node2vec.model")

filename = "wikilinks_ids"
folder = os.path.join(PWD, "data")
G = read_net(folder, filename)

node2vec = Node2Vec(G, workers=10)

model = node2vec.fit(window=10, min_count=1)
model.wv.save_word2vec_format(EMBEDDING_FILENAME)