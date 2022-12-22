import json
import os

import numpy as np

sep = ' '
dataset = []
queries = ['расписание', 'занятия', 'пары', ]
label = 'date'

with open(os.path.dirname(os.path.abspath(__file__)) + '/dates.txt', 'r') as file:
    dates = list(map(lambda x: x.replace('\n', ''), file.readlines()))

for date in dates:
    query = queries[np.argmax(np.random.rand(len(queries),))]
    if np.random.rand() >= .5:
        result = date + sep + query
        start, end = 0, len(date)
        ner = (start, end)
    else:
        result = query + sep + date
        start = len(query) + len(sep)
        end = start + len(date)
        ner = (start, end)
    dataset.append({
        'entities': [{'start': start, 'end': end, 'label': label.upper()}],
        'text': result.strip()
    })

with open(os.path.dirname(os.path.abspath(__file__)) + '/dates.json', 'w') as file:
    json.dump(dataset, file, indent=2, ensure_ascii=False)
