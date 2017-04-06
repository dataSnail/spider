# -*- coding:utf-8 -*-  
'''
Created on 2016年12月30日

@author: MQ
'''
import scrapy

class sinaRelationItem(scrapy.Item):
    """新浪微博用户关系（关注关系、粉丝关系都可用）
    """
    sinaRelation = scrapy.Field()
class sinaRelationItemLs(object):
    """新浪微博用户关系（关注关系、粉丝关系都可用）
    """
    def __init__(self):
        self.sinaRelationLs = []

class sinaBlogItem(scrapy.Field):
    """新浪微博
    """
    sinaBlogEntity = scrapy.Field()
    
class sinaBlogItemLs(object):
    """新浪微博Ls
    """
    def __init__(self):
        self.sinaBlogEntityLs = []
        
class sinaCommentItem(scrapy.Field):
    """新浪微博评论
    """
    sinaCommentEntity = scrapy.Field()
    
class sinaCommentItemLs(object):
    """新浪微博评论Ls
    """
    def __init__(self):
        self.sinaCommentEntityLs = []
class sinaUserItem(scrapy.Field):
    """新浪微博评论
    """
    sinaUserEntity = scrapy.Field()
    
class sinaUserItemLs(object):
    """新浪微博评论Ls
    """
    def __init__(self):
        self.sinaUserEntityLs = []
        