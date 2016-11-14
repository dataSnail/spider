# -*- coding:utf-8 -*-
'''
Created on 2016年10月3日

@author: MQ
'''
from twisted.enterprise import adbapi
import MySQLdb.cursors

class dbManager():

    def __init__(self, my_host='223.3.75.180', my_db='sina'):
        self.__dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host = my_host,
                                            db = my_db,
                                            user = 'root',
                                            passwd = 'root@123',
                                            cursorclass = MySQLdb.cursors.DictCursor,
                                            charset = 'utf8',
                                            use_unicode = True)
    def get_dbpool(self):
        return self.__dbpool
