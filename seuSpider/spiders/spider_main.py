# -*- coding:utf-8 -*-
'''
Created on 2016年12月30日

@author: MQ
'''
# import sys
import re
import logging
# import getopt
import json
from scrapy import Request
from seuSpider.scrapy_redis_seu.spiders import RedisSpider
# from seuSpiderHandlers.doubanHandler import doubanHandler
from seuSpider.spiderHandlers.sinaHandler import sinaHandler
from seuSpider.spiderHandlers.doubanHandler import doubanHandler

class spiderWorker(RedisSpider):
    """运行第一个参数
    
    """
    name = 'spider_main'
    redis_key = 'douban_film'#运行时需改变
    start_urls = []
    
    custom_settings={
        'ITEM_PIPELINES' : {
#             'seuSpider.pipelines.sinaPipeline': 300,
            'seuSpider.pipelines.doubanPipeline': 300
                           },
        'DOWNLOADER_MIDDLEWARES' : {
            'seuSpider.ipproxy.middleware.UserAgentMiddleware': 543,
#             'seuSpider.ipproxy.middleware.noProxyMiddleware':544,
            'seuSpider.ipproxy.middleware.CookiesMiddleware': 543
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
#             item1,item2 = sinaHandler().userRelationHandler(json_data, response.url)
#             yield item1
#             yield item2
            #----------------------------------------------------------------
#             yield doubanHandler().reviewHandler(json_data)
    
            #----------------------------------------------------------------
#             item1 = doubanHandler().relationHandler(json_data,response.url)
#             yield item1
# #             yield item2
#             extract_uid = re.findall("user/(.+)/followers",response.url)#url相关
#             next_link = "https://m.douban.com/rexxar/api/v2/user/"+extract_uid[0]+"/followers?start=%s&count=20&ck=&for_mobile=1"
#             if json_data["start"]+20<json_data["total"]:
#                 yield Request(url=next_link%(json_data["start"]+20), callback=self.parse)
            #------------------------------------------------------------------------------
#             item = doubanHandler().userInfoHandler(json_data)
#             yield item
            #------------------------------------------------------------------------------
            
#             item = doubanHandler().reviewCommentHandler(json_data,response.url)
#             yield item
#             extract_rid = re.findall("review/(.+)/comments",response.url)#url相关
#             next_link = "https://m.douban.com/rexxar/api/v2/review/"+extract_rid[0]+"/comments?count=25&start=%s&ck=&for_mobile=1"
#             if json_data["start"]+25<json_data["total"]:
#                 yield Request(url=next_link%(json_data["start"]+25), callback=self.parse)


            #--------------------------------------------------------------------------------
#             item = doubanHandler().userGroupRelationHandler(json_data, response.url)
#             yield item
#             extract_rid = re.findall("user/(.+)/joined_groups",response.url)#url相关
#             next_link = "https://m.douban.com/rexxar/api/v2/group/user/"+extract_rid[0]+"/joined_groups?start=%s&count=20&for_mobile=1"
#             if json_data["start"]+20<json_data["total"]:
#                 yield Request(url=next_link%(json_data["start"]+20), callback=self.parse)
            #-------------------------------------------------------------
            if len(json_data)>0:
                logging.info(response.url)
                item = doubanHandler().filmInfoHandler(json_data)
                yield item
                
                extract_start = int(re.findall("start=(.+)&limit=15",response.url)[0])
                extract_year = int(re.findall("tag\/(.+)\/\?type=movie",response.url)[0])
                next_link = 'https://m.douban.com/j/tag/%s/?type=movie&start=%s&limit=15'
                
                if extract_start < 500:
                    yield Request(url=next_link%(str(extract_year),str(extract_start+15)), callback=self.parse) 
            else:
                logging.info(response.url+"::no INFO")
                
                
                
    @staticmethod
    def close(spider, reason):
        logging.error('Spider closed ==========================================>'+str(reason))
        #重启spider
