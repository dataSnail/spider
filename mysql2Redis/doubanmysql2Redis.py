# -*- coding:utf-8 -*-
'''
Created on 2016年12月23日

@author: MQ
'''
class doubanmysql2Redis():
    def comment2Redis(self):
        for i in xrange(0,4720,25):
            self.__redisDb.rpush('douban_frelation','https://m.douban.com/rexxar/api/v2/movie/3541415/interests?count=20&start=%s'%i)
            
    def review2Redis(self):
        for i in xrange(0,4720,25):
            self.__redisDb.rpush('douban_reviews','https://m.douban.com/rexxar/api/v2/movie/3541415/reviews?count=25&start=%s&ck=&for_mobile=1'%i)
   
if __name__ == '__main__':
    a = doubanmysql2Redis()
    a.comment2Redis()
