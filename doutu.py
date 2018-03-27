#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lee
import os
import requests
import re


def strip(path):
    path = re.sub(r'[? \*"``.<>:/]', '', str(path))
    return path


class Spider:
    def run(self, url):
        dir_name = '就这样'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        r = requests.get(url, headers=header)
       # print(r.text)
        img_num = re.findall('http://www.doutula.com/photo/\d+', r.text)
        for prew_img_url in img_num:
            parse_img = requests.get(prew_img_url, headers=header)
            img_url = re.findall('content="http://img.doutula.com/production/uploads/image(.*?)"/>', parse_img.text)
            dir_name_i = re.findall('<td align="center" class="wr pl">(.*?)</td>', parse_img.text)
            print(dir_name_i)
           # print(img_url)
            pre_zui = 'http://img.doutula.com/production/uploads/image'
            real_img_url = pre_zui + ''.join(img_url)
            pix = (real_img_url.split('/')[-1]).split('.')[-1]
           # print(real_img_url)
            dir_name_o = strip(real_img_url.strip())
            img_path = os.path.join(dir_name, "%s.%s" % (dir_name_o, pix))
            dir_name_lst = os.path.join(dir_name, "%s.%s" % (dir_name_i, pix))
            if not os.path.exists(real_img_url):
                response = requests.get(real_img_url, headers=header)
                print(img_path)
                if response:
                    img_data = response.content
                    with open(dir_name_lst, 'wb') as f:
                        f.write(img_data)


if __name__ == '__main__':
    prew_image_cut = 100
    url = 'http://www.doutula.com/photo/list/?page='
    startt_url = 'http://www.doutula.com/photo/list/?page'
    for img_page in range(80, int(prew_image_cut)+1):
        start_url = url + str(img_page)
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
            'Referer': "www.doutula.com/article/list/?page"}
        spider = Spider()
        spider.run(start_url)
