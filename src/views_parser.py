import os
import json
import requests
from collections import defaultdict
import time

WIKIPEDIA_API = "https://sl.wikipedia.org/w/api.php"
PWD = os.getcwd()

with open(os.path.join(PWD, "data", "wikilinks.json"), "r") as f:
    data = json.loads(f.read())

# Flatten
pageids_all = list(data.keys())

# Redirects
params = {
    "action": "query",
    "format": "json",
    "pageids": "",
    "prop": "pageviews"
}

views_map = defaultdict()
step = 50
c = 0
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
            content = json.loads(r.text)

            print(r.url)

            for page in content["query"]["pages"]:
                if "pageviews" in content["query"]["pages"][page].keys():
                    views_map[page] = content["query"]["pages"][page]["pageviews"]
                else:
                    pageids_all.append(page)
            break
        except Exception as e:
            print(e)
            time.sleep(60)

    c += 50
    if c % 100 == 0:
        print(c)
        with open(os.path.join(PWD, "data", 'redirect_map.json'), 'w') as f:
            json.dump(views_map, f)
        with open(os.path.join(PWD, "data", 'count.txt'), 'w') as f:
            f.write(str(c))

with open(os.path.join(PWD, "data", 'views_map.json'), 'w') as f:
    json.dump(views_map, f)
with open(os.path.join(PWD, "data", 'count.txt'), 'w') as f:
    f.write("end")
with open(os.path.join(PWD, "data", 'repeat_pages.txt'), 'w') as f:
    json.dump(repeat_pages, f)