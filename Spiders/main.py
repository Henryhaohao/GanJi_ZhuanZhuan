# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/3/23--20:00
__author__ = 'Henry'

'''
爬取商品详情页的URL
'''

import pymongo
from multiprocessing import Pool
from Spiders.detail_list import get_item_info,get_detail_urls
from Spiders.channel_list import channel_list

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
url_list = ganji['url_list']
item_info = ganji['item_info']

# 防止插入重复数据
# 建立一个唯一索引,名为url,就是详情页的url字段,当插入重复的url数据时,就会报错,插入不了
# 1.先清空表:db.item_info.remove({}) #必须先清空表在插入索引,不然会失败 ('ok':1 才行!)
# 2.建立索引:db.item_info.ensureIndex({'url':1},{'unique':true})
# 3.插入数据:db.item_info.insert({'title': '优米U5，详细私聊，双卡双待，手机配件都在', 'price': '350', 'area': '广州-白云', 'url': 'http://zhuanzhuan.ganji.com/detail/948735353389596685z.shtml'})

# 教程:https://www.cnblogs.com/huangxincheng/archive/2012/02/29/2372699.html
# 删除索引:db.item_info.dropIndex("_name_id_1")
# 创建表:db.createCollection(“TableName”)

def get_all_urls(channel):
    '''获取某个分类所有商品详情的URL'''
    for page in range(1,101):
        get_detail_urls(channel,page)

def process_one():
    '''1.先要获取所有详情页的URL'''
    pool.map(get_all_urls, channel_list.split())

def process_two():
    '''2.获取所有的商品详情信息'''
    for url in url_list.find({}, {'url': 1, '_id': 0}):  # 查询所有数据打印出URL字段,把默认的_id给去掉才行
        print(url['url'])
        pool.apply_async(get_item_info, (url['url'],))  # apply_async异步非阻塞; apply:阻塞,已经淘汰了


if __name__ == '__main__':
    pool = Pool(processes=8)
    # 注意:先单独运行process_one()生成url_list,再单独运行process_two生成item_list
    process_one()
    # process_two()

    # 关闭进程池
    pool.close()
    pool.join()
    print('爬取完成!')
