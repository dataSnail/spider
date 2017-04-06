# -*- coding:utf-8 -*-
'''
Created on 2016年10月5日

@author: MQ
'''
import sys
sys.path.append('../')
import random
import logging
import base64
import os
import redis
from scrapy.exceptions import IgnoreRequest
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import json
from seuSpider.cookie import initCookie, updateCookie, removeCookie
from scrapy.utils.response import response_status_message
from seuSpider.ipproxy.agents import AGENTS
from time import sleep

class UserAgentMiddleware(object):
    def process_request(self,request,spider):
#         logging.info('using UserAgentMiddleware-----------------------------------------------UserAgentMiddleware')
        agent = random.choice(AGENTS)
        if agent:
            request.headers['User-Agent'] = agent

class aBuProxyMiddleware(object):
    proxyServer = "http://proxy.abuyun.com:9010"
    proxyUser = "H5S031HK5GAI638P"
    proxyPass = "0451B74483012582"
    proxyAuth = "Basic " + base64.encodestring(proxyUser + ":" + proxyPass)
    last_url = 'NULL'
#     print proxyAuth
    def process_request(self,request,spider):
#         print request
        #修复重定向bug
        if not request.url.startswith('http://m.weibo.cn'):
            logging.warn('request.url is::::'+request.url+' and the last_url is ::::'+self.last_url)
            request.headers["Proxy-Switch-Ip"] = "yes"
            request._set_url(self.last_url)
            logging.warn('request.url is changed to :=====>'+request.url)
        else:
            self.last_url = request.url
        logging.info('using aBuProxyMiddleware-----------------------------------------------aBuProxyMiddleware')
        request.meta['proxy'] = self.proxyServer
        request.headers["Proxy-Authorization"] = self.proxyAuth

    def process_response(self,request,response,spider):
        #切换ip
        logging.info('url : '+str(request.url)+' ,status:'+str(response.status))
        if response.status != 200:
            #返回错误状态，统一修复request.url,重新进行请求
            request._set_url(self.last_url)
            #代理429错误，请求数量超过限制
            if response.status == 429:
                sleep(5)
                logging.warn('too many request sleep for 5 seconds-------------------------------------------------->429')
            if response.status == 402:
                sleep(60)
                logging.warn('up to date !!-------------------------------------------------->402')
            if response.status == 403 or response.status == 503:
                #重新切换ip
                request.headers["Proxy-Switch-Ip"] = "yes"

            request.meta['proxy'] = self.proxyServer
            request.headers["Proxy-Authorization"] = self.proxyAuth
            #切换代理，重新请求，设置不过滤上一次请求的url
            request.dont_filter = True
            return request
        if not response.url.startswith('http://m.weibo.cn'):
#             self.change_ipproxy()
            request._set_url(self.last_url)
            request.meta['proxy'] = self.proxyServer
            request.headers["Proxy-Authorization"] = self.proxyAuth
            request.headers["Proxy-Switch-Ip"] = "yes"
            request.dont_filter = True
            return request
        return response

    def process_exception(self,request,exception,spider):
        logging.info('process_exception in aBuProxyMiddleware changing proxy---------------------------------------<<<exception is ::::'+str(exception))
        request._set_url(self.last_url)
        #修复url，换ip
        request.headers["Proxy-Switch-Ip"] = "yes"
        request.meta['proxy'] = self.proxyServer
        request.headers["Proxy-Authorization"] = self.proxyAuth
        return request

class CookiesMiddleware(RetryMiddleware):
    """ 维护Cookie """

    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)
#         self.rconn = settings.get("RCONN", redis.Redis(crawler.settings.get('REDIS_HOST', 'localhsot'), crawler.settings.get('REDIS_PORT', 6379)))
        self.rconn = settings.get("RCONN", redis.Redis(password = "redis123",host = "223.3.94.145", port = 6379))
        initCookie(self.rconn, crawler.spider.name)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def process_request(self, request, spider):
        redisKeys = self.rconn.keys()
        while len(redisKeys) > 0:
            elem = random.choice(redisKeys)
            if "SinaSpider:Cookies" in elem:
                cookie = json.loads(self.rconn.get(elem))
                request.cookies = cookie
                request.meta["accountText"] = elem.split("Cookies:")[-1]
                break
            else:
                redisKeys.remove(elem)

    def process_response(self, request, response, spider):
        if response.status in [300, 301, 302, 303]:
            try:
                redirect_url = response.headers["location"]
                if "login.weibo" in redirect_url or "login.sina" in redirect_url:  # Cookie失效
                    logging.warning("One Cookie need to be updating...")
                    updateCookie(request.meta['accountText'], self.rconn, spider.name)
                elif "weibo.cn/security" in redirect_url:  # 账号被限
                    logging.warning("One Account is locked! Remove it!")
                    removeCookie(request.meta["accountText"], self.rconn, spider.name)
                elif "weibo.cn/pub" in redirect_url:
                    logging.warning(
                        "Redirect to 'http://weibo.cn/pub'!( Account:%s )" % request.meta["accountText"].split("--")[0])
                reason = response_status_message(response.status)
                return self._retry(request, reason, spider) or response  # 重试
            except Exception, e:
                raise IgnoreRequest
        elif response.status in [403, 414]:
            logging.error("%s! Stopping..." % response.status)
            os.system("pause")
        else:
            return response
class noProxyMiddleware(object):
    def process_request(self,request,spider):
        #修复重定向bug
        if not request.url.startswith('https://m.douban.com'):
            logging.warn('request.url is::::'+request.url+' and the last_url is ::::'+self.last_url)
            request._set_url(self.last_url)
            logging.warn('request.url is changed to :=====>'+request.url)
        else:
            self.last_url = request.url
#         logging.info('using noProxyMiddleware-----------------------------------------------noProxyMiddleware')

    def process_response(self,request,response,spider):
        #切换ip
        logging.info('url : '+str(request.url)+' ,status:'+str(response.status))
        if response.status != 200:
            #返回错误状态，统一修复request.url,重新进行请求
            request._set_url(self.last_url)
            request.dont_filter = True
            return request
        if not response.url.startswith('https://m.douban.com'):
#             self.change_ipproxy()
            request._set_url(self.last_url)
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
