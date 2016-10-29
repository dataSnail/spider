# -*- coding:utf-8 -*-
'''
Created on 2016年10月3日

@author: MQ
'''
from twisted.enterprise import adbapi
import MySQLdb.cursors

class dbManager():

    def __init__(self, my_db='sina'):
        self.__dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host = '223.3.94.211',
                                            db = my_db,
                                            user = 'root',
                                            passwd = 'root',
                                            cursorclass = MySQLdb.cursors.DictCursor,
                                            charset = 'utf8',
                                            use_unicode = True)
    def get_dbpool(self):
        return self.__dbpool
