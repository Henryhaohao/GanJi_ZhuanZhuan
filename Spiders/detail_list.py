# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/3/23--17:45
__author__ = 'Henry'

'''
爬取赶集网二手的转转商品信息
'''

# 58同城,赶集网,承压性很好,但是对同一个IP的访问频率做了限制,但是time.sleep不用,所有搭建IP池就好了

import requests, time, pymongo, random, re
from bs4 import BeautifulSoup

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
url_list = ganji['url_list']
item_info = ganji['item_info']


def get_detail_urls(channel, page):
    '''获取某个分类下所有页面的商品的详情页URL'''
    # eg:http://bj.ganji.com/shouji/o1/
    url = '{}o{}/'.format(channel, str(page))
    html = requests.get(url).text
    urls = re.findall(r'class="img">\s*<a href="(.*?detail.*?)\?', html)
    print(url)
    if urls:
        for url in urls:
            print(url)  # 一页60条
            url_list.insert_one({'url': url})
    else:
        print('这是最后一页了!')
        pass


# get_detail_urls('http://bj.ganji.com/shouji/',1)


def get_item_info(url):
    '''获取商品的详情信息'''
    html = requests.get(url)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, 'lxml')
        title = soup.select('.box_left_top > h1')[0].get_text()
        if title != '':
            price = soup.select('.price_now > i')[0].get_text()
            area = soup.select('.palce_li > span > i')[0].get_text()
            # 以前的地址提取方法(list+map+匿名函数,取出每个a标签中的text组成一个列表得到完整的地址)
            # area = list(map(lambda x:x.text,soup.select('.palce_li > a')))
            data = {
                'title': title,
                'price': price,
                'area': area,
                'url': url,
            }
            print(data)
            try:
                item_info.insert_one(data)
            except:
                # 因为在main.py中给item_info文档建立了url索引,插入重复的数据会DuplicateKeyError异常报错
                print('数据已存在!')
        else:
            print('商品已下架!')
    else:
        print('商品已售出,404错误')

# get_item_info('http://zhuanzhuan.ganji.com/detail/1023461341034053642z.shtml')
