# -*- coding: utf-8 -*-

# 爬取新浪用户的所有微博，顺便记录下用户信息

from sina_scra.scrapy_redis_seu.spiders import RedisSpider
from scrapy import Request
from scrapy.spiders import Spider
from sina_scra.items import SinaWblogItem
from sina_scra.items import SinaUserItem
from sina_scra.items import SinaFlagItem

import re
import json
import time
import MySQLdb
import MySQLdb.cursors
import logging
import sys
from sina_scra.utils.dbManager2 import dbManager2


class WblogSpider(RedisSpider):
    name = 'sina_wblog'  # 爬虫名称
    allowed_domain = ['weibo.cn']  # 访问的url的域名
    redis_key = 'wblog:start_urls'

    # 不同spider各自的settings
    custom_settings = {
        'ITEM_PIPELINES': {
            'sina_scra.pipelines.WblogPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES' : {
            'sina_scra.ipproxy.middleware.UserAgentMiddleware': 543,
            # 'sina_scra.ipproxy.middleware.noProxyMiddleware':544,
            'sina_scra.ipproxy.middleware.aBuProxyMiddleware':546,
        }
    }

    # 初始化
    def __init__(self, *args, **kwargs):
        logging.info('-----initiating WblogSpider------')
        super(WblogSpider, self).__init__(*args, **kwargs)

    # 解析页面
    def parse(self, response):
        logging.info("parse : " + response.url)

        try:
            render_data = json.loads(response.body)
        except Exception as e:
            #重新请求
            logging.error('json data is wrong on url : %s and the Exception e is ========>%s'%(response.url,str(e)))
            #重新请求 ,返回到redis里面，设置优先级
            yield Request(response.url,meta={'dont_redirect': True},dont_filter=True,callback=self.parse)

        try:
            # mod/pagelist表示当前页有微博内容
            if render_data['cards'][0]['mod_type'] == 'mod/pagelist':
                item = SinaWblogItem()  # 微博内容
                self.init_item(item)

                for status in render_data['cards'][0]['card_group']:
                    mblog = status['mblog']
                    if 'retweeted_status' in mblog.keys():
                        # 如果有原微博，那么也要保存下来
                        if 'deleted' in mblog['retweeted_status']:
                            dItem = SinaWblogItem()  # 被删除的微博内容
                            self.init_item(dItem)
                            self.fill_dItem(dItem, mblog['retweeted_status'])
                            yield dItem
                        else:
                            reItem = SinaWblogItem()
                            self.init_item(reItem)
                            self.fill_item(reItem, mblog['retweeted_status'])
                            yield reItem

                            # 原微博的作者也要保存
                            uItem = SinaUserItem()  # 原微博的作者
                            self.fill_uItem(uItem, mblog['retweeted_status']['user'])
                            yield uItem

                    # 当前用户的微博
                    if 'deleted' in mblog:
                        dItem = SinaWblogItem()
                        self.init_item(dItem)
                        self.fill_dItem(dItem, mblog)
                        yield dItem
                    else:
                        self.fill_item(item, mblog)

                yield item

            else:
                logging.info('empty wblog: ' + response.url)
                try:
                    f = open('noWblogUrls.txt','a')
                    f.write("rpush wblog:start_urls "+str(response.url)+'\n')
                except Exception as e:
                    logging.info('page :::'+str(response.url)+' can not write to file noWblogUrls---------------!!!!!!!')
                finally:
                    f.close()
        except Exception as e:
            logging.error('something is wrong on url : %s and the Exception e is ========>%s'%(response.url,str(e)))

    # 初始化item
    def init_item(self, item):
        item['uid'] = []
        item['mid'] = []
        item['retweeted_uid'] = []
        item['retweeted_mid'] = []
        item['json_text'] = []
        item['created_timestamp'] = []

    # 填写item
    def fill_item(self, item, mblog):
        # 用户id
        if mblog['user']['id']:
            item['uid'].append(mblog['user']['id'])
        else:
            item['uid'].append('0')
        # 微博id
        if mblog['mid']:
            item['mid'].append(mblog['mid'])
        else:
            item['mid'].append('0')
        # 原微博id
        if 'retweeted_status' in mblog.keys():
            item['retweeted_mid'].append(mblog['retweeted_status']['mid'])
            if 'id' in mblog['retweeted_status']['user']:
                item['retweeted_uid'].append(mblog['retweeted_status']['user']['id'])
            else:
                item['retweeted_uid'].append('0')
        else:
            item['retweeted_mid'].append('0')
            item['retweeted_uid'].append('0')
        # 微博内容
        item['json_text'].append(mblog)
        # 爬取微博的时间
        item['crawl_timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # 发微博的时间
        if mblog['created_timestamp']:
            item['created_timestamp'].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mblog['created_timestamp'])))
        else:
            item['created_timestamp'].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    # 填写dItem
    def fill_dItem(self, item, mblog):
        # 用户id
        item['uid'].append('0')
        # 微博id
        if mblog['mid']:
            item['mid'].append(mblog['mid'])
        else:
            item['mid'].append('0')
        # 原微博作者id
        item['retweeted_uid'].append('0')
        # 原微博id
        item['retweeted_mid'].append('0')
        # 微博内容
        item['json_text'].append(mblog)
        # 爬取微博的时间
        item['crawl_timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # 发微博的时间
        if mblog['created_timestamp']:
            item['created_timestamp'].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mblog['created_timestamp'])))
        else:
            item['created_timestamp'].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    # 填写uItem
    def fill_uItem(self, uItem, user):
        uItem['uid'] = user['id'] if user['id'] else '0'
        uItem['screen_name'] = user['screen_name'] if user['screen_name'] else '0'
        uItem['profile_image_url'] = user['profile_image_url'] if user['profile_image_url'] else '0'
        uItem['statuses_count'] = user['statuses_count'] if user['statuses_count'] else '0'
        uItem['verified'] = user['verified'] if user['verified'] else '0'
        uItem['verified_reason'] = user['verified_reason'] if user['verified_reason'] else '0'
        uItem['gender'] = user['gender'] if user['gender'] else '0'
        uItem['mbtype'] = user['mbtype'] if user['mbtype'] else '0'
        uItem['ismember'] = user['ismember'] if user['ismember'] else '0'
        uItem['fansNum'] = user['fansNum'] if user['fansNum'] else '0'
        uItem['description'] = "".join(re.findall(ur"[\u4e00-\u9fa5a-z0-9\w\-\.,@?^=%&amp;:/~\+#<>\s]+", user['description'])) if user['description'] else '0'
        uItem['verified_type'] = user['verified_type'] if user['verified_type'] else '0'
        uItem['insert_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
