import os
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool


def main(img_page):
    url = 'http://www.mzitu.com/page/'
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
        'Referer': "http:://http://www.mzitu.com/"}
    parser = 'html.parser'
    cur_path = os.getcwd() + '/'
    start_url = url + str(img_page)
    response = requests.get(start_url, headers=get_item(start_url))
    soup = BeautifulSoup(response.text, parser)
    img_ids = soup.find(id='pins').find_all('a', target='_blank')[1::2]
    for img_id in img_ids:
        dir_name = img_id.get_text().strip().replace('?', '')
        img_id = img_id['href']
        img_id_item = requests.get(img_id, headers=get_item(img_id))
        soup = BeautifulSoup(img_id_item.text, parser)
        img_cnt = soup.find('div', class_='pagenavi').find_all('a')[4].get_text()
        img_path = cur_path + dir_name
        if not os.path.exists(img_path):
            try:
                os.makedirs(img_path)
            except Exception as e:
                print(e)
        try:
            os.chdir(img_path)
        except Exception as e:
            print(e)
        print('下载' + dir_name + '...')
        for img_index in range(1, int(img_cnt) + 1):
            img_link = img_id + '/' + str(img_index)
            cur_page = requests.get(img_link, headers=get_item(img_link))
            soup = BeautifulSoup(cur_page.text, parser)
            img_src = soup.find('div', 'main-image').find('img')['src']
            img_name = img_src.split('/')[-1]
            f = open(img_name, 'wb')
            f.write(requests.get(img_src, headers=get_item(img_src)).content)
            f.close()
        if not os.path.exists(cur_path):
            os.chdir(cur_path)
def get_item(url):
    real_header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36','Referer': str(url)}
    return real_header


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i for i in range(50)])
