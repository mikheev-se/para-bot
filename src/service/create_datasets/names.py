import json
import os

import numpy as np

sep = ' '
dataset = []
queries = ['gitlab аккаунт',
           'гитлаб аккаунт',
           'github аккаунт',
           'гитхаб аккаунт',
           'баллы',
           'успеваемость', ]
label = 'name'

with open(os.path.dirname(os.path.abspath(__file__)) + '/../../../datasets/names/names.txt', 'r') as file:
    names = list(map(lambda x: x.replace('\n', ''), file.readlines()))

for name in names:
    query = queries[np.argmax(np.random.rand(len(queries),))]
    if np.random.rand() >= .5:
        result = name.title() + sep + query
        start, end = 0, len(name)
        ner = (start, end)
    else:
        result = query + sep + name.title()
        start = len(query) + len(sep)
        end = start + len(name)
        ner = (start, end)
    dataset.append({
        'entities': [{'start': start, 'end': end, 'label': label.upper()}],
        'text': result.strip()
    })

with open(os.path.dirname(os.path.abspath(__file__)) + '/../../../datasets/names/names.json', 'w') as file:
    json.dump(dataset, file, indent=2, ensure_ascii=False)
