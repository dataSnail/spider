# -*- coding:utf-8 -*-  
'''
Created on 2016年10月3日

@author: MQ
'''
import scrapy.cmdline

if __name__ == '__main__':
#     scrapy.cmdline.execute(argv=['scrapy', 'crawl','user_relation'])
#     scrapy.cmdline.execute(argv=['scrapy', 'crawl','sina_comment'])
    scrapy.cmdline.execute(argv=['scrapy', 'crawl','sina_status'])