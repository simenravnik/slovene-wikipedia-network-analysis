from collections import defaultdict
import os
import json

PWD = os.getcwd()

with open(os.path.join(PWD, "data", "wikilinks.json"), "r") as f:
    data = json.loads(f.read())

with open(os.path.join(PWD, "data", "id_to_title_map.json"), "r") as f:
    id_to_title_map = json.loads(f.read())

ids = list(data.keys())
seen = [False] * len(ids)
similarity_map = defaultdict(list)
for i in range(len(ids)):
    if seen[i]:
        continue
    seen[i] = True
    id_first = ids[i]
    links_first = data[id_first]
    if len(links_first) == 0:
        seen[i] = True
        continue
    
    for j in range(i+1, len(ids)):
        if seen[j]:
            continue
        id_second = ids[j]
        links_second = data[id_second]
        if len(links_second) == 0:
            seen[j] = True
            continue

        if links_first == links_second:
            seen[j] = True
            similarity_map[id_to_title_map[id_first]].append(id_to_title_map[id_second])
    
    if (i+1) % 1000 == 0:
        print(i)
        with open(os.path.join(PWD, "data", 'similarity_map.json'), 'w') as f:
            json.dump(similarity_map, f)
        with open(os.path.join(PWD, "data", 'count.txt'), 'w') as f:
            f.write(str(i))

with open(os.path.join(PWD, "data", 'similarity_map.json'), 'w') as f:
    json.dump(similarity_map, f)
with open(os.path.join(PWD, "data", 'count.txt'), 'w') as f:
    f.write("end")