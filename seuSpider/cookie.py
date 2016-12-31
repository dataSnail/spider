# -*- coding:utf-8 -*-  
'''
Created on 2016年12月9日
https://github.com/LiuXingMing/SinaSpider/blob/master/Sina_spider3/Sina_spider3/cookies.py
@author: MQ
'''
import base64
import os
import requests
import json
import logging

logger = logging.getLogger(__name__)

#微博账号列表
weiboId = [
           ('209923908@qq.com','mq123456')
           ]
def getCookie(account,password):
    loginURL = 'https://accounts.douban.com/login'
#     username = base64.b64encode(account.encode("utf-8")).decode("utf-8")
    postData = {
                "source": "None",
                'redir':'https://www.douban.com/',
                'form_email':'209923908@qq.com',
                'form_password':'mq123456',
                'login':'登录'
                }
    session = requests.Session()
    r = session.post(loginURL, data=postData,verify=False)
#     jsonStr = r.content.decode('gbk')
    cookie = session.cookies.get_dict()
    return json.dumps(cookie)
def initCookie(rconn, spiderName):
    """ 获取所有账号的Cookies，存入Redis。如果Redis已有该账号的Cookie，则不再获取。 """
    for weibo in weiboId:
        if rconn.get("%s:Cookies:%s--%s" % (spiderName, weibo[0], weibo[1])) is None:  # 'SinaSpider:Cookies:账号--密码'，为None即不存在。
            cookie = getCookie(weibo[0], weibo[1])
            if len(cookie) > 0:
                rconn.set("%s:Cookies:%s--%s" % (spiderName, weibo[0], weibo[1]), cookie)
#     cookie = getCookie(weiboId[0][0], weiboId[0][1])
#     print cookie
    cookieNum = "".join(rconn.keys()).count("douban_relations:Cookies")
    logger.warning("The num of the cookies is %s" % cookieNum)
    if cookieNum == 0:
        logger.warning('Stopping...')
        os.system("pause")


def updateCookie(accountText, rconn, spiderName):
    """ 更新一个账号的Cookie """
    account = accountText.split("--")[0]
    password = accountText.split("--")[1]
    cookie = getCookie(account, password)
    if len(cookie) > 0:
        logger.warning("The cookie of %s has been updated successfully!" % account)
        rconn.set("%s:Cookies:%s" % (spiderName, accountText), cookie)
    else:
        logger.warning("The cookie of %s updated failed! Remove it!" % accountText)
        removeCookie(accountText, rconn, spiderName)


def removeCookie(accountText, rconn, spiderName):
    """ 删除某个账号的Cookie """
    rconn.delete("%s:Cookies:%s" % (spiderName, accountText))
    cookieNum = "".join(rconn.keys()).count("SinaSpider:Cookies")
    logger.warning("The num of the cookies left is %s" % cookieNum)
    if cookieNum == 0:
        logger.warning('Stopping...')
        os.system("pause")
    
if __name__ == "__main__":
    pass
    