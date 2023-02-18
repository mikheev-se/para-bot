import json
import os
import spacy
from spacy.util import filter_spans
from spacy.tokens import DocBin

data_path = os.path.dirname(os.path.abspath(__file__)) + '/../../datasets/'
datasets_names = ['dates', 'names', 'numbers']
nlp = spacy.load('ru_core_news_md')
doc_bin = DocBin()

for name in datasets_names:
    with open(data_path + name + '/' + name + '.json',
              'r') as file:
        data = json.load(file)
    for dataset in data:
        doc = nlp.make_doc(dataset['text'])
        entities = []
        for entity in dataset['entities']:
            span = doc.char_span(entity['start'], entity['end'], label=entity['label'],
                                 alignment_mode="contract")
            if span is None:
                print("Skipping entity")
            else:
                entities.append(span)
        filtered_entities = filter_spans(entities)
        doc.ents = filtered_entities
        doc_bin.add(doc)

print(data_path + "training_data.spacy")
doc_bin.to_disk(data_path + "training_data.spacy")
