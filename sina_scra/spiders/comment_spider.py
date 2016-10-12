# -*- coding: utf-8 -*-

# 爬取新浪用户的所有微博，顺便记录下用户信息

from scrapy import Request
from scrapy.spiders import Spider

from sina_scra.items import SinaCommentItem
from sina_scra.items import SinaAllJsonItem
from sina_scra.items import SinaFlagItem

import json
import time
import MySQLdb
import MySQLdb.cursors
import logging


class CommentSpider(Spider):
    name = "sina_comment"  # 爬虫名称
    allowed_domain = [""]  # 访问的url的域名
    start_urls = []  # 初始url
    total_mids = []  # 与初始url相对应的mid
    total_uids = []  # 与mid相对应的uid
    url_part_one = 'http://m.weibo.cn/single/rcList?format=cards&id='
    url_part_two = '&type=comment&hot=0&page='

    cookie_T_WM = "59aa264b56d5e3b3d985798e4d90f47a"
    cookie_H5_INDEX = '3'
    cookie_H5_INDEX_TITLE='rubinorth'
    cookie_ALF='1478170106'
    cookie_SCF='AhXRhNsz5jQCJyxi-OaDnhdm6oCrmRx_04kdMaUtyV6L7AmImJtgNqVjFx5QQA5_8qVUchoJol6a4D8Rnb1slBA.'
    cookie_SUB = "_2A2569_7nDeTxGeNO4lMU-CnOzDmIHXVWG4KvrDV6PUJbktBeLWz6kW0cPXf0jtrXd3-Q0gTOr2-EqtFU1Q.."
    cookie_SUBP = "0033WrSXqPxfM725Ws9jqgMF55529P9D9WWqGKPmkK7YwfuIK6ON7U5k5JpX5o2p5NHD95Qfeh.pSKnNeoMfWs4DqcjiMrHbIg4aMrxQ"
    cookie_SUHB = "0pHxZc08gWqenE"
    cookie_SSOLoginState = "1475579575"

    # 对start_urls进行初始化
    def __init__(self):
        conn = MySQLdb.connect(host='223.3.94.145', db='sina', user='root', passwd='root@123', charset='utf8')
        cursor = conn.cursor()
        my_sql = 'SELECT uid, mid FROM wblog_520 WHERE comment_flag = 0'
        try:
            cursor.execute(my_sql)
            for result in cursor.fetchall():
                uid = result[0]
                self.total_uids.append(uid)
                mid = result[1]
                self.total_mids.append(mid)
        except MySQLdb.Error, e:
            print "CommentSpider MySQL Error:%s" % str(e)
        cursor.close()
        conn.close()

        self.start_urls.append(self.url_part_one + str(self.total_mids[0]) + self.url_part_two + '1')
        # self.start_urls = [self.url_part_one + '1731502203' + self.url_part_two + '2']

        self.cookie = {"_T_WM": self.cookie_T_WM,
                       "H5_INDEX": self.cookie_H5_INDEX,
                       "H5_INDEX_TITLE": self.cookie_H5_INDEX_TITLE,
                       "ALF": self.cookie_ALF,
                       "SCF": self.cookie_SCF,
                       "SUB": self.cookie_SUB,
                       "SUBP": self.cookie_SUBP,
                       "SUHB": self.cookie_SUHB,
                       "SSOLoginState": self.cookie_SSOLoginState}

        print len(self.total_mids)

    # 根据start_urls生成最初的url请求
    def start_requests(self):
        return [Request(url, cookies=self.cookie, meta={'maxPage': -1, 'nowPage': 1, 'mIndex': 0}, callback=self.parse_page) for url in
                self.start_urls]

    # 处理爬取到的页面
    def parse_page(self, response):
        logging.info("parse : " + response.url)

        render_data = json.loads(response.body)

        if response.meta['maxPage'] == -1:
            # 第一次进来时需要设置maxPage
            # mod/empty表示没有内容
            render_data = render_data[1]
            if render_data['mod_type'] == 'mod/empty':
                maxPage = -1
            elif 'maxPage' in render_data.keys():
                maxPage = render_data['maxPage']
            else:
                maxPage = -1
        else:
            render_data = render_data[0]
            maxPage = response.meta['maxPage']

        # mod/pagelist表示当前页有评论内容
        if render_data['mod_type'] == 'mod/pagelist':
            item = SinaCommentItem()  # 微博评论
            self.init_item(item)

            # jItem = SinaAllJsonItem()  # 评论所有json内容
            # jItem['mid'] = []
            # jItem['allJson'] = []

            for comment in render_data['card_group']:
                self.fill_item(item, comment, self.total_mids[response.meta['mIndex']])
                # jItem['mid'].append(self.total_mids[response.meta['mIndex']])
                # jItem['allJson'].append(comment)

            yield item
            # yield jItem

        # 生成新的request
        nowPage = response.meta['nowPage']
        mIndex = response.meta['mIndex']
        if nowPage >= maxPage:
            # nowPage >= maxPage的话说明这条微博的评论已经爬完了
            fItem = SinaFlagItem()
            fItem['uid'] = self.total_uids[mIndex]
            fItem['mid'] = self.total_mids[mIndex]
            fItem['comment_flag'] = '1'
            yield fItem
            # 如果self.total_mids里面有新的mid的话，那就爬新的微博的评论
            if mIndex < len(self.total_mids) - 1:
                mIndex += 1
                yield Request(self.url_part_one + str(self.total_mids[mIndex]) + self.url_part_two + '1', cookies=self.cookie,
                               meta={'maxPage': -1, 'nowPage': 1, 'mIndex': mIndex}, callback=self.parse_page)
            else:
                yield None
        else:
            # 否则就爬下一页的评论
            yield Request(self.url_part_one + str(self.total_mids[mIndex]) + self.url_part_two + str(int(nowPage) + 1), cookies=self.cookie,
                           meta={'maxPage': maxPage, 'nowPage': int(nowPage) + 1, 'mIndex': mIndex},
                           callback=self.parse_page)

    # 初始化item
    def init_item(self, item):
        # 爬取评论的时间
        item['crawl_timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        item['uid'] = []
        item['cid'] = []
        item['mid'] = []
        item['reply_id'] = []
        item['text'] = []
        item['source'] = []
        item['like_counts'] = []
        item['created_at'] = []

    # 填写item
    def fill_item(self, item, comment, mid):
        # 用户id
        item['uid'].append(comment['user']['id'])
        # 评论id
        item['cid'].append(comment['id'])
        # 微博id
        item['mid'].append(mid)
        # 如果这条评论是回复其他评论a的，那就是a的id
        if 'reply_id' in comment.keys():
            item['reply_id'].append(comment['reply_id'])
        else:
            item['reply_id'].append('0')
        # 评论内容
        item['text'].append(comment['text'])
        # 来源
        item['source'].append(comment['source'])
        # 点赞数
        item['like_counts'].append(comment['like_counts'])
        # 发评论的时间
        item['created_at'].append(comment['created_at'])

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
