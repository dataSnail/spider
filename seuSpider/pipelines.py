# -*- coding: utf-8 -*-
from seuSpider.utils.dbManager import dbManager
from seuSpider.spiderHandlers.sinaHandler import sinaHandler
from seuSpider.items.sinaItems import sinaCommentItem,\
    sinaRelationItem, sinaBlogItem,sinaUserItem
from seuSpider.spiderHandlers.doubanHandler import doubanHandler
from seuSpider.items.doubanItems import doubanShortCommentItem, doubanReviewItem,\
    doubanRelationItem,doubanReviewCommentItem,\
    doubanUserGroupRelationItem, doubanFilmItem, doubanGroupInfoItem
from seuSpider.items.doubanItems import doubanUserInfoItem

class sinaPipeline(object):
    """新浪数据处理
    """
    __sinaHandlerInstance = sinaHandler()
    __dbpool = dbManager('tim').get_dbpool()
    def __init__(self):
        pass

    def process_item(self, item, spider):
        if item.__class__ == sinaRelationItem:
            self.__dbpool.runInteraction(self.__sinaHandlerInstance.relationDBHandler,item)
#         if item.__class__ == userInfoItem:
#             self.__dbpool.runInteraction(self.__sinaHandlerInstance.sinaUserInfoDBHandler,item)
        if item.__class__ == sinaBlogItem:
            self.__dbpool.runInteraction(self.__sinaHandlerInstance.sinaBlogDBHandler,item)
        if item.__class__ == sinaCommentItem:
            self.__dbpool.runInteraction(self.__sinaHandlerInstance.sinaCommentDBHandler,item)
        if item.__class__ == sinaUserItem:
            self.__dbpool.runInteraction(self.__sinaHandlerInstance.sinaSingleUserInfoDBHandler,item)
        return item

class doubanPipeline(object):
    """豆瓣数据处理
    """
    __doubanHandlerInstance = doubanHandler()
    __dbpool = dbManager('douban').get_dbpool()
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
        if item.__class__ == doubanGroupInfoItem:#豆瓣小组信息
            self.__dbpool.runInteraction(self.__doubanHandlerInstance.groupInfoDBHandler, item)
        return item
        

