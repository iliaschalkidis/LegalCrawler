import os
import sys
import requests
from multiprocessing import cpu_count, Pool
from data import DATA_DIR
from bs4 import BeautifulSoup
from crawlers.helpers import clean_text
sys.setrecursionlimit(100000)

dir_root = os.path.join(DATA_DIR, 'uk')

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


def get_file_by_id(original_url):
    url = original_url + '/enacted?view=plain'
    uk_id = original_url.replace('https://legislation.gov.uk/','')
    filename = os.path.join(dir_root, f'{uk_id}.txt')
    try:
        content = requests.get(url).text
        if 'This item of legislation isn’t available on this site' in content or 'View PDF' in content:
            print(url + ' ONLY IN PDF')
            return 0
        elif 'The page you requested could not be found' in content:
            print(url + ' NOT AVAILABLE')
            return 0
        with open(filename, 'w', encoding='utf-8') as file:
            content = clean_text(content)
            cleantext = BeautifulSoup(content, "lxml").find("div", {"id": "content"}).text
            file.write(cleantext)
    except Exception as error:
        print(error)
        print(original_url + ' ERROR')


def download_uk_law():
    types_dict = {'ukpga': (1980, 60), 'ukla': (1991, 60), 'uksi': (1987, 3000), 'asp': (1999, 60), 'ssi': (1999, 600),
                  'wsi': (1999, 350), 'nisi': (1999, 20), 'nia': (2000, 60), 'mwa': (2008, 60), 'ukmo': (2013, 60),
                  'anaw': (2012, 60)}

    possible_links = []
    for act_type, (start_year, last_id) in types_dict.items():
        for year in range(start_year, 2022):
            if not os.path.exists(os.path.join(dir_root, act_type, str(year))):
                os.makedirs(os.path.join(dir_root, act_type, str(year)))
            for id in range(1, last_id+1):
                possible_links.append(f'https://legislation.gov.uk/{act_type}/{year}/{id}')
    with Pool(processes=cpu_count()) as pool:
        pool.map(get_file_by_id, possible_links)


if __name__ == '__main__':
    download_uk_law()
