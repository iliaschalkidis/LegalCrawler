import os
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import tqdm
from data import DATA_DIR

dir_root = os.path.join(DATA_DIR, 'fin')
prefix = 'http://www.finlex.fi'


def get_file_by_id(year, id, url, i):
    file = os.path.join(os.path.join(dir_root, year), id)
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    os.system('wget \'' + prefix + url + '.pdf\' -O \'' + os.path.join(os.path.join(dir_root, year), id) + '.pdf\' -q')
    if not os.stat(os.path.join(os.path.join(dir_root, year), id) + '.pdf').st_size == 0:
        os.system('pdftotext \'' + os.path.join(os.path.join(dir_root, year), id) + '.pdf\' ' + os.path.join(os.path.join(dir_root, year), id) + '.txt -q')
    else:
        with open(os.path.join(dir_root, 'log.txt'), 'a') as log:
            log.write(os.path.join(os.path.join(dir_root, year), id) + '.pdf' + '|' + url + '|' + str(i) + '\n')
    os.remove(os.path.join(os.path.join(dir_root, year), id) + '.pdf')


def download_fin_law():
    for i in tqdm.tqdm(range(0, 1041, 20), total=len(list(range(0, 1041, 20)))):
        data = urlopen('https://www.finlex.fi/en/laki/kaannokset/aakkos.php?lang=en&_offset=' + str(i)).read().decode('utf-8')
        soup = BeautifulSoup(data, "html.parser")
        titles = soup.find_all("dt", {'class': 'doc'})
        contents = soup.find_all("dd", {'class': 'desc'})
        for item in zip(titles, contents):
            regex = r'((\d+)/(\d+) English)'
            id = re.search(regex, item[0].find('a').get_text()).group(2)
            year = re.search(regex, item[0].find('a').get_text()).group(3)

            url = item[1].find('a')['href']

            get_file_by_id(year, id, url, i)


if __name__ == '__main__':
    download_fin_law()
