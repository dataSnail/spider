# -*- coding:utf-8 -*-  
'''
Created on 2016年10月3日

@author: MQ
'''
import MySQLdb

class dbManager2():
    def __init__(self,dbname,host='223.3.75.180',user='root',passwd='root@123',port=3306,charset='utf8'):
        self.__host = host
        self.__user = user
        self.__passwd = passwd
        self.__port = port
        self.__charset = charset
        self.__conn=MySQLdb.connect(host=self.__host,user=self.__user,passwd=self.__passwd,port=self.__port,charset=self.__charset)
        self.__conn.select_db(dbname)
        self.__cur = self.__conn.cursor()
    
    def executeSelect(self,sql):
        self.__cur.execute(sql)
        resultLs = self.__cur.fetchall()
        return resultLs
    
    def execute(self,sql):
        self.__cur.execute(sql)
        self.__conn.commit()

    def executemany(self,sql,values):
        self.__cur.executemany(sql,values)
        self.__conn.commit()

    def release(self):
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.conn.close()
            
            
if __name__ == '__main__':
#     db = dbManager2()
#     cur =dbManager2().get_cur('sina')
#     sum1 = 0
#     for i in range(1000):
#         sql = 'select count(0) from frelation_%s'%i
#         cur.execute(sql)
#         count = cur.fetchall()
#         print i,count[0][0]
#         sum1+=count[0][0]
#     print sum1
#     cur = dbManager2().get_cur('sina')
#     cur.execute('select uid,currentPage,maxPage from uid_weibo where id = 1')
#     uidData = cur.fetchall()
#     current_uid = uidData[0][0]
#     current_page = uidData[0][1]
#     current_max_page = uidData[0][2]
#     print current_uid,current_page,current_max_page
#     pre_user_list = []
#     result_list=[]
#     db =dbManager2()
#     cur = db.get_cur('sina')
#     sql = 'SELECT uid from scra_flags_0 where wblog_flag = 0 ORDER BY id ASC LIMIT 0,100'
#     count = cur.execute(sql)
#     if count>0:
#         pre_user_list = cur.fetchall()
#         for i in pre_user_list:
#             result_list.append(i[0])
#     else:
# #         sys.exit()
#         print 'end=======================================>'
#     db.release()
#     print result_list
#     a = []
#     import time
#     while 1:
#         db = dbManager2(dbname="douban")
#         print db.executeSelect('select * from comments3541415')
#         time.sleep(1)

    db = dbManager2(dbname="sina")
    print db.executeSelect("select 1 ")