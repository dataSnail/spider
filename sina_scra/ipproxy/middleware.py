# -*- coding:utf-8 -*-
'''
Created on 2016年10月5日

@author: MQ
'''
from sina_scra.ipproxy.agents import AGENTS
import random
import logging
import base64
from time import sleep

class UserAgentMiddleware(object):
    def process_request(self,request,spider):
        logging.info('using UserAgentMiddleware-----------------------------------------------UserAgentMiddleware')
        agent = random.choice(AGENTS)
        if agent:
            request.headers['User-Agent'] = agent


# class ProxyMiddleware(object):
#     ip = '127.0.0.1'
#     port = '1080'
#     protocol = 'HTTP'
#     proxy_addr = "http://%s:%s"%(ip,port)
#     ip_status = -1
# #     last_url = ''
#     conn = dbManager2()
#     cur = conn.get_cur('sinaData')
#     def process_request(self,request,spider):
# #         print request
#         logging.info('using ProxyMiddleware-----------------------------------------------ProxyMiddleware')
#         request.meta['proxy'] = self.proxy_addr
#
#
#     def process_response(self,request,response,spider):
#         #切换ip
#         logging.info('url : '+str(request.url)+' ,status:'+str(response.status))
#         if response.status != 200:
# #             self.last_url = request.url
#             self.change_ipproxy()
#             request.meta['proxy'] = self.proxy_addr
#             #切换代理，重新请求，设置不过滤上一次请求的url
#             request.dont_filter = True
#             return request
# #         if not response.url.startswith('http://m.weibo.cn'):
# #             self.change_ipproxy()
# #             request.replace(url=self.last_url)
# #             request.meta['proxy'] = self.proxy_addr
# #             request.dont_filter = True
# #             return request
#         return response
#
#     def select_ipproxy(self):
#         ip_list = []
#         #更新ip标记
#         sql = 'update ipproxy set status = status+1 where ip = \'%s\' and port = \'%s\'' %(self.ip,self.port)
#         self.cur.execute(sql)
#         self.conn.commit()
#         #选取状态标记最小的一个
#         count = self.cur.execute('select ip,port,protocol from ipproxy order by status asc limit 1')
#         if count > 0:
#             ip_list = self.cur.fetchall()
#         else:
#             print 'no ip can be used in db'
#         return ip_list
#     def process_exception(self,request,exception,spider):
#         logging.info('process_exception ......................')
# #         self.last_url = request.url
#         #切换ip
#         self.change_ipproxy()
#         request.meta['proxy'] = self.proxy_addr
#         return request
#
#     def change_ipproxy(self):
#         proxy_list = self.select_ipproxy()
# #         print proxy_list
#         if len(proxy_list)==1 and len(proxy_list[0])==3:
#             self.ip = str(proxy_list[0][0])
#             self.port = str(proxy_list[0][1])
#             if len(proxy_list[0][2].split('/'))>1:
#                 self.protocol = proxy_list[0][2].split('/')[0]
#             else:
#                 self.protocol = proxy_list[0][2]
#             self.proxy_addr = self.protocol+'://%s:%s'%(self.ip,self.port)
#             logging.info('proxy_addr is : '+self.proxy_addr)
#         else:
#             print 'can not change_ipproxy'

class aBuProxyMiddleware(object):
    proxyServer = "http://proxy.abuyun.com:9010"
    proxyUser = "H5S031HK5GAI638P"
    proxyPass = "0451B74483012582"
    proxyAuth = "Basic " + base64.encodestring(proxyUser + ":" + proxyPass)
#     print proxyAuth
    def process_request(self,request,spider):
#         print request
        self.last_url = request.url
        logging.info('using aBuProxyMiddleware-----------------------------------------------aBuProxyMiddleware')
        request.meta['proxy'] = self.proxyServer
        request.headers["Proxy-Authorization"] = self.proxyAuth
        request.cookie = COOKIE

    def process_response(self,request,response,spider):
        #切换ip
        logging.info('url : '+str(request.url)+' ,status:'+str(response.status))
        if response.status != 200:
#             self.last_url = request.url
            #代理429错误，请求数量超过限制
            if response.status == 429:
                sleep(5)
                logging.warn('too many request sleep for 5 seconds-------------------------------------------------->429')
            if response.status == 402:
                sleep(60)
                logging.warn('up to date !!-------------------------------------------------->402')
            #等待
            request.meta['proxy'] = self.proxyServer
            request.headers["Proxy-Authorization"] = self.proxyAuth
            #切换代理，重新请求，设置不过滤上一次请求的url
            request.dont_filter = True
            return request
        if not response.url.startswith('http://m.weibo.cn'):
#             self.change_ipproxy()
            request.replace(url=self.last_url)
            request.meta['proxy'] = self.proxyServer
            request.headers["Proxy-Authorization"] = self.proxyAuth
            request.dont_filter = True
            return request
        return response

    def process_exception(self,request,exception,spider):
        logging.info('process_exception in aBuProxyMiddleware changin proxy---------------------------------------<<<')
#         self.last_url = request.url
        #等待
        request.meta['proxy'] = self.proxyServer
        request.headers["Proxy-Authorization"] = self.proxyAuth
        return request

import os
import cookielib
import requests


class MyCookieMiddleware(object):

    def __init__(self):
        self.load_cookie()
        self.cnt = 0

    def load_cookie(self):
        load_cookiejar = cookielib.MozillaCookieJar()
        load_cookiejar.load(os.path.abspath(os.pardir) + '/ipproxy/cookie.txt', ignore_discard=True, ignore_expires=True)
        self.load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)

    def process_request(self,request,spider):
        logging.info('using MyCookieMiddleware-----------------------------------------------MyCookieMiddleware')
        request.cookie = self.load_cookies
        self.last_url = request.url

    def process_response(self,request,response,spider):
        if response.status == 404:
            if 'passport' in response.url:
                execfile(os.path.abspath(os.pardir) + '/utils/login.py')
                self.load_cookie
                request.replace(url=self.last_url)
                request.dont_filter = True
                return request
            # print 'here'
            # print response.url
            # self.cnt += 1
            # if self.cnt == 20:
            #     self.cnt = 0
            #     logging.warn('in MyCookieMiddleware url : '+str(request.url)+' ,status:'+str(response.status))
            #     sleep(5)
            #     execfile(os.path.abspath(os.pardir) + '/utils/login.py')
            #     self.load_cookie
            #     request.dont_filter = True
            #     return request
        return response

class noProxyMiddleware(object):
    def process_request(self,request,spider):
        self.last_url = request.url
        logging.info('using noProxyMiddleware-----------------------------------------------noProxyMiddleware')

    def process_response(self,request,response,spider):
        logging.info('url : '+str(request.url)+' ,status:'+str(response.status))
        if response.status != 200:
            request.dont_filter = True
            return request
        if not response.url.startswith('http://m.weibo.cn'):
#             self.change_ipproxy()
            request.replace(url=self.last_url)
            request.meta['proxy'] = self.proxyServer
            request.headers["Proxy-Authorization"] = self.proxyAuth
            request.dont_filter = True
            return request
        return response

    def process_exception(self,request,exception,spider):
        logging.info('process_exception in noProxyMiddleware changin proxy---------------------------------------<<<')
        return request

# if __name__ == '__main__':
#     a = ProxyMiddleware()
#     a.change_ipproxy()
#     print a.ip
#     print a.port
#     print a.protocol
