import classla
import json
import nltk
from nltk.corpus import stopwords
import wikipediaapi


wiki = wikipediaapi.Wikipedia('sl')

nltk.download('stopwords')

# download standard models for Slovenian
classla.download('sl')
nlp = classla.Pipeline('sl', processors='tokenize,ner,pos,lemma,depparse')

stopwords = set(stopwords.words('slovene'))
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
for p in punc:
    stopwords.add(p)

with open("data/title_to_id_map.json", "r") as f:
    title_to_id_map = json.loads(f.read())

with open("data/id_to_title_map.json", "r") as f:
    id_to_title_map = json.loads(f.read())

with open("data/wikilinks.json", "r") as f:
    data = json.loads(f.read())

titles = []
for id in data.keys():
    titles.append(id_to_title_map[id])

print("Zacenjam z pridobivanjem in lematizaticjo povzetkov...")

lemma_all = []
for idx, title in enumerate(titles):
    page = wiki.page(title)
    summary = page.summary

    lemma = [i for i in nlp(summary).get("lemma") if i not in stopwords]
    lemma_all.append(lemma)

    if idx % 100 == 0:
        with open("data/export/lemma_all.json", 'w') as f:
            json.dump(lemma_all, f)
        with open("data/export/count.json", 'w') as f:
            json.dump(idx, f)

with open("data/export/lemma_all.json", 'w') as f:
    json.dump(lemma_all, f)
with open("data/export/count.json", 'w') as f:
    json.dump("end", f)