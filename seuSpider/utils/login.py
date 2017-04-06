#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
Info
- author : "xchaoinfo"
- email  : "xchaoinfo@qq.com"
- date   : "2016.4.8"
3.4 遇到一些问题，于 4.8 号解决。
这里遇到的问题是 跨域请求时候， headers 中的 Host 不断变化的问题，需要针对
不同的访问，选择合适的 Host
3.4 遇到问题，大概是忽略了更换 Host 的问题
'''
import os

import requests
import json
import base64
import time
import math
import random
from PIL import Image
import cookielib
import urllib2
# try:
#     from urllib.parse import quote_plus
# except:
from urllib import quote_plus

'''
3.4
所有的请求都分析的好了
模拟请求 一直不成功
在考虑是哪里出了问题
以后学了新的知识后 再来更新
'''

# 构造 Request headers
global headers
headers = {
    "Host": "passport.weibo.cn",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
}

session = requests.session()
# 访问登录的初始页面
index_url = "https://passport.weibo.cn/signin/login"
# session.get(index_url, headers=headers)


def get_su(username):
    """
    对 email 地址和手机号码 先 javascript 中 encodeURIComponent
    对应 Python 3 中的是 urllib.parse.quote_plus
    然后在 base64 加密后decode
    """
    username_quote = quote_plus(username)
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")


def login_pre(username):
    # 采用构造参数的方式
    params = {
        "checkpin": "1",
        "entry": "mweibo",
        "su": get_su(username),
        "callback": "jsonpcallback" + str(int(time.time() * 1000) + math.floor(random.random() * 100000))
    }
    '''真是日了狗，下面的这个写成 session.get(login_pre_url，headers=headers) 404 错误
        这条 3.4 号的注释信息，一定是忽略了 host 的变化，真是逗比。
    '''
    pre_url = "https://login.sina.com.cn/sso/prelogin.php"
    headers["Host"] = "login.sina.com.cn"
    headers["Referer"] = index_url
    pre = session.get(pre_url, params=params, headers=headers)

    # pa = r'\((.*?)\)'
    # res = re.findall(pa, pre.text)
    # if res == []:
    if pre.text == None:
        print("好像哪里不对了哦，请检查下你的网络，或者你的账号输入是否正常")
    else:
        js = json.loads(pre.text)
        if js["showpin"] == 1:
            headers["Host"] = "passport.weibo.cn"
            capt = session.get("https://passport.weibo.cn/captcha/image", headers=headers)
            capt_json = capt.json()
            capt_base64 = capt_json['data']['image'].split("base64,")[1]
            with open('capt.jpg', 'wb') as f:
                f.write(base64.b64decode(capt_base64))
                f.close()
            im = Image.open("capt.jpg")
            im.show()
            im.close()
            cha_code = input("请输入验证码\n>")
            return cha_code, capt_json['data']['pcid']
        else:
            return ""


def login(username, password, pincode, cnt):
    postdata = {
        "username": username,
        "password": password,
        "savestate": "1",
        "ec": "0",
        "pagerefer": "",
        "entry": "mweibo",
        "wentry": "",
        "loginfrom": "",
        "client_id": "",
        "code": "",
        "qq": "",
        "hff": "",
        "hfp": "",
    }
    if pincode == "":
        pass
    else:
        # postdata["pincode"] = pincode[0]
        # postdata["pcid"] = pincode[1]
        postdata["vid"] = pincode[1]
    headers["Host"] = "passport.weibo.cn"
    headers["Reference"] = index_url
    headers["Origin"] = "https://passport.weibo.cn"
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    post_url = "https://passport.weibo.cn/sso/login"
    login = session.post(post_url, data=postdata, headers=headers)
    # print(login.cookies)
    # print(login.status_code)
    js = login.json()
    # print(js)
    uid = js["data"]["uid"]
    crossdomain = js["data"]["crossdomainlist"]
    cn = "https:" + crossdomain["sina.com.cn"]
    # 下面两个对应不同的登录 weibo.com 还是 m.weibo.cn
    # 一定要注意更改 Host
    # mcn = "https:" + crossdomain["weibo.cn"]
    # com = "https:" + crossdomain['weibo.com']
    headers["Host"] = "login.sina.com.cn"
    session.get(cn, headers=headers)
    headers["Host"] = "m.weibo.cn"
    # ht = session.get("http://weibo.cn/%s/info" % uid, headers=headers)
    ht = session.get('http://m.weibo.cn/single/rcList?format=cards&id=3914102592235131&type=comment&page=1', headers=headers)
    print ht
    # print os.path.abspath(os.pardir) + '\cookie.txt'
    cookie_jar = cookielib.MozillaCookieJar(os.path.abspath(os.pardir)+'/data/cookie' + str(cnt) + '.txt')
    requests.utils.cookiejar_from_dict({c.name: c.value for c in session.cookies}, cookie_jar)
    cookie_jar.save(ignore_discard=True, ignore_expires=True)

    # pa = r'<title>(.*?)</title>'
    # res = re.findall(pa, ht.text)
    # print("你好%s，你正在使用 xchaoinfo 写的模拟登录" % res[0])
    # print(cn, com, mcn)


if __name__ == "__main__":
    index = 3
    username_password = {}
    username_password["15601588775"] = "19930331NORTH"
    username_password["txhqqpp@126.com"] = "!QAZ2wsx"
    username_password["qmeng2014@gmail.com"] = "qmeng@123"
    username_password["15501681628"] = "19930331:weibo"
    username_password["17019952460"] = "you456789"

    pincode = login_pre(username_password.keys()[index])
    print pincode
    login(username_password.keys()[index], username_password.values()[index], pincode, index)
