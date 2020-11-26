import json
import requests
from bs4 import BeautifulSoup
import tqdm
import re
filename = '/Users/kiddo/Desktop/DATASETS/CJEU_citations.json'



with open(filename) as file:
    data =  json.load(file)['results']['bindings']

    for record in tqdm.tqdm(data):
        case = dict()
        case['celex_id'] = record['act_celex_id']['value']
        url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{}'.format(case['celex_id'])
        try:
            html = requests.get(url).text
        except:
            print('ERROR ', case['celex_id'])
        if record['citations']['value'] == '':
            citations = []
        elif '|' in record['citations']['value']:
            citations = record['citations']['value'].split('|')
        else:
            citations = [record['citations']['value']]
        case['text'] = re.sub('(\n *)+', '\n', re.sub(' +', ' ', BeautifulSoup(html).text.replace(u'\u00a0', ' ')))
        if  re.search('\norder', case['text'].lower()) is None:
            print('ERROR ', case['celex_id'])
            continue
        print('DONE  ', case['celex_id'])
        case['citations'] = citations
        case['publication_date'] =  record['publication_date']['value']
        with open('/Users/kiddo/Desktop/DATASETS/CJEU/{}.json'.format(record['act_celex_id']['value']), 'w') as outfile:
            json.dump(case, outfile, indent=1)
