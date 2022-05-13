import json
from collections import defaultdict, OrderedDict
import wikipediaapi
import requests
import os
import random
import time

wiki = wikipediaapi.Wikipedia('sl')

PWD = os.getcwd()

with open(os.path.join(PWD, "data", 'titles.json'), 'r') as f:
    titles = json.load(f)

with open(os.path.join(PWD, "data", 'title_to_id_map.json'), 'r') as f:
    title_to_id_map = json.load(f)

titles_set = set(titles).intersection(set(title_to_id_map.keys()))

count = 0
data = defaultdict(list)
for title in titles[count:]:

    if title not in titles_set:
        continue

    while True:
        try:
            page = wiki.page(title)
            links = set(page.links.keys())
            break
        except:
            print("Banned!")
            time.sleep(60)

    valid_links = list(links.intersection(titles_set))
    valid_links_ids = list(map(lambda link: title_to_id_map[link], valid_links))
    title_id = title_to_id_map[title]
    data[title_id] = valid_links_ids

    count += 1
    if count % 100 == 0:
        print(count)
        with open(os.path.join(PWD, "data", 'wikilinks.json'), 'w') as f:
            json.dump(data, f)
        with open(os.path.join(PWD, "data", 'count.txt'), 'w') as f:
            f.write(str(count))