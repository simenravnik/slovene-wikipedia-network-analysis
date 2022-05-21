import os
import json
import pandas as pd
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

with open(os.path.join("..", "..", "data", 'page_categories.json'), 'r') as f:
    page_categories = json.load(f)

categories_set = set()
count = defaultdict(int)
for page, categories in page_categories.items():
    for category in categories:
        count[category[11:]] += 1
        categories_set.add(category[11:])

for i, c in count.items():
    if c <= 5:
        categories_set.remove(i)

main_topics = [
    "Arhitektura",
    "Astronomija",
    "Biologija",
    "Človek",
    "Dogodki",
    "Družba",
    "Film",
    "Filozofija",
    "Fizika",
    "Geografija",
    "Glasba",
    "Izobraževanje",
    "Jezik",
    "Kemija",
    "Kmetijstvo",
    "Književnost",
    "Kultura",
    "Likovna umetnost",
    "Ljudje",
    "Matematika",
    "Narava",
    "Okolje",
    "Politika",
    "Posel",
    "Pravo",
    "Psihologija",
    "Religija",
    "Tehnika",
    "Umetnost",
    "Vojaštvo",
    "Zdravje",
    "Zgodovina",
    "Znanost"
]

for i in main_topics:
    if i in categories_set:
        categories_set.remove(i)

all_categories = main_topics
for i in list(categories_set):
    all_categories.append(i)

category_to_idx_map = defaultdict(int)
idx = 0
for i in all_categories:
    category_to_idx_map[i] = idx
    idx += 1

data_one_hot = np.zeros((len(page_categories), len(all_categories)), dtype=int)

idx_to_id_map = defaultdict(str)
idx = 0
for page, categories in page_categories.items():

    idx_to_id_map[idx] = page

    for category in categories:
        data_one_hot[idx][category_to_idx_map[category[11:]]] = 1

    idx += 1

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(data_one_hot)

principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])

fig = plt.figure(figsize = (12,12), facecolor="white", dpi=200)
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)

ax.scatter(principalDf['principal component 1'], principalDf['principal component 2'])

plt.show()


