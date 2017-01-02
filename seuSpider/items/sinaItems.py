# -*- coding:utf-8 -*-  
'''
Created on 2016年12月30日

@author: MQ
'''
import scrapy

class userRelationItem(scrapy.Item):
    #用户id
    uid = scrapy.Field()
    #关注目标用户id
    fid = scrapy.Field()

class userInfoItem(scrapy.Item):
    uid = scrapy.Field()
    scree_name =scrapy.Field()
    profile_img_url = scrapy.Field()
    status_count = scrapy.Field()
    verified = scrapy.Field()
    verified_reason = scrapy.Field()
    gender = scrapy.Field()
    mbtype = scrapy.Field()
    mbrank = scrapy.Field()
    followers_count = scrapy.Field()
    description = scrapy.Field()
    verified_type = scrapy.Field()
    
class mblogItem(scrapy.Item):
    # 新浪用户所有微博
    uid = scrapy.Field()
    mid = scrapy.Field()
    bid = scrapy.Field()
    retweeted_mid = scrapy.Field()
    text = scrapy.Field()
    isLongText = scrapy.Field()
    source = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    like_count = scrapy.Field()
    hasPic = scrapy.Field()
    hasGif = scrapy.Field()
    hasOutlink = scrapy.Field()
    created_timestamp = scrapy.Field()
    crawl_timestamp = scrapy.Field()

class commentItem(scrapy.Item):
    # 评论
    uid = scrapy.Field()
    cid = scrapy.Field()
    mid = scrapy.Field()
    reply_id = scrapy.Field()
    text = scrapy.Field()
    source = scrapy.Field()
    like_counts = scrapy.Field()
    created_at = scrapy.Field()
    crawl_timestamp = scrapy.Field()

#----------list-------------
class userRelationitemLs(object):
    #用户id
    uidLs = []
    #关注目标用户id
    fidLs = []
class userInfoItemLs(object):
    uidLs =  []
    scree_nameLs = []
    profile_img_urlLs =  []
    status_countLs =  []
    verifiedLs =  []
    verified_reasonLs =  []
    genderLs =  []
    mbtypeLs =  []
    mbrankLs =  []
    followers_countLs =  []
    descriptionLs =  []
    verified_typeLs =  []
    
class sinaWblogItemLs(scrapy.Item):
    # 新浪用户所有微博
    uidLs = []
    midLs = []
    bidLs = []
    retweeted_midLs = []
    textLs = []
    isLongTextLs = []
    sourceLs = []
    reposts_countLs = []
    comments_countLs = []
    attitudes_countLs = []
    like_countLs = []
    hasPicLs = []
    hasGifLs = []
    hasOutlinkLs = []
    created_timestampLs = []
    crawl_timestampLs = []