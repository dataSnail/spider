# -*- coding: utf-8 -*-
from seuSpider.utils.dbManager import dbManager
from seuSpider.spiderHandlers.sinaHandler import sinaHandler
from seuSpider.items.sinaItems import userInfoItem,userRelationItem,sinaMblogItem,sinaCommentItem
from seuSpider.spiderHandlers.doubanHandler import doubanHandler
from seuSpider.items.doubanItems import doubanShortCommentItem, doubanReviewItem,\
    doubanRelationItem, doubanUserItem,doubanReviewCommentItem,\
    doubanUserGroupRelationItem, doubanFilmItem
from seuSpider.items.doubanItems import doubanUserInfoItem

class sinaPipeline(object):
    __sinaHandlerInstance = sinaHandler()
    __dbpool = dbManager().get_dbpool()
    def __init__(self):
        pass

    def process_item(self, item, spider):
        if item.__class__ == userRelationItem:
            self.__dbpool.runInteraction(self.__sinaHandlerInstance.sinaRelationDBHandler,item)
        if item.__class__ == userInfoItem:
            self.__dbpool.runInteraction(self.__sinaHandlerInstance.sinaUserInfoDBHandler,item)
        if item.__class__ == sinaMblogItem:
            self.__dbpool.runInteraction(self.__sinaHandlerInstance.sinaMblogDBHandler,item)
        if item.__class__ == sinaCommentItem:
            self.__dbpool.runInteraction(self.__sinaHandlerInstance.sinaCommentDBHandler,item)
        return item

class doubanPipeline(object):
    __doubanHandlerInstance = doubanHandler()
    __dbpool = dbManager().get_dbpool()
    def __init__(self):
        pass
        
    def process_item(self, item, spider):
        if item.__class__ == doubanShortCommentItem:#豆瓣电影短评
            self.__dbpool.runInteraction(self.__doubanHandlerInstance.commentDBHandler,item)
        if item.__class__ == doubanReviewItem:#豆瓣电影长评
            self.__dbpool.runInteraction(self.__doubanHandlerInstance.reviewDBHandler,item)
        if item.__class__ == doubanRelationItem:#豆瓣关系（包含关注关系和粉丝关系都可用）
            self.__dbpool.runInteraction(self.__doubanHandlerInstance.relationDBHandler,item)
#         if item.__class__ == doubanUserItem:
#             self.__dbpool.runInteraction(self.__doubanHandlerInstance.userDBHandler,item)
        if item.__class__ == doubanUserInfoItem:#豆瓣用户信息
            self.__dbpool.runInteraction(self.__doubanHandlerInstance.userInfoDBHandler, item)
        if item.__class__ == doubanReviewCommentItem:#豆瓣长评回复
            self.__dbpool.runInteraction(self.__doubanHandlerInstance.reviewCommentDBHandler,item)
        if item.__class__ == doubanUserGroupRelationItem:#豆瓣组关系
            self.__dbpool.runInteraction(self.__doubanHandlerInstance.userGroupRelationDBHandler,item)
        if item.__class__ == doubanFilmItem:#豆瓣电影信息
            self.__dbpool.runInteraction(self.__doubanHandlerInstance.filmInfoDBHandler, item)
        return item
        

