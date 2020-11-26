import os
import string
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import tqdm
from data import DATA_DIR


def clear_corpus(root):
    time.sleep(20)
    remove = []
    for root, _, files in os.walk(root):
        for file in files:
            text_file = os.path.join(root, file)
            if text_file.__contains__('.pdf'):
                remove.append(text_file)

    for i in remove:
        os.remove(i)


def get_file_by_id(prefix, root, year, url, i, split):
    year = str(year)
    if not os.path.exists(os.path.dirname(os.path.join(os.path.join(root, year), url) + '.pdf')):
        os.makedirs(os.path.dirname(os.path.join(os.path.join(root, year), url) + '.pdf'))

    os.system('wget \'' + prefix + url + '.pdf\' -O \'' + os.path.join(os.path.join(root, year), url) + '.pdf\' -q')
    if not os.stat(os.path.join(os.path.join(root, year), url) + '.pdf').st_size == 0:
        if split:
            os.system('pdftocairo -pdf \'' + os.path.join(os.path.join(root, year), url) + '.pdf\' \'' + os.path.join(os.path.join(root, year), url) + '_cleared.pdf\'')
            os.system('mutool poster -x 2 \'' + os.path.join(os.path.join(root, year), url) + '_cleared.pdf\' \'' + os.path.join(os.path.join(root, year), url) + '_ALL_unenc.pdf\'')
            os.system('gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=\'' + os.path.join(os.path.join(root, year), url) + '_ALL.pdf\' -c .setpdfwrite -f \'' + os.path.join(os.path.join(root, year), url) + '_ALL_unenc.pdf\'')
            os.system('pdftk A=\'' + os.path.join(os.path.join(root, year), url) + '_ALL.pdf\' cat Aodd output \'' + os.path.join(os.path.join(root, year), url) + '_odd.pdf\' dont_ask')
            os.system('pdftotext \'' + os.path.join(os.path.join(root, year), url) + '_odd.pdf\' ' + os.path.join(os.path.join(root, year), url) + '.txt -q' )
        else:
            os.system('pdftotext \'' + os.path.join(os.path.join(root, year), url) + '.pdf\' ' + os.path.join(os.path.join(root, year), url) + '.txt -q' )
    else:
        with open(os.path.join(root, 'log.txt'), 'a') as log:
            log.write(os.path.join(os.path.join(root, year), url) + '.pdf' + '|' + url + '|' + str(i) + '\n')


def download_ca_law(data_list=None):
    if data_list is None:
        data_list = ['annual_statutes', 'regulations', 'consolidated_acts']
    dir_root = os.path.join(DATA_DIR, 'ca/annual_statutes')
    prefix = 'http://laws.justice.gc.ca/PDF/'

    if 'annual_statutes' in data_list:
        for i in tqdm.tqdm(range(2001, 2021), total=len(list(range(2001, 2021)))):
            data = urlopen('http://laws.justice.gc.ca/eng/AnnualStatutes/index' + str(i) + '.html').read().decode('utf-8')
            soup = BeautifulSoup(data, "html.parser")

            list_items = soup.find("ul", {'class':'wet-boew-zebra'})
            items = list_items.find_all('a')
            for item in items:
                year = i
                url = item['href']

                get_file_by_id(prefix, dir_root, year, url, i, True)


        clear_corpus(dir_root)

    regulations = [char for char in string.ascii_uppercase if char != 'X' and char != 'Z']
    regulations.append('NUM')

    dir_root = os.path.join(DATA_DIR, 'ca/regulations')
    prefix = 'http://laws.justice.gc.ca/'

    if 'regulations' in data_list:
        for regulation in tqdm.tqdm(regulations):
            data = urlopen('http://laws.justice.gc.ca/eng/regulations/' + str(regulation) + '.html').read().decode('utf-8')
            soup = BeautifulSoup(data, "html.parser")

            items = soup.find_all('span', {'class': 'pdfLink'})
            for item in items:
                year = regulation
                url = item.find('a')['href']

                get_file_by_id(prefix, dir_root, year, url[1:-4], regulation, True)

        clear_corpus(dir_root)

    dir_root = '/mnt/data/processed_files/CAN_Legislation/consolidated_acts/'
    prefix = 'http://laws.justice.gc.ca/'

    acts = [char for char in string.ascii_uppercase if char != 'X' and char != 'Z']

    if 'consolidated_acts' in data_list:
        for act in tqdm.tqdm(acts):
            data = urlopen('http://laws.justice.gc.ca/eng/acts/' + str(act) + '.html').read().decode('utf-8')
            soup = BeautifulSoup(data, "html.parser")

            items = soup.find_all('span', {'class': 'pdfLink'})
            for item in items:
                year = act
                url = item.find('a')['href']

                get_file_by_id(prefix, dir_root, year, url[1:-4], act, True)

        clear_corpus(dir_root)


if __name__ == '__main__':
    download_ca_law()
