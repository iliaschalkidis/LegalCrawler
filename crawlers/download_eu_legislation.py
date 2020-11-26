import os
import sys
import requests
from functools import partial
from multiprocessing import cpu_count, Pool
from bs4 import BeautifulSoup
from data import DATA_DIR
from crawlers.helpers import clean_text
sys.setrecursionlimit(100000)

root_dir = os.path.join(DATA_DIR, 'eu')

if not os.path.exists(root_dir):
    os.makedirs(root_dir)


def get_file_by_id(celex_id):
    url = f'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex_id}'
    filename = os.path.join(root_dir, f'{celex_id}.txt')
    try:
        content = requests.get(url).text
        if 'The requested document does not exist.' in content:
            print(celex_id + ' DOES NOT EXIST IN ENGLISH')
            raise Exception
        with open(filename, 'w', encoding='utf-8') as file:
            content = clean_text(content)
            if "docHtml" in content:
                cleantext = BeautifulSoup(content, "lxml").find("div", {"id": "docHtml"}).text
            else:
                cleantext = BeautifulSoup(content, "lxml").text
            file.write(cleantext)
    except:
        print(celex_id + ' ERROR')


def download_eu_law():

    sparql_query = """http://publications.europa.eu/webapi/rdf/sparql?default-graph-uri=&query=prefix+cdm%3A+%3Chttp%3A%2F%2Fpublications.europa.eu%2Fontology%2Fcdm%23%3E%0D%0A%0D%0Aselect+%3Fcelex_id%0D%0Awhere+%7B%0D%0A%3Feu_act+cdm%3Aresource_legal_id_celex+%3Fcelex_id.%0D%0A%3Feu_act+a+%3Feu_act_type.%0D%0A%3Feu_act+cdm%3Aresource_legal_number_natural+%3Feu_act_number.%0D%0AFILTER%28%3Feu_act_type+IN+%28cdm%3Aregulation%2C+cdm%3Adirective%2C+cdm%3Adecision%29%29%0D%0A%7D&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+"""

    try:
        content = requests.get(sparql_query).text
        celex_ids = [span.text[1:11] for span in BeautifulSoup(content, "html.parser").find_all('pre')]
    except:
        print('EURLEX SPARQL ENDPOINT NOT RESPONSIVE')
        return 0

    with Pool(processes=cpu_count()) as pool:
        pool.map(partial(get_file_by_id), celex_ids)


if __name__ == '__main__':
    download_eu_law()
