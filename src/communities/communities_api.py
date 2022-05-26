import os
import json
import requests
from collections import defaultdict
import time

with open("data/title_to_id_map.json", "r") as f:
    title_to_id_map = json.loads(f.read())

with open("data/id_to_title_map.json", "r") as f:
    id_to_title_map = json.loads(f.read())

with open("data/wikilinks.json", "r") as f:
    data = json.loads(f.read())
pageids_all = list(data.keys())


WIKIPEDIA_API = "https://sl.wikipedia.org/w/api.php"

# Redirects
params = {
    "action": "query",
    "format": "json",
    "prop": "extracts",
    "exintro": 1,
    "explaintext": 1,
    "pageids": ""
}

summaries = defaultdict()
step = 20
c = 0

print(len(pageids_all))
while(True):

    if len(pageids_all) == 0:
        break

    pageids = pageids_all[:step]
    pageids_all = pageids_all[step:]

    pageids_string = "|".join(pageids)

    params["pageids"] = pageids_string
    while True:
        try:
            r = requests.get(url=WIKIPEDIA_API, params=params)
            print(r.url)
            content = json.loads(r.text)

            for page in content["query"]["pages"]:
                if "extract" in content["query"]["pages"][page].keys():
                    summaries[page] = content["query"]["pages"][page]["extract"]
                    c += 1
                else:
                    print(page)
                    pageids_all.append(page)
            break
        except Exception as e:
            print(e)
            time.sleep(60)
    
    # if c % 100 == 0:
    with open("data/export/summaries.json", 'w') as f:
        json.dump(summaries, f)
    with open("data/export/count.json", 'w') as f:
        f.write(str(c))

with open("data/export/summaries.json", 'w') as f:
    json.dump(summaries, f)
with open("data/export/count.json", 'w') as f:
    f.write("end")