# -*- coding:utf-8 -*-  
'''
Created on 2016年12月22日

@author: MQ
电影：长评、短评、长评和短评人信息
用户：关注、粉丝、小组、广播、书影音
小组：成员
'''
import scrapy

class relationItem(scrapy.Item):
    """豆瓣好友关系
    """
    #用户id
    uid = scrapy.Field()
    #用户关注者id
    fid = scrapy.Field()

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

#----- Ls封装 传递给pipeline----------
class relationItemLs(object):
    """豆瓣好友关系
    """
    def __init__(self):
        #用户id
        self.uidLs = []
        #用户关注者id
        self.fidLs = []
    
class shortCommentItemLs(object):
    """短评Item 列表
    """
    def __init__(self):
        #短评人ID
        self.cuidLs = []
        #短评ID
        self.commentIdLs = []
        #短评内容
        self.commentLs = []
        #电影评分count,max,value
        self.ratingLs = []
        #短评点赞数目
        self.vote_countLs = []
        #短评时间
        self.create_timeLs = []
    
class reviewItemLs(object):
    """影评Item 列表
    """
    def __init__(self):
        #影评人ID
        self.cuidLs = []
        #影评ID
        self.reviewIdLs = []
        #影评标题
        self.titleLs = []
        #影评评分count,max,value
        self.ratingLs = []
        #影评有用数目
        self.useful_countLs = []
        #影评点赞数目
        self.likers_countLs = []
        #影评点赞数目
        self.vote_statusLs = []
        #影评无用数量
        self.useless_countLs = []
        #影评时间
        self.create_timeLs = []
        
        self.comments_countLs = []
    
class userItemLs(object):
    """用户信息Item
    """
    def __init__(self):
        #用户数字Id
        self.unidLs = []
        #用户名id
        self.uidLs = []
        #关注数
        self.following_countLs = []
        #介绍
        self.introLs = []
        #note数量
        self.note_countLs = []
        #位置信息
        self.locLs = []
        #注册时间
        self.reg_timeLs = []
        #加入小组数
        self.joined_group_countLs = []
        #粉丝数
        self.followers_countLs = []
        #状态数目
        self.statuses_countLs = []
        #
        self.group_chat_countLs = []
        #生日
        self.birthdayLs = []
        #屏显名字
        self.nameLs = []
        #性别
        self.genderLs = []
