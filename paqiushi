#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lee
import json
import random

import requests
import re
import os


start_url = 'https://www.qiushibaike.com/imgrank/'
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36', }

def strip(path):
    path = re.sub(r'[? \*"``.<>:/]', '', str(path))
    return path
class Spider:

    def run(self, start_url):
        dir_name_o = '就这样'
        if not os.path.exists(dir_name_o):
            os.makedirs(dir_name_o)
        img_ids = self.get_img_ids(start_url)
        for img_id in img_ids:
            img_item_info = self.get_img_info(img_id)
            self.save_img(img_item_info, img_id,dir_name_o)
           # exit()
    def get_img_ids(self,start_url):
        response = requests.get(start_url, headers=header)
        ids = re.findall(r'a href="/article/(\d+)', response.text)
       # print(ids)
        return set(ids)

    def get_img_info(self, img_id):
        img_item_url = "https://www.qiushibaike.com/article/%s" % (img_id)
        response = requests.get(img_item_url, headers=header)
        return response.text

    def save_img(self, img_item_info, img_id, dir_name_o):
      #  dir_name_o = '就这'
       # print(img_item_info)
        dir_name_i = ','.join(re.findall(r'<meta name="description" content="(.*?)" />', img_item_info))
        dir_name = strip(dir_name_i.strip())
      #  print(dir_name)
        img_id_id = (int(img_id)/10000)
        img_url = "https://pic.qiushibaike.com/system/pictures/%d/%d/medium/app%d.jpg" % (img_id_id, int(img_id), int(img_id))
        pix = (img_url.split('/')[-1]).split('.')[-1]
        img_path = os.path.join(dir_name_o, "%s.%s" % (dir_name, pix))
       # print(img_path)
        if not os.path.exists(img_path):
            response = requests.get(img_url, headers=header)
            print(img_url)
            if response:
               # if img_path.strip():
                img_data = response.content
                with open(img_path, 'wb') as f:
                    f.write(img_data)


if __name__ == '__main__':
    spider = Spider()
    for i in range(1, 500):
        spider.run(start_url)
