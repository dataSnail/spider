# -*- coding:utf-8 -*-  
'''
Created on 2016年10月3日

@author: MQ
'''
import MySQLdb
import logging

class dbManager2():
    def __init__(self,host='223.3.94.145',user='root',passwd='root@123',port=3306,charset='utf8'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.charset = charset
        self.conn = None
        self.cur = None
    
    def get_cur(self,dbname):
        try:
            self.conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,port=self.port,charset=self.charset)
            self.cur = self.conn.cursor()
            self.conn.select_db(dbname)
        except Exception as e:
            logging.error(e)
        return self.cur
    
    
    
    def release(self):
        if self.cur != None:
            self.cur.close()
        if self.conn != None:
            self.conn.close()
    
    def commit(self):
        if self.conn != None:
            self.conn.commit()
            
            
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
    pre_user_list = []
    result_list=[]
    db =dbManager2()
    cur = db.get_cur('sina')
    sql = 'SELECT uid from scra_flags_0 where wblog_flag = 0 ORDER BY id ASC LIMIT 0,100'
    count = cur.execute(sql)
    if count>0:
        pre_user_list = cur.fetchall()
        for i in pre_user_list:
            result_list.append(i[0])
    else:
#         sys.exit()
        print 'end=======================================>'
    db.release()
    print result_list
    
    