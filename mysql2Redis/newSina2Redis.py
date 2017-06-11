# -*- coding:utf-8 -*-
'''
Created on 2016年10月1日

@author: MQ
'''
import sys
sys.path.append('../')

from seuSpider.utils.dbManager2 import dbManager2
from seuSpider.utils import r2mConfig
import time
import redis
import logging



class mysql2Redis():

    __mark403 = False
    def __init__(self):
        self.__proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
              "host" : r2mConfig.ABU_PROXY_HOST,
              "port" : r2mConfig.ABU_PROXY_PORT,
              "user" : r2mConfig.ABU_PROXY_USER,
              "pass" : r2mConfig.ABU_PROXY_PWD,
            }
        #选择使用代理
        self.__enable_proxy = False
#         self.__url = 'http://m.weibo.cn/page/json?containerid=100505%s_-_FOLLOWERS&page=%s'
        self.__url = 'http://m.weibo.cn/container/getSecond?containerid=100505%s_-_FOLLOWERS&page=%s'#2017.1.20 new url
        #数据库连接不上，停止运行程序30min = 1800s
        try:
            self.__db = dbManager2(dbname="tim",host="223.3.94.145")
            self.__redisDb = redis.Redis(host=r2mConfig.REDIS_SERVER_IP,port= r2mConfig.REDIS_PORT,db=0,password=r2mConfig.REDIS_PASSWD)
        except Exception as e:
            logging.error('Exception in __init__ :::::%s  and sleep at :::%s-----1800s'%(str(e),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
            time.sleep(1800)

    def getUserListFromMysql(self):
        try:
            u_url  = "http://m.weibo.cn/container/getSecond?containerid=100505%s_-_FOLLOWERS&page=1"
            sql = 'SELECT fid from sinaFrelation GROUP BY fid HAVING fid NOT IN (SELECT DISTINCT uid FROM sinaFrelation) LIMIT 0,10'
            uidLs = self.__db.executeSelect(sql)
            for uid in uidLs:
                self.__redisDb.rpush('sina_relation',u_url%str(uid[0]))
#                 print u_url%str(uid[0])
        except Exception as e:
            logging.error('Exception in function::: getUserListFromMysql -------------------->%s'%str(e))
    def gettttt(self):
        try:
            u_url  = "http://m.weibo.cn/container/getIndex?containerid=230283%s_-_INFO"
            sql = 'SELECT uid from users_have_all_relations order by uid asc'
            
            sql2 = 'SELECT uid from ('\
'SELECT users_have_all_relations.id,users_have_all_relations.uid,userinfo.id as id1 from users_have_all_relations LEFT JOIN userinfo ON users_have_all_relations.uid = userinfo.uid'\
') a WHERE  id1 is NULL order by uid asc'
            
            uidLs = self.__db.executeSelect(sql2)
            for uid in uidLs:
                self.__redisDb.rpush('sinaUser',u_url%str(uid[0]))
#                 print u_url%str(uid[0])
        except Exception as e:
            logging.error('Exception in function::: getUserListFromMysql -------------------->%s'%str(e))

if __name__ == '__main__':
#     print '------running------'
        a = mysql2Redis()
        a.gettttt()
#         while 1:
#             a.getUserListFromMysql()
#             time.sleep(5)

