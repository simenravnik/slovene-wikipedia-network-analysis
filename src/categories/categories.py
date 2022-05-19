import json
from collections import defaultdict, OrderedDict
import requests
import os
import time

PWD = os.getcwd()

WIKIPEDIA_API = "https://sl.wikipedia.org/w/api.php"

params = {
    "action": "query",
    "format": "json",
    "list": "allcategories",
    "aclimit": "max",
    "accontinue": "",
    "continue": ""
}
next_params = params

all_categories = set()
count = 0
while True:

    while True:
        try:
            r = requests.get(url=WIKIPEDIA_API, params=params)

            print(r.request.url)

            content = json.loads(r.text)

            for category in content["query"]["allcategories"]:
                all_categories.add(category["*"])
            break
        except Exception as e:
            print(e)
            print("Banned!")
            time.sleep(60)
   
    if "continue" not in content.keys():
        break

    params["accontinue"] = content["continue"]["accontinue"]
    params["continue"] = content["continue"]["continue"]

    count += 1
    if count % 100 == 0:
        print(count)
        with open(os.path.join(PWD, "data", 'categories.json'), 'w') as f:
            json.dump(list(all_categories), f)
        with open(os.path.join(PWD, "data", 'count.txt'), 'w') as f:
            f.write(str(count))
            json.dump(next_params, f)
        next_params = params

with open(os.path.join(PWD, "data", 'categories.json'), 'w') as f:
    json.dump(list(all_categories), f)
with open(os.path.join(PWD, "data", 'count.txt'), 'w') as f:
    f.write("end")