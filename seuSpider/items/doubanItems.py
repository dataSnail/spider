# -*- coding:utf-8 -*-  
'''
Created on 2016年12月22日

@author: MQ
'''
import scrapy

class shortCommentItem(scrapy.Item):
    """短评Item
    """
    #短评人ID
    cuid = scrapy.Field()
    #短评ID
    commentId = scrapy.Field()
    #短评内容
    comment = scrapy.Field()
    #电影评分count,max,value
    rating = scrapy.Field()
    #短评点赞数目
    vote_count = scrapy.Field()
    #短评时间
    create_time = scrapy.Field()


class shortCommentItemLs(object):
    """短评Item 列表
    +++封装 传递给pipeline
    """
    #短评人ID
    cuidLs = []
    #短评ID
    commentIdLs = []
    #短评内容
    commentLs = []
    #电影评分count,max,value
    ratingLs = []
    #短评点赞数目
    vote_countLs = []
    #短评时间
    create_timeLs = []
    

class userItem(scrapy.Item):
    """用户信息Item
    """
    #用户数字Id
    unid = scrapy.Field()
    #用户名id
    uid = scrapy.Field()
    #关注数
    following_count = scrapy.Field()
    #介绍
    intro = scrapy.Field()
    #note数量
    note_count = scrapy.Field()
    #位置信息
    loc = scrapy.Field()
    #注册时间
    reg_time = scrapy.Field()
    #加入小组数
    joined_group_count = scrapy.Field()
    #粉丝数
    followers_count = scrapy.Field()
    #状态数目
    statuses_count = scrapy.Field()
    #
    group_chat_count = scrapy.Field()
    #生日
    birthday = scrapy.Field()
    #屏显名字
    name = scrapy.Field()
    #性别
    gender = scrapy.Field()


"""影评Item和影评ItemLs
"""
class reviewItem(scrapy.Item):
    """影评Item
    """
    #影评人ID
    cuid = scrapy.Field()
    #影评ID
    reviewId = scrapy.Field()
    #影评标题
    title = scrapy.Field()
    #影评评分count,max,value
    rating = scrapy.Field()
    #影评有用数目
    useful_count = scrapy.Field()
    #影评点赞数目
    likers_count = scrapy.Field()
    #影评点赞数目
    vote_status = scrapy.Field()
    #影评无用数量
    useless_count = scrapy.Field()
    #影评时间
    create_time = scrapy.Field()
    
    comments_count = scrapy.Field()

class reviewItemLs(object):
    """影评Item 列表
    +++封装 传递给pipeline
    """
    #影评人ID
    cuidLs = []
    #影评ID
    reviewIdLs = []
    #影评标题
    titleLs = []
    #影评评分count,max,value
    ratingLs = []
    #影评有用数目
    useful_countLs = []
    #影评点赞数目
    likers_countLs = []
    #影评点赞数目
    vote_statusLs = []
    #影评无用数量
    useless_countLs = []
    #影评时间
    create_timeLs = []
    
    comments_countLs = []
