# -*- coding:utf-8 -*-
'''
Created on 2016年10月3日

@author: MQ
'''
from twisted.enterprise import adbapi
import MySQLdb.cursors

class dbManager():

    def __init__(self, my_db='douban'):
        self.__dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host = '223.3.75.216',
                                            db = my_db,
                                            user = 'root',
                                            passwd = 'root@123',
                                            cp_min = 10,
                                            cp_max = 100,
                                            cursorclass = MySQLdb.cursors.DictCursor,
                                            charset = 'utf8',
                                            use_unicode = True)
    def get_dbpool(self):
        return self.__dbpool

if __name__ == '__main__':
    import time
    d = dbManager()
    d.get_dbpool()
    while 1:
        pass
        time.sleep(1)
        print '1'
    