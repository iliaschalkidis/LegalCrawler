import requests, shutil, zipfile
from bs4 import BeautifulSoup
import glob
import os
import tqdm
import json_lines
from data import DATA_DIR

dir_root = os.path.join(DATA_DIR, 'us_caselaw')


def download_us_caselaw():
    COOKIE_CONTENT = None
    response = requests.get('https://case.law/bulk/download/#researcher',
                            headers={'cookie': COOKIE_CONTENT})

    soup = BeautifulSoup(response.text)

    states = soup.find_all('div', {'class': 'col-12'})

    for col in tqdm.tqdm(states):
        state = col.find('div', {'class': 'section-subtitle'}).text
        url = col.find('a', {'class': 'btn-primary'}).attrs['href']
        response = requests.get(url, stream=True, headers={'cookie': COOKIE_CONTENT})
        state_zip = os.path.join(dir_root, f'{state}.zip')
        handle = open(state_zip, "wb")
        for chunk in response.iter_content(chunk_size=512):
            if chunk:  # filter out keep-alive new chunks
                handle.write(chunk)
        handle.close()
        with zipfile.ZipFile(state_zip) as zf:
            state_tmp = os.path.join(dir_root, f'{state}_temp')
            zf.extractall(state_tmp)
        os.remove(state_zip)
        filenames = glob.glob(f'{state_tmp}/*/data/*')
        jsonl_filename = os.path.join(DATA_DIR, f'{state}.jsonl.xz')
        shutil.move(filenames[0], jsonl_filename)
        shutil.rmtree(state_tmp)
        os.makedirs(os.path.join(dir_root, state))
        with json_lines.open(jsonl_filename) as reader:
            for obj in reader:
                id = obj['id']
                title = obj['reporter']['full_name'] + ' ' + obj['citations'][0]['cite']
                head = obj['casebody']['data']['head_matter']
                opinions = [op['text'] for op in obj['casebody']['data']['opinions']]
                if len(opinions) > 1:
                    opinions = '\n\n'.join(opinions)
                elif len(opinions) == 1:
                    opinions = opinions[0]
                else:
                    opinions = ''
                if len(obj['casebody']['data']['judges']) != 0:
                    judges = obj['court']['name'] + '\n' + obj['casebody']['data']['judges'][0]
                else:
                    judges = obj['court']['name']
                keys = list(obj['casebody']['data'].keys())
                if len(keys) > 5:
                    print('ERROR {}'.format(id))

                with open(os.path.join(dir_root, state, f'{id}.txt'), 'w') as file:
                    file.write(title + '\n' + head + '\n' + opinions + '\n' + judges)
        os.remove(jsonl_filename)


if __name__ == '__main__':
    download_us_caselaw()
