import os
import json
import requests
from collections import defaultdict
import time

WIKIPEDIA_API = "https://sl.wikipedia.org/w/api.php"
PWD = os.getcwd()

with open(os.path.join(PWD, "data", "title_to_id_map.json"), "r") as f:
    title_to_id_map = json.loads(f.read())

with open(os.path.join(PWD, "data", "id_to_title_map.json"), "r") as f:
    id_to_title_map = json.loads(f.read())

# Flatten
possible_rederect_titles = list(title_to_id_map.keys())
title_to_id_set = set(title_to_id_map.keys())

# Redirects
params = {
    "action": "query",
    "format": "json",
    "pageids": "",
    "redirects": "True"
}

redirect_map = defaultdict()
for idx in range(0, len(possible_rederect_titles), 50):
    titles = possible_rederect_titles[idx:idx+50]

    pageids = list(map(lambda title: str(title_to_id_map[title]), titles))
    pageids_string = "|".join(pageids)

    params["pageids"] = pageids_string
    while True:
        try:
            r = requests.get(url=WIKIPEDIA_API, params=params)
            content = json.loads(r.text)

            if "redirects" in content["query"]:
                redirects = content["query"]["redirects"]
                for redirect in redirects:
                    if redirect["to"] in title_to_id_set:
                        redirect_map[title_to_id_map[redirect["from"]]] = title_to_id_map[redirect["to"]]
            break
        except Exception as e:
            print(e)
            time.sleep(60)
    
    if idx % 100 == 0:
        print(idx)
        with open(os.path.join(PWD, "data", 'redirect_map.json'), 'w') as f:
            json.dump(redirect_map, f)
        with open(os.path.join(PWD, "data", 'count.txt'), 'w') as f:
            f.write(str(idx))

with open(os.path.join(PWD, "data", 'redirect_map.json'), 'w') as f:
    json.dump(redirect_map, f)
with open(os.path.join(PWD, "data", 'count.txt'), 'w') as f:
    f.write("end")

