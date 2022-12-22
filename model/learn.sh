python3.7 ../datasets/dates/dates.py
python3.7 ../datasets/names/names.py
python3.7 ../datasets/numbers/nums.py
python3.7 ../scripts/model.py
python3.7 -m spacy init fill-config base_config.cfg config.cfg
python3.7 -m spacy train config.cfg --output ./ --paths.train ../datasets/training_data.spacy --paths.dev ../datasets/training_data.spacy --gpu-id -1