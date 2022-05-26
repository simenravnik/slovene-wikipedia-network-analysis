import json
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
import numpy as np
from helper_functions import read_net
import multiprocessing


with open("data/wikilinks.json", "r") as f:
    data = json.loads(f.read())

with open("data/title_to_id_map.json", "r") as f:
    title_to_id_map = json.loads(f.read())

with open("data/id_to_title_map.json", "r") as f:
    id_to_title_map = json.loads(f.read())

with open("data/summaries_all.json", "r") as f:
    summaries = json.loads(f.read())

G = read_net("data", "wikilinks_ids")


pageid_to_id_map = dict()
for node, label in G.nodes(data=True):
    pageid_to_id_map[label["label"]] = node

summaries_list = list(summaries.values())
tfidf = TfidfVectorizer().fit_transform(summaries_list)

idx_to_id_map = dict()
id_to_idx_map = dict()
for idx, id in enumerate(list(summaries.keys())):
    idx_to_id_map[idx] = id
    id_to_idx_map[id] = idx

def write_edges(i, thres=0.15):
    pairwise_similarity = tfidf[i] * tfidf.T
    similarity_vector = pairwise_similarity.toarray()[0][i+1:]

    idxs = np.where(similarity_vector > thres)[0]
    list(map(lambda idx: f.write(str(i)+ " " + str(idx) + "\n"), idxs))


f = open("data/wikilinks_summaries.edg", "w")
for i in range(len(summaries_list)):
    write_edges(i, thres=0.15)
    if i % 100 == 0:
        print(i)
f.close()

with open("data/idx_to_id_map.json", 'w') as f:
    json.dump(idx_to_id_map, f)