# -*- coding: utf-8 -*-
from seuSpider.utils.dbManager import dbManager
from seuSpider.spiderHandlers.sinaHandler import sinaHandler
from seuSpider.items.sinaItems import userInfoItem,userRelationItem,mblogItem,commentItem
from seuSpider.spiderHandlers.doubanHandler import doubanHandler
from seuSpider.items.doubanItems import shortCommentItem, reviewItem

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
        if item.__class__ == mblogItem:
            self.__dbpool.runInteraction(self.__sinaHandlerInstance.sinaMblogDBHandler,item)
        if item.__class__ == commentItem:
            self.__dbpool.runInteraction(self.__sinaHandlerInstance.sinaCommentDBHandler,item)
        return item

class doubanPipeline(object):
    __doubanHandlerInstance = doubanHandler()
    __dbpool = dbManager().get_dbpool()
    def __init__(self):
        pass
        
    def process_item(self, item, spider):
        if item.__class__ == shortCommentItem:
            self.__dbpool.runInteraction(self.__doubanHandlerInstance.commentDBHandler,item)
        if item.__class__ == reviewItem:
            self.__dbpool.runInteraction(self.__doubanHandlerInstance.reviewDBHandler,item)
        return item

