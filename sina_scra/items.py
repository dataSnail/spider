# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaScraItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class UserRelationItem(scrapy.Item):

    uid = scrapy.Field()
    fid = scrapy.Field()

class UserInfoItem(scrapy.Item):
    uid = scrapy.Field()
    scree_name =scrapy.Field()
    profile_img_url = scrapy.Field()
    status_count = scrapy.Field()
    verified = scrapy.Field()
    verified_reason = scrapy.Field()
    gender = scrapy.Field()
    mbtype = scrapy.Field()
    ismember = scrapy.Field()
    fansNum = scrapy.Field()
    description = scrapy.Field()
    verified_type = scrapy.Field()

class SinaWblogItem(scrapy.Item):
    # 新浪用户所有微博
    uid = scrapy.Field()
    mid = scrapy.Field()
    bid = scrapy.Field()
    retweeted_uid = scrapy.Field()
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
    json_text = scrapy.Field()

class SinaUserItem(scrapy.Item):
    uid = scrapy.Field()
    screen_name = scrapy.Field()
    profile_image_url = scrapy.Field()
    statuses_count = scrapy.Field()
    verified = scrapy.Field()
    verified_reason = scrapy.Field()
    gender = scrapy.Field()
    mbtype = scrapy.Field()
    ismember = scrapy.Field()
    fansNum = scrapy.Field()
    description = scrapy.Field()
    verified_type = scrapy.Field()
    insert_time = scrapy.Field()


class SinaFlagItem(scrapy.Item):
    uid = scrapy.Field()
    mid = scrapy.Field()
    wblog_flag = scrapy.Field()
    comment_flag = scrapy.Field()


class SinaAllJsonItem(scrapy.Item):
    uid = scrapy.Field()
    mid = scrapy.Field()
    allJson = scrapy.Field()


class SinaCommentItem(scrapy.Item):
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
