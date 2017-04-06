# -*- coding:utf-8 -*-  
'''
Created on 2017年3月5日

@author: MQ
'''

from seuSpider.utils.dbManager2 import dbManager2

class stastic():
    def __init__(self):
        #数据库连接不上，停止运行程序30min = 1800s
        self.__db = dbManager2(dbname="douban")

    def group_count_count(self):
        selectSql = "SELECT count(DISTINCT uid) FROM userGroupRelation WHERE groupid in (SELECT groupid FROM (SELECT count(0) as num,groupid FROM userGroupRelation GROUP BY groupid) a WHERE num > %s)"
        selectCount = "select distinct num from (select count(0) as num from userGroupRelation group by groupid) a ORDER BY num ASC"
        countTuples = self.__db.executeSelect(selectCount)
        with open('C:\\noInfomationUrls.txt','a') as filee:
            for t in countTuples:
                executeSql = selectSql%t[0]
                personCount = self.__db.executeSelect(executeSql)[0][0]
                print [t[0],personCount]
                filee.write(str(t[0])+str(personCount)+'\n')

    def group_count_time(self):
        selectSql = "SELECT DATE_FORMAT(create_time,'%%Y-%%m-%%d') dayTime,count(0) num FROM (SELECT * FROM comments3541415 WHERE cuid in (SELECT uid FROM userGroupRelation WHERE groupid = %s)) a GROUP BY dayTime ORDER BY dayTime asc"
        selectCount = "SELECT groupid FROM userGroupRelation GROUP BY groupid ORDER BY count(0) DESC LIMIT 100"
        countTuples = self.__db.executeSelect(selectCount)
        a=0
#         for t in countTuples:
# #             print selectSql%t[0]
#             a=a+1
#             executeSql = selectSql%t[0]
#             personCount = self.__db.executeSelect(executeSql)
#             with open('C:\\groups\\group_'+str(a)+'.txt','a') as filee:
#                 for i in personCount:
#                     filee.write(str(i[0])+','+str(i[1])+'\n')
        executeSql = selectSql%133541           
        personCount = self.__db.executeSelect(executeSql)
        with open('C:\\groups\\group_'+str(a)+'.txt','a') as filee:
            for i in personCount:
                filee.write(str(i[0])+','+str(i[1])+'\n')           
                    
    def delRelation(self):
        selectSql = "DELETE FROM relations_copy WHERE fid > %s AND fid < %s"
        selectCount = "SELECT DISTINCT id FROM userInfo_3541415 ORDER BY id ASC"
        countTuples = self.__db.executeSelect(selectCount)
        last_id = 0
        for t in countTuples:
            executeSql = selectSql%(last_id,t[0])
            last_id = t[0]
            self.__db.execute(executeSql)                
                
if __name__ == '__main__':
    a = stastic()
    a.delRelation()