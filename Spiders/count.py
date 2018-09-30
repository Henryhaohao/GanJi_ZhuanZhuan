# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/3/23--22:00
__author__ = 'Henry'

'''
监控抓取了多少数据
'''

import time
from Spiders.detail_list import item_info

while True:
    # count = url_list.find().count()
    count = item_info.find().count()
    print(count)
    time.sleep(6)

# 3分钟爬完所有URL---61900条
