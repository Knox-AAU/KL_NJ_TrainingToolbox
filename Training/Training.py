import json

import spacy
from spacy.tokens import DocBin
from spacy.cli.train import train as spacy_train


def train_model(model: str = "da_core_news_lg",
                train: str = "./output/train.jsonl",
                dev: str = "./output/dev.jsonl",
                dest: str = "./output",
                config: str = "./Training/accuracy_config.cfg"):
    train_destination = f'{dest}/train.spacy'
    dev_destination = f'{dest}/dev.spacy'
    print("---Converting training set to spacy binary---")
    __convert_to_spacy_binary(model, train, train_destination)
    print("---Converting dev set to spacy binary---")
    __convert_to_spacy_binary(model, dev, dev_destination)
    print("---Training spacy model---")
    spacy_train(config, dest, overrides={"paths.train": train_destination, "paths.dev": dev_destination})


def __convert_to_spacy_binary(base_model: str, dataset_fp: str, destination: str):
    db = DocBin()
    nlp = spacy.load(base_model)
    with open(dataset_fp, encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                doc = nlp.make_doc(data['data'])
                ents = []
                for start, end, label in data['label']:
                    span = doc.char_span(start, end, label=label)
                    ents.append(span)
                doc.ents = ents
                db.add(doc)
            except BaseException as e:
                print(f'Skipping: {data}. Message: {e}')
    db.to_disk(destination)
    return db