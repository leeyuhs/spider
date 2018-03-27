#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lee
import requests
import re
import time
import json
import os
import random


def strip(path):
    path = re.sub(r'[? \\*``<>:/]', '', str(path))
    return path


#爬虫类
class Spider:
    def __init__(self):
        self.session =requests.Session()
    def run(self,start_url):
        img_ids = self.get_img_item_ids(start_url)
        #print(img_ids)
        for img_id in img_ids:
            img_item_info = self.get_img_item_info(img_id)
            #print(img_item_info)
            #exit()
            self.save_img(img_item_info)
    #下载器
    def download(self,url):
        try:
            return self.session.get(url)
        except Exception as e :
            print(e)
    #返回套图id列表
    def get_img_item_ids(self,start_url):
        responce = self.download(start_url)
        if responce:
            html = responce.text
            ids = re.findall(r'http://tu.duowan.com/gallery/(\d+).html',html)
           # print(ids)
            return set(ids)
    #根据套图id获取套图信息
    def get_img_item_info(self,img_id):
        #http://tu.duowan.com/index.php?r=show/getByGallery/&gid=136187&_=1514454642571
        img_item_url = "http://tu.duowan.com/index.php?r=show/getByGallery/&gid=%s&_=%s" % (img_id,int(time.time()*1000))
        response = self.download(img_item_url)
        if response:
            data = json.loads(response.text)
          #  print(data)
            return json.loads(response.text)

        #根据套图的信息，持久化
    def save_img(self, img_item_info):
        dir_name = strip(img_item_info['gallery_title'].strip())
      #  print(dir_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        for img_info in img_item_info['picInfo']:
            img_name = strip(img_info['title'].strip())
            img_url = img_info['url']
            pix = (img_url.split('/')[-1]).split('.')[-1]
            #图片的全路径
            img_path = os.path.join(dir_name,"%s.%s" % (img_name,pix))
            if not os.path.exists(img_path):
                responce = self.download(img_url)
                print(img_url)
                if responce:
                    img_data = responce.content
                    with open(img_path, 'wb') as f:
                        f.write(img_data)


if __name__ == '__main__':
    spider = Spider()
    start_url = 'http://tu.duowan.com/m/meinv'
    spider.run(start_url)
