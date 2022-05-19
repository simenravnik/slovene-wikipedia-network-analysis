import os
import json
import requests
from collections import defaultdict
import time

WIKIPEDIA_API = "https://sl.wikipedia.org/w/api.php"
PWD = os.getcwd()

with open(os.path.join(PWD, "data", "wikilinks.json"), "r") as f:
    data = json.loads(f.read())

pageids_all = list(data.keys())

# Redirects
params = {
    "action": "query",
    "format": "json",
    "pageids": "",
    "prop": "categories",
    "cllimit": "max"
}

page_categories = defaultdict(list)
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

            for page in content["query"]["pages"]:
                if "categories" in content["query"]["pages"][page].keys():
                    for category in content["query"]["pages"][page]["categories"]:
                        page_categories[page].append(category["title"])
                    
                else:
                    print(page)
                    pageids_all.append(page)
            break
        except Exception as e:
            print(e)
            time.sleep(60)
    
    c += 1
    if c % 100 == 0:
        print(c)
        with open(os.path.join(PWD, "data", 'page_categories.json'), 'w') as f:
            json.dump(page_categories, f)
        with open(os.path.join(PWD, "data", 'count.txt'), 'w') as f:
            f.write("Count = " + str(c) + "\nNum of exported pages = " + str(len(page_categories)))

with open(os.path.join(PWD, "data", 'page_categories.json'), 'w') as f:
    json.dump(page_categories, f)
with open(os.path.join(PWD, "data", 'count.txt'), 'w') as f:
    f.write("end")