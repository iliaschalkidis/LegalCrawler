## Legal Crawler :octopus:

A collection of scripts to crawl English legal corpora :closed_book: from open public domains.

* The current version supports the following domains:

| Corpus          | Domain                          | Corpus alias        |
| ------------------- | ------------------------------------  | ------------------- |
| :eu: EU legislation      | https://eur-lex.europa.eu/            | `eu`                |
| :uk: UK legislation      | https://legislation.gov.uk/           | `uk` |
| :canada: Canadian legislation  | http://laws.justice.gc.ca/eng/      | `ca` |
| :jp: Japanese legislation  | http://www.japaneselawtranslation.go.jp/law/     | `jp` |
| :finland: Finish legislation    | https://www.finlex.fi/en    | `fi` |
| :us: US case law* | https://case.law/bulk/download/ | `us` |

\* In order to use the script for US case law, you need to first apply for a researcher account.

* For US public filings, e.g., contracts, please use the library OpenEDGAR (https://github.com/LexPredict/openedgar) by LexPredict.
* Documents are saved in raw text format, amend the code if you wish to better handle metadata, document structure, etc.

## :bangbang: Disclaimer :bangbang:

* If you aim to use the code, please carefully read the individual license agreements with respect to re-use, re-publication, terms of use, etc. :memo:
* The text cleansing from the original PDF/HTML files is minimal. Consider amending the scripts and/or writing your own post-processing data cleansing process that better fit for each corpus. :construction:
* These scripts aim to give researchers a kick start for scraping legal corpora from public domains. They should not considered a stand-alone qualified solution. :construction:

## Project Requirements:

### Python packages
* json-lines
* tqdm
* beautifulsoup4

### Linux packages (command line tools)

The following linux packages are used to process PDF documents:

* pdftocairo
* pdftotext
* mutool
* gs

## Quick start:

### Install python requirements:

```
pip install -r requirements.txt

sudo apt-get install libcairo2-dev
sudo apt-get install libpango1.0-dev
sudo apt-get install -y xpdf
sudo apt-get install mupdf mupdf-tools
```

### Download Canadian legislation

```
python download_legal_corpora.py --corpus ca
```

### Download EU legislation

```
python download_legal_corpora.py --corpus eu

```

### Download all (EU, UK, CA, FI, JP, US)

```
python download_legal_corpora.py --corpus all

```


