# -*- coding:utf-8 -*-
'''
Created on 2016年12月30日

@author: MQ
'''
# import sys
import logging
# import getopt
import json
from scrapy import Request
from seuSpider.utils.dbManager2 import dbManager2
from seuSpider.scrapy_redis_seu.spiders import RedisSpider
# from seuSpiderHandlers.doubanHandler import doubanHandler
from seuSpiderHandlers.sinaHandler import sinaHandler

class spiderWorker(RedisSpider):
    """运行第一个参数
    
    """
    name = 'spider_main'
    redis_key = 'sina_frelation'#运行时需改变
    start_urls = []
    conn = dbManager2()
    
#     custom_settings={
#         'ITEM_PIPELINES' : {
#             'seuSpider.pipelines.doubanReviewPipeline': 300
#                            },
#         'DOWNLOADER_MIDDLEWARES' : {
#             'seuSpider.ipproxy.middleware.UserAgentMiddleware': 543,
#             'seuSpider.ipproxy.middleware.noProxyMiddleware':544,
#             'seuSpider.ipproxy.middleware.CookiesMiddleware': 543
#         }
#     }
    
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
#         opts, args = getopt.getopt(sys.argv[1:], "hk:")
#         for op,value in opts:
#             if op == "-k":
#                 self.redis_key = value
#                 logging.info("REDIS_KEY = %s",self.redis_key)
#             else:
#                 sys.exit()
            

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
            item1,item2 = sinaHandler().userRelationHandler(json_data, response.url)
            yield item1
            yield item2
#             yield doubanHandler().reviewHandler(json_data)

    @staticmethod
    def close(spider, reason):
        logging.error('Spider closed ==========================================>'+str(reason))
        #重启spider
