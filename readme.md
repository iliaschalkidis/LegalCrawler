## Legal Crawler :octopus:

A collection of scripts to crawl legal corpora from public domains.

The current version supports the following:

| Corpus          | Domain                          | Corpus alias        |
| ------------------- | ------------------------------------  | ------------------- |
| :eu: EU legislation      | https://eur-lex.europa.eu/            | `eu`                |
| :uk: UK legislation      | https://legislation.gov.uk/           | `uk` |
| :ca: Canadian legislation  | http://laws.justice.gc.ca/eng/      | `ca` |
| :jp: Japanese legislation  | http://www.japaneselawtranslation.go.jp/law/     | `jp` |
| Finish legislation    | https://www.finlex.fi/en    | `fi` |
| US case law | https://case.law/bulk/download/ | `us` |

## Requirements:

### Python packages
* json-lines
* tqdm
* beautifulsoup4

### Linux packages (command line tools)

* pdftocairo
* pdftotext
* mutool
* gs

## Quick start:

### Install python requirements:

```
pip install -r requirements.txt
```

### Download Canadian legislation

```
python download_legal_corpora.py --corpus ca
```

### Download EU legislation

```
wget -O data/datasets/datasets.zip http://nlp.cs.aueb.gr/software_and_datasets/EURLEX57K/datasets.zip
unzip data/datasets/datasets.zip -d data/datasets/EURLEX57K
rm data/datasets/datasets.zip
rm -rf data/datasets/EURLEX57K/__MACOSX
mv data/datasets/EURLEX57K/dataset/* data/datasets/EURLEX57K/
rm -rf data/datasets/EURLEX57K/dataset
wget -O data/datasets/EURLEX57K/EURLEX57K.json http://nlp.cs.aueb.gr/software_and_datasets/EURLEX57K/eurovoc_en.json
```


