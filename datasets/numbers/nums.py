import json
import os

import numpy as np

sep = ' '
dataset = []
queries = ['лабораторная', 'лабораторная номер', 'контрольная', 'контрольная номер', 'неделя']
label = 'number'

with open(os.path.dirname(os.path.abspath(__file__)) + '/numbers.txt', 'r') as file:
    numbers = list(map(lambda x: x.replace('\n', ''), file.readlines()))

for number in numbers:
    query = queries[np.argmax(np.random.rand(len(queries),))]
    result = query + sep + number
    start = len(query) + len(sep)
    end = start + len(number)
    ner = (start, end)
    dataset.append({
        'entities': [{'start': start, 'end': end, 'label': label.upper()}],
        'text': result.strip()
    })

with open(os.path.dirname(os.path.abspath(__file__)) + '/numbers.json', 'w') as file:
    json.dump(dataset, file, indent=2, ensure_ascii=False)
