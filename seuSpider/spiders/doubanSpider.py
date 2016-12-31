# -*- coding:utf-8 -*-
'''
Created on 2016年10月3日

@author: MQ
'''
from seuSpider.scrapy_redis_seu.spiders import RedisSpider
import json
from seuSpider.items.doubanItems import shortCommentItem,shortCommentItemLs
from seuSpider.items.doubanItems import reviewItem,reviewItemLs
import logging

class DoubanRelationSpider(RedisSpider):
    name = 'douban_relations'
    redis_key = 'douban_frelation'
    start_urls = []
    user_list = []

    pre_user_count = 1
    custom_settings={
        'ITEM_PIPELINES' : {
            'sina_scra.pipelines.doubanPipeline': 300
                           },
        'DOWNLOADER_MIDDLEWARES' : {
            'sina_scra.ipproxy.middleware.UserAgentMiddleware': 543,
            'sina_scra.ipproxy.middleware.noProxyMiddleware':544,
            'sina_scra.ipproxy.middleware.CookiesMiddleware': 543
        }
                     }
    user_current_index = 0
    def __init__(self, *args, **kwargs):
        print '-----__init__--------'
        super(DoubanRelationSpider, self).__init__(*args, **kwargs)

    #redis 爬取
    def parse(self,response):
        print '-----parse--------'
        #获取返回json数据
        json_data = json.loads(response.body)
        item = shortCommentItem()
        itemLs = shortCommentItemLs()
        
        for interest in json_data["interests"]:
            itemLs.cuidLs.append(interest["user"]["id"])
            itemLs.commentIdLs.append(interest["id"])
            itemLs.commentLs.append(interest["comment"])
            if type(interest["rating"])== type(None):
                itemLs.ratingLs.append("null")
            else:
                itemLs.ratingLs.append(str(interest["rating"]["count"])+","+str(interest["rating"]["max"])+","+str(interest["rating"]["value"]))
            itemLs.vote_countLs.append(interest["vote_count"])
            itemLs.create_timeLs.append(interest["create_time"])
        item["cuid"] = itemLs.cuidLs
        item["commentId"] = itemLs.commentIdLs
        item["comment"]= itemLs.commentLs
        item["rating"] = itemLs.ratingLs
        item["vote_count"] = itemLs.vote_countLs
        item["create_time"] = itemLs.create_timeLs
        yield item
        
        

    @staticmethod
    def close(spider, reason):
        logging.error('Spider closed ==========================================>'+str(reason))
        #重启spider

class DoubanReviewsSpider(RedisSpider):
    name = 'douban_reviews'
    redis_key = 'douban_reviews'
    start_urls = []
    user_list = []

    pre_user_count = 1
    custom_settings={
        'ITEM_PIPELINES' : {
            'sina_scra.pipelines.doubanReviewPipeline': 300
                           },
        'DOWNLOADER_MIDDLEWARES' : {
            'sina_scra.ipproxy.middleware.UserAgentMiddleware': 543,
            'sina_scra.ipproxy.middleware.noProxyMiddleware':544,
            'sina_scra.ipproxy.middleware.CookiesMiddleware': 543
        }
                     }
    user_current_index = 0
    def __init__(self, *args, **kwargs):
        print '-----__init__--------'
        super(DoubanReviewsSpider, self).__init__(*args, **kwargs)

    #redis 爬取
    def parse(self,response):
        print '-----parse--------'
        #获取返回json数据
        json_data = json.loads(response.body)
        item = reviewItem()
        itemLs = reviewItemLs()
        
        for reviews in json_data["reviews"]:
            itemLs.cuidLs.append(reviews["user"]["id"])
            itemLs.reviewIdLs.append(reviews["id"])
            itemLs.titleLs.append(reviews["title"])
            if type(reviews["rating"])== type(None):
                itemLs.ratingLs.append("null")
            else:
                itemLs.ratingLs.append(str(reviews["rating"]["count"])+","+str(reviews["rating"]["max"])+","+str(reviews["rating"]["value"]))
            itemLs.useful_countLs.append(reviews["useful_count"])
            itemLs.likers_countLs.append(reviews["likers_count"])
            itemLs.vote_statusLs.append(reviews["vote_status"])
            itemLs.useless_countLs.append(reviews["useless_count"])
            itemLs.create_timeLs.append(reviews["create_time"])
            itemLs.comments_countLs.append(reviews["comments_count"])
            
        item["cuid"] = itemLs.cuidLs
        item["reviewId"] = itemLs.reviewIdLs
        item["title"]= itemLs.titleLs
        item["rating"] = itemLs.ratingLs
        item["useful_count"] = itemLs.useful_countLs
        item["likers_count"] = itemLs.likers_countLs
        item["vote_status"] = itemLs.vote_statusLs
        item["useless_count"] = itemLs.useless_countLs
        item["comments_count"] = itemLs.comments_countLs
        item["create_time"] = itemLs.create_timeLs
        yield item
        
        

    @staticmethod
    def close(spider, reason):
        logging.error('Spider closed ==========================================>'+str(reason))
        #重启spider