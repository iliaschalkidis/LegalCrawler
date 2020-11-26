import os
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import tqdm
from data import DATA_DIR

dir_root = os.path.join(DATA_DIR, 'ja')

categories_dict = {
'http://www.japaneselawtranslation.go.jp/law/list/?ft=3&ha=2&re=2&dn=200&ia=03&ct.x=70&ct.y=26&bu=4096':'Foreign affairs and Defense',
'http://www.japaneselawtranslation.go.jp/law/list/?ft=3&ha=2&re=2&dn=200&ia=03&ct.x=51&ct.y=12&bu=2048':'Labor, Public welfare and Social welfare',
'http://www.japaneselawtranslation.go.jp/law/list/?ft=3&ha=2&re=2&dn=200&ia=03&ct.x=70&ct.y=18&bu=1024':'Transport and Communication',
'http://www.japaneselawtranslation.go.jp/law/list/?ft=3&ha=2&re=2&dn=200&ia=03&ct.x=34&ct.y=19&bu=512':'Financing and Insurance',
'http://www.japaneselawtranslation.go.jp/law/list/?ft=3&ha=2&re=2&dn=200&ia=03&ct.x=83&ct.y=30&bu=256':'Industries',
'http://www.japaneselawtranslation.go.jp/law/list/?ft=3&ha=2&re=2&dn=200&ia=03&ct.x=26&ct.y=7&bu=128':'Education and Culture',
'http://www.japaneselawtranslation.go.jp/law/list/?ft=3&ha=2&re=2&dn=200&ia=03&ct.x=69&ct.y=23&bu=64':'Tax and Financial affairs',
'http://www.japaneselawtranslation.go.jp/law/list/?ft=3&ha=2&re=2&dn=200&ia=03&ct.x=69&ct.y=25&bu=32':'Construction and Environment',
'http://www.japaneselawtranslation.go.jp/law/list/?ft=3&ha=2&re=2&dn=200&ia=03&ct.x=74&ct.y=11&bu=16':'Criminal affairs and Police',
'http://www.japaneselawtranslation.go.jp/law/list/?ft=3&ha=2&re=2&dn=200&ia=03&ct.x=54&ct.y=11&bu=8':'Civil affairs and Business affairs',
'http://www.japaneselawtranslation.go.jp/law/list/?ft=3&ha=2&re=2&dn=200&ia=03&ct.x=74&ct.y=18&bu=4':'Judiciary',
'http://www.japaneselawtranslation.go.jp/law/list/?ft=3&ha=2&re=2&dn=200&ia=03&ct.x=102&ct.y=26&bu=2':'Constitution and General administration'
}

categories_dict = {v:k for k, v in categories_dict.items()}


def get_file_by_id(category, doc_id):

    try:
        data = urlopen('http://www.japaneselawtranslation.go.jp/law/detail_main?vm=02&id=' + str(doc_id)).read().decode('utf-8')
    except:
        print(f'{doc_id} DOES NOT EXIST')
        return

    soup = BeautifulSoup(data, "html.parser")
    for tag in soup.find_all("span", {'class':'balloon'}):
        tag.replaceWith('')

    for i in soup.find_all('div', {'class':'LawNum'}):
        if re.search(r'(No\.\s?(\d+))', i.get_text()):
            id = re.search(r'(No\.\s?(\d+))', i.get_text()).group(1)
        else:
            id = '0'
        year = re.search(r'(\d+, (\d+))', i.get_text()).group(2)

    file = os.path.join(os.path.join(os.path.join(dir_root, category.replace(' ', '_')), year), id)
    if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))
    with open(file + '.txt', 'w') as output:
        output.write(soup.get_text())


def download_ja_law():
    for category_name, category_url in tqdm.tqdm(categories_dict.items(), total=len(categories_dict)):
        entries = set()
        data = urlopen(category_url).read().decode('utf-8')
        soup = BeautifulSoup(data, "html.parser")
        items1 = soup.find_all("ul", {'class':None})
        for item in items1:
            items2 = item.find_all("li")
            for i in items2:
                if i.find('a')['href'].__contains__('law/detail'):
                    entries.add(i.find('a')['href'])

        entries = sorted(list(entries), key=lambda x: int(str(x.split('&page=')[1])))
        for entry in entries:
            data = urlopen(entry).read().decode('utf-8')
            soup = BeautifulSoup(data, "html.parser")
            items = soup.find_all("iframe", {'class':'footer'})
            for i in items:
                data = urlopen(i['src']).read().decode('utf-8')
                soup = BeautifulSoup(data, "html.parser")
                items2 = soup.find_all("input", {'name':'id'})
                for j in items2:
                    get_file_by_id(category_name, j['value'])


if __name__ == '__main__':
    download_ja_law()