import spacy

examples = [
    "Михеев Сергей Евгеньевич gitlab аккаунт",
    "Михеев Сергей gitlab аккаунт",
    "Михеев gitlab аккаунт",
    "24.09 расписание",
    "24 сентября расписание",
    "Какая успеваемость у Михеева Сергея",
    "15 Октября",
    "Ольга Канева",
    "Что нужно делать в 15 лабораторной"
]

nlp = spacy.load('ru_core_news_md')

ruler = nlp.add_pipe("entity_ruler")
patterns = [
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]+\.[0-9]+'
                }
            }
        ],
        'id': '1'
    },
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            },
            {
                'LEMMA': 'январь'
            }
        ]
    },
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            },
            {
                'LEMMA': 'февраль'
            }
        ]
    },
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            },
            {
                'LEMMA': 'март'
            }
        ]
    },
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            },
            {
                'LEMMA': 'апрель'
            }
        ]
    },
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            },
            {
                'LEMMA': 'май'
            }
        ]
    },
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            },
            {
                'LEMMA': 'июнь'
            }
        ]
    },
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            },
            {
                'LEMMA': 'июль'
            }
        ]
    },
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            },
            {
                'LEMMA': 'август'
            }
        ]
    },
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            },
            {
                'LEMMA': 'сентябрь'
            }
        ]
    },
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            },
            {
                'LEMMA': 'октябрь'
            }
        ]
    },
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            },
            {
                'LEMMA': 'ноябрь'
            }
        ]
    },
    {
        'label': 'DATE',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            },
            {
                'LEMMA': 'декабрь'
            }
        ]
    },
    {
        'label': 'NUM',
        'pattern': [
            {
                'TEXT': {
                    'REGEX': '[0-9]'
                }
            }
        ],
        'id': '2'
    },
]
ruler.add_patterns(patterns)

for example in examples:
    doc = nlp(example)
    print(doc)
    print([(ent.text, ent.label_) for ent in doc.ents])
    print('---')
