#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: lee
import requests
import re
from pprint import pprint


url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9048'
r = requests.get(url)
pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
result = dict(re.findall(pattern, r.text))
print(result.keys())
print(result.values())
