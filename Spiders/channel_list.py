# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/3/23--17:23
__author__ = 'Henry'

'''
爬取赶集网二手商品的所有分类
'''

import requests
from bs4 import BeautifulSoup

url = 'http://bj.Ganji.com/wu/'
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')
# print(soup)
channel = soup.select('div.content > div > div > dl > dt > a')
# print(channel)
for i in channel:
    channel_url = 'http://bj.Ganji.com' + i.get('href')
    # print(channel_url)

# 分类列表
channel_list = '''
    http://bj.Ganji.com/jiaju/
    http://bj.Ganji.com/rirongbaihuo/
    http://bj.Ganji.com/shouji/
    http://bj.Ganji.com/jiadian/
    http://bj.Ganji.com/ershoubijibendiannao/
    http://bj.Ganji.com/ruanjiantushu/
    http://bj.Ganji.com/yingyouyunfu/
    http://bj.Ganji.com/diannao/
    http://bj.Ganji.com/fushixiaobaxuemao/
    http://bj.Ganji.com/meironghuazhuang/
    http://bj.Ganji.com/shuma/
    http://bj.Ganji.com/laonianyongpin/
    '''
