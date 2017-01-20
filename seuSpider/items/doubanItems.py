# -*- coding:utf-8 -*-  
'''
Created on 2016年12月22日

@author: MQ
电影：长评、短评、长评和短评人信息
用户：关注、粉丝、小组、广播、书影音
小组：成员
'''
import scrapy

class doubanRelationItem(scrapy.Item):
    """豆瓣好友关系
    """
    #用户id
    uid = scrapy.Field()
    #用户关注者id
    fid = scrapy.Field()

class doubanShortCommentItem(scrapy.Item):
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


class doubanUserItem(scrapy.Item):
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

class doubanUserInfoItem(scrapy.Item):
    """用户详细信息
    """
    #用户数字id
    id = scrapy.Field()
    #用户字符id，可能跟数字id重复
    uid = scrapy.Field()
    #用户关注数量
    following_count = scrapy.Field()
    #
    seti_channel_count = scrapy.Field()
    #用户照片专辑数量
    photo_albums_count = scrapy.Field()
    #用户简介
    abstract = scrapy.Field()
    #用户信息
    intro = scrapy.Field()
    #用户notes（日记?)数量
    notes_count = scrapy.Field()
    #用户位置信息
    loc = scrapy.Field()
    #用户注册时间
    reg_time = scrapy.Field()
    #用户加入小组数量
    joined_group_count = scrapy.Field()
    #用户粉丝数量
    followers_count = scrapy.Field()
    #用户是否手机绑定
    is_phone_bound = scrapy.Field()
    #用户认证类型
    verify_type = scrapy.Field()
    #
    updated_profile = scrapy.Field()
    #
    type = scrapy.Field()
    #用户装填数量
    statuses_count = scrapy.Field()
    #
    group_chat_count = scrapy.Field()
    #用户拥有豆单数量
    owned_doulist_count = scrapy.Field()
    #用户生日
    birthday = scrapy.Field()
    #
    collected_subjects_count = scrapy.Field()
    #用户屏显名字
    name = scrapy.Field()
    #用户性别
    gender = scrapy.Field()
    #用户认证理由
    verify_reason = scrapy.Field()
    #
    ark_published_count = scrapy.Field()
    #
    following_doulist_count = scrapy.Field()
    #
    is_normal = scrapy.Field()


class doubanReviewItem(scrapy.Item):
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
    
class doubanReviewCommentItem(scrapy.Item):
    """豆瓣影评的回应Item
    +++由于关于某个影评的回应都在同一个影评id下，所以默认回应的回应都在爬取的范围内，不再重新进行爬取，只记录id
    """
    #回应id
    rcid = scrapy.Field()
    #回应的影评id
    rid = scrapy.Field()
    #回应的用户id
    uid = scrapy.Field()
    #回应的回复
    rrcid = scrapy.Field()
    #回应文本
    text = scrapy.Field()
    #回应时间
    create_time = scrapy.Field()
    
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

class userInfoItemLs(object):
    """用户详细信息
    """
    def __init__(self):
        #用户数字id
        self.idLs = []
        #用户字符id，可能跟数字id重复
        self.uidLs = []
        #用户关注数量
        self.following_countLs = []
        #
        self.seti_channel_countLs = []
        #用户照片专辑数量
        self.photo_albums_countLs = []
        #用户简介
        self.abstractLs = []
        #用户信息
        self.introLs = []
        #用户notes（日记?)数量
        self.notes_countLs = []
        #用户位置信息
        self.locLs = []
        #用户注册时间
        self.reg_timeLs = []
        #用户加入小组数量
        self.joined_group_countLs = []
        #用户粉丝数量
        self.followers_countLs = []
        #用户是否手机绑定
        self.is_phone_boundLs = []
        #用户认证类型
        self.verify_typeLs = []
        #
        self.updated_profileLs = []
        #
        self.typeLs = []
        #用户装填数量
        self.statues_countLs = []
        #
        self.group_chat_countLs = []
        #用户拥有豆单数量
        self.owned_doulist_countLs = []
        #用户生日
        self.birthdayLs = []
        #
        self.collected_subjects_countLs = []
        #用户屏显名字
        self.nameLs = []
        #用户性别
        self.genderLs = []
        #用户认证理由
        self.verify_reasonLs = []
        #
        self.ark_published_countLs = []
        #
        self.following_doulist_countLs = []
        #
        self.is_normalLs = []
   
class doubanReviewCommentItemLs(object):
    """豆瓣影评的回应Item
    """
    def __init__(self):
        #回应id
        self.rcidLs = []
        #回应的影评id
        self.ridLs = []
        #回应的用户id
        self.uidLs = []
        #回应的回复
        self.rrcidLs = []
        #回应文本
        self.textLs = []
        #回应时间
        self.create_timeLs = []
        