# -*- coding:utf-8 -*-
'''
Created on 2016年12月23日

@author: MQ
'''
import logging
import time
import redis
from seuSpider.utils.dbManager2 import dbManager2
from seuSpider.utils import r2mConfig

class doubanmysql2Redis():
    def __init__(self):
        #数据库连接不上，停止运行程序30min = 1800s
        try:
            self.__db = dbManager2(dbname="douban")
            self.__redisDb = redis.Redis(host=r2mConfig.REDIS_SERVER_IP,port= r2mConfig.REDIS_PORT,db=0,password=r2mConfig.REDIS_PASSWD)
        except Exception as e:
            logging.error('Exception in __init__ e: %s  and sleep at :::%s-----30min'%(str(e),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
            time.sleep(1800)
    
    def comment2Redis(self):
        """豆瓣短评
        """
        for i in xrange(0,4720,25):
            self.__redisDb.rpush('douban_comment','https://m.douban.com/rexxar/api/v2/movie/1866473/interests?count=20&start=%s'%i)
            
    def review2Redis(self):
        """豆瓣影评
        """
        for i in xrange(0,4720,25):
            self.__redisDb.rpush('douban_review','https://m.douban.com/rexxar/api/v2/movie/3541415/reviews?count=25&start=%s&ck=&for_mobile=1'%i)
    
    def relation2Redis(self):
        """豆瓣关注关系 豆瓣粉丝
        """
        selectSql = "select uid from userflag where uid>1304040"
        tupleLs = self.__db.executeSelect(selectSql)
        for t in tupleLs:
#             self.__redisDb.rpush('douban_frelation','https://m.douban.com/rexxar/api/v2/user/%s/following?start=0&count=20&ck=&for_mobile=1'%t[0])#用户关注
            self.__redisDb.rpush('douban_frelation','https://m.douban.com/rexxar/api/v2/user/%s/followers?start=0&count=20&ck=eoxQ&for_mobile=1'%t[0])#用户粉丝
    def reviewComment2Redis(self):
        """影评回应url
        """
        selectSql = "select distinct rid from reviews3541415"
        tupleLs = self.__db.executeSelect(selectSql)
        for t in tupleLs:
            self.__redisDb.rpush('douban_reviewComment','https://m.douban.com/rexxar/api/v2/review/%s/comments?count=25&start=0&ck=&for_mobile=1'%t[0])
            
    def userInfo2Redis(self):
        """用户详细信息url
        """
        selectSql = "select uid from userflag ORDER BY uid ASC"
        tupleLs = self.__db.executeSelect(selectSql)
        for t in tupleLs:
            self.__redisDb.rpush('douban_userInfo','https://m.douban.com/rexxar/api/v2/user/%s?ck=&for_mobile=1'%t[0])
            
    def userGroup2Redis(self):
        """用户加入小组url
        """
        selectSql = "select id from aa  WHERE id >= 14369802 ORDER BY id ASC"
        tupleLs = self.__db.executeSelect(selectSql)
        for t in tupleLs:
            self.__redisDb.rpush('douban_userGroup','https://m.douban.com/rexxar/api/v2/group/user/%s/joined_groups?start=0&count=20&for_mobile=1'%t[0])
#             print 'https://m.douban.com/rexxar/api/v2/group/user/%s/joined_groups?start=0&count=20&for_mobile=1'%t[0]
    def group2Redis(self):
        """用户加入小组url
        """
#         selectSql = "SELECT DISTINCT groupid FROM userGroupRelation where groupid > 235451 ORDER BY groupid ASC"
        selectSql = "SELECT DISTINCT groupid FROM userGroupRelation LEFT JOIN groupInfo on userGroupRelation.groupid = groupInfo.id WHERE groupInfo.id is NULL"
        tupleLs = self.__db.executeSelect(selectSql)
        for t in tupleLs:
            self.__redisDb.rpush('douban_group','https://m.douban.com/rexxar/api/v2/group/%s?ck=&for_mobile=1'%t[0])

    def doubanTJGroup(self):
        selectSql = "select memberNum,count from tj order by memberNum asc"
        tupleLs = self.__db.executeSelect(selectSql)
        result = []
        summ = 126419
        for t in tupleLs:
            result.append([t[0]-1,summ])
            summ = summ - t[1]
        
        for i in result:
            print i
            

if __name__ == '__main__':
    a = doubanmysql2Redis()
    a.group2Redis()
