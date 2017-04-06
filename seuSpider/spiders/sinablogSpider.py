# -*- coding:utf-8 -*-  
'''
Created on 2017年3月21日

@author: MQ
'''
import re
import logging
import json
from scrapy import Request
from seuSpider.scrapy_redis_seu.spiders import RedisSpider
from seuSpider.spiderHandlers.sinaHandler import sinaHandler

class spiderWorker(RedisSpider):
    """运行第一个参数
    
    """
    name = 'sinaBlogSpider'
    redis_key = 'sinaBlog'#运行时需改变
    start_urls = []
    
    custom_settings={
        'ITEM_PIPELINES' : {
            'seuSpider.pipelines.sinaPipeline': 300
                           },
        'DOWNLOADER_MIDDLEWARES' : {
            'seuSpider.ipproxy.middleware.UserAgentMiddleware': 543,
#             'seuSpider.ipproxy.middleware.noProxyMiddleware':544,
#             'seuSpider.ipproxy.middleware.CookiesMiddleware': 543
        }
    }
    def __init__(self, *args, **kwargs):
        print '-----start spider--------'
        super(spiderWorker, self).__init__(*args, **kwargs)

    #redis 爬取
    def parse(self,response):
        try:
            #获取返回json数据
            json_data = json.loads(response.body)
        except Exception as e:
            #重新请求
            logging.error('\n----------url error----------\n%s\n----------url error---------\njson data is error and the Exception e is ========>%s'%(response.url,str(e)))
#             time.sleep(5)
            #重新请求 ,返回到redis里面，设置优先级
            yield Request(response.url,meta={'dont_redirect': True},dont_filter=True,callback=self.parse)
        else:
            #用户关系
            item = sinaHandler().blogHander(json_data)
            yield item
                
                
    @staticmethod
    def close(spider, reason):
        logging.error('Spider closed ==========================================>'+str(reason))
        #重启spider
