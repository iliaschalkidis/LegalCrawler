import os
import sys
import json
import requests
import re
from functools import partial
from multiprocessing import cpu_count, Pool
from bs4 import BeautifulSoup
from data import DATA_DIR
sys.setrecursionlimit(100000)

root_dir = os.path.join(DATA_DIR, 'eu')


def download_eu_law():
    with open('/Users/kiddothe2b/Library/Preferences/PyCharm2019.3/scratches/download_legal_corpora/eu_legislation_metadata.json') as file:
        data = list(json.load(file).keys())

    with Pool(processes=cpu_count()) as pool:
        pool.map(partial(download_celex_id), data)


def download_celex_id(celex_id):
    url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{}'
    filename = os.path.join(root_dir, re.sub('[/]', '_', celex_id) + '.html')
    try:
        content = requests.get(url.format(celex_id)).text
        if 'The requested document does not exist.' in content:
            print(celex_id + ' DOES NOT EXIST IN ENGLISH')
            raise Exception
        with open(filename, 'w', encoding='utf-8') as file:
            cleantext = BeautifulSoup(file.read(), "lxml").text
            file.write(cleantext)
    except:
        print.info(celex_id + ' ERROR')


if __name__ == '__main__':
    download_celex_id()
