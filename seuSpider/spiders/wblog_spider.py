# -*- coding: utf-8 -*-

# 爬取新浪用户的所有微博，顺便记录下用户信息

from seuSpider.scrapy_redis_seu.spiders import RedisSpider
from scrapy import Request
from seuSpider.items.items import SinaWblogItem
from seuSpider.items.items import SinaUserItem
from seuSpider.items.items import SinaAllJsonItem

import re
import json
import time
import logging


class WblogSpider(RedisSpider):
    name = 'sina_wblog'  # 爬虫名称
    allowed_domain = ['weibo.cn']  # 访问的url的域名
    redis_key = 'wblog:start_urls'

    # 不同spider各自的settings
    custom_settings = {
        'ITEM_PIPELINES': {
            'sina_scra.pipelines.WblogPipeline': 300,
            'sina_scra.pipelines.WblogJsonPipeline': 301,
        },
        'DOWNLOADER_MIDDLEWARES' : {
            'sina_scra.ipproxy.middleware.UserAgentMiddleware': 543,
            # 'sina_scra.ipproxy.middleware.noProxyMiddleware':544,
            'sina_scra.ipproxy.middleware.aBuProxyMiddleware':546,
        }
    }

    # 初始化
    def __init__(self, *args, **kwargs):
        logging.info('-----initiating WblogSpider------')
        super(WblogSpider, self).__init__(*args, **kwargs)

    # 解析页面
    def parse(self, response):
        logging.info("parse : " + response.url)

        try:
            render_data = json.loads(response.body)
        except Exception as e:
            #重新请求
            logging.error('json data is wrong on url : %s and the Exception e is ========>%s'%(response.url,str(e)))
            #重新请求 ,返回到redis里面，设置优先级
            yield Request(response.url,meta={'dont_redirect': True},dont_filter=True,callback=self.parse)

        try:
            # mod/pagelist表示当前页有微博内容
            if render_data['cards'][0]['mod_type'] == 'mod/pagelist':
                item = SinaWblogItem()  # 微博内容
                self.init_item(item)

                jItem = SinaAllJsonItem()  # 微博所有json内容
                jItem['uid'] = []
                jItem['allJson'] = []

                for status in render_data['cards'][0]['card_group']:
                    mblog = status['mblog']
                    if 'retweeted_status' in mblog.keys():
                        # 如果有原微博，那么也要保存下来
                        if 'deleted' in mblog['retweeted_status']:
                            dItem = SinaWblogItem()  # 被删除的微博内容
                            self.init_item(dItem)
                            self.fill_dItem(dItem,mblog['retweeted_status'])
                            yield dItem
                        else:
                            reItem = SinaWblogItem()
                            self.init_item(reItem)
                            self.fill_item(reItem, mblog['retweeted_status'])
                            yield reItem

                            # 把整个json保存下来
                            if mblog['retweeted_status']['user']['id']:
                                jItem['uid'].append(mblog['retweeted_status']['user']['id'])
                            else:
                                jItem['uid'].append('0')
                            jItem['allJson'].append(mblog['retweeted_status'])

                            # 并且原微博的作者也要保存
                            uItem = SinaUserItem()  # 原微博的作者
                            self.fill_uItem(uItem, mblog['retweeted_status']['user'])
                            yield uItem

                    # 当前用户的微博
                    if 'deleted' in mblog:
                        dItem = SinaWblogItem()
                        self.init_item(dItem)
                        self.fill_dItem(dItem,mblog)
                        yield dItem
                    else:
                        self.fill_item(item, mblog)
                        # 把整个json保存下来
                        if mblog['user']['id']:
                            jItem['uid'].append(mblog['user']['id'])
                        else:
                            jItem['uid'].append('0')
                        jItem['allJson'].append(mblog)

                yield item
                yield jItem
            else:
                logging.info('empty wblog: ' + response.url)
                try:
                    f = open('noWblogUrls.txt','a')
                    f.write("rpush wblog:start_urls "+str(response.url)+'\n')
                except Exception as e:
                    logging.info('page :::'+str(response.url)+' can not write to file noWblogUrls---------------!!!!!!!')
                finally:
                    f.close()
        except Exception as e:
            logging.error('something is wrong on url : %s and the Exception e is ========>%s'%(response.url,str(e)))


    # # 对start_urls进行初始化
    # def __init__(self):
    #     self.start_urls = []  # 初始url
    #     self.total_uids = []  # 与初始url相对应的uid
    #     self.url_part_one = 'http://m.weibo.cn/page/json?containerid=100505'
    #     self.url_part_two = '_-_WEIBO_SECOND_PROFILE_WEIBO&itemid=&page='
    #     self.total_uids = self.get_pre_user_list(100)
    #     self.conn = dbManager2()
    # #从数据库获得num个用户列表
    # def get_pre_user_list(self,num=1):
    #     pre_user_list = []
    #     result_list=[]
    #     cur = self.conn.get_cur('sina')
    #     sql = 'SELECT uid from scra_flags_0 where wblog_flag = 0 ORDER BY id ASC LIMIT 0,%s'%num
    #     count = cur.execute(sql)
    #     if count>0:
    #         pre_user_list = cur.fetchall()
    #         for i in pre_user_list:
    #             result_list.append(i[0])
    #     else:
    #         sys.exit()
    #         print 'end=======================================>'
    #     cur.close()
    #     return result_list
#
#     # 根据start_urls生成最初的url请求
#     def start_requests(self):
#         #检查现在爬去的页面进度--mq
#         cur = self.conn.get_cur('sina')
#         cur.execute('select uid,currentPage,maxPage from uid_weibo where id = 1')
#         uidData = cur.fetchall()
#         current_uid = uidData[0][0]
#         current_page = 1
#         current_max_page = -1
# #         cur.execute('select uid from scra_flags_0 where wblog_flag = 0 ORDER BY id ASC limit 0,1')
#         scra_flag_uid = self.total_uids[0]
#         logging.info('continue to scrapy --------->>>user: '+str(current_uid)+' currentPage : '+str(current_page)+',current_max_page'+str(current_max_page))
#         if scra_flag_uid == current_uid:
#             current_page = uidData[0][1]
#             current_max_page = uidData[0][2]
#             logging.info('continue to scrapy --------->>>user: '+str(current_uid)+' currentPage : '+str(current_page)+',current_max_page'+str(current_max_page))
#         #检查完毕--mq
#         self.start_urls.append(self.url_part_one + str(self.total_uids[0]) + self.url_part_two + '1')
#         return [Request(url, meta={'maxPage': current_max_page, 'nowPage': current_page, 'uIndex': 0}, callback=self.parse_page) for url in self.start_urls]
#
#     # 处理爬取到的页面
#     def parse_page(self, response):
#         logging.info("parse : " + response.url)
#
#         render_data = json.loads(response.body)
#         if response.meta['maxPage'] == -1:
#             # 第一次进来时需要设置maxPage
#             # mod/empty表示没有内容
#             if render_data['cards'][0]['mod_type'] == 'mod/empty':
#                 maxPage = -1
#             elif 'maxPage' in render_data['cards'][0]:
#                 maxPage = render_data['cards'][0]['maxPage']
#             else:
#                 maxPage = -1
#         else:
#             maxPage = response.meta['maxPage']
#
#         # mod/pagelist表示当前页有微博内容
#         if render_data['cards'][0]['mod_type'] == 'mod/pagelist':
#             item = SinaWblogItem()  # 微博内容
#             self.init_item(item)
#
#             jItem = SinaAllJsonItem()  # 微博所有json内容
#             jItem['uid'] = []
#             jItem['allJson'] = []
#
#             for status in render_data['cards'][0]['card_group']:
#                 mblog = status['mblog']
#                 if 'retweeted_status' in mblog.keys():
#                     # 如果有原微博，那么也要保存下来
#                     if 'deleted' in mblog['retweeted_status']:
#                         dItem = SinaWblogItem()  # 被删除的微博内容
#                         self.init_item(dItem)
#                         self.fill_dItem(dItem,mblog['retweeted_status'])
#                         yield dItem
#                     else:
#                         reItem = SinaWblogItem()
#                         self.init_item(reItem)
#                         self.fill_item(reItem, mblog['retweeted_status'])
#                         yield reItem
#
#                         # 把整个json保存下来
#                         if mblog['retweeted_status']['user']['id']:
#                             jItem['uid'].append(mblog['retweeted_status']['user']['id'])
#                         else:
#                             jItem['uid'].append('0')
#                         jItem['allJson'].append(mblog['retweeted_status'])
#
#                         # 并且原微博的作者也要保存
#                         uItem = SinaUserItem()  # 原微博的作者
#                         self.fill_uItem(uItem, mblog['retweeted_status']['user'])
#                         yield uItem
#
#                 # 当前用户的微博
#                 if 'deleted' in mblog:
#                     dItem = SinaWblogItem()
#                     self.init_item(dItem)
#                     self.fill_dItem(dItem,mblog)
#                     yield dItem
#                 else:
#                     self.fill_item(item, mblog)
#                     # 把整个json保存下来
#                     if mblog['user']['id']:
#                         jItem['uid'].append(mblog['user']['id'])
#                     else:
#                         jItem['uid'].append('0')
#                     jItem['allJson'].append(mblog)
#
#             yield item
#             yield jItem
#
#         # 生成新的request
#         nowPage = response.meta['nowPage']
#         uIndex = response.meta['uIndex']
#         if nowPage >= maxPage:  # nowPage >= maxPage的话说明这个用户的微博已经爬完了
#
# #                 fItem = SinaFlagItem()
# #                 fItem['uid'] = self.total_uids[uIndex]
# #                 fItem['wblog_flag'] = '1'
# #                 yield fItem
#
#             cur = self.conn.get_cur('sina')
#             update_sql = 'update scra_flags_0 set wblog_flag = 1 where uid = %s' %self.total_uids[uIndex]
#             cur.execute(update_sql)
#             self.conn.commit()
#             cur.close()
#             # 如果self.total_uids里面有新的uid的话，那就爬新的用户的微博
#             if uIndex < len(self.total_uids) - 1:
#                 uIndex += 1
#             else:
#                 #内存中用户列表爬完，从数据库中重新获取
#                 self.total_uids = self.get_pre_user_list(100)
#                 #重置uIndex
#                 uIndex = 0
#
#             yield Request(self.url_part_one + str(self.total_uids[uIndex]) + self.url_part_two + '1',
#                                meta={'maxPage': -1, 'nowPage': 1, 'uIndex': uIndex}, callback=self.parse_page)
#         else:  #当前用户的微博还没爬完,爬下一页的微博
#             cur = self.conn.get_cur('sina')
#             update_sql = 'update uid_weibo set uid = %s,currentPage=%s,maxPage=%s where id = 1' %(self.total_uids[uIndex],nowPage,maxPage)
#             cur.execute(update_sql)
#             self.conn.commit()
#             cur.close()
#             logging.info('------------------------------')
#             # 下一页的微博
#             yield Request(self.url_part_one + str(self.total_uids[uIndex]) + self.url_part_two + str(int(nowPage) + 1),
#                            meta={'maxPage': maxPage, 'nowPage': int(nowPage) + 1, 'uIndex': uIndex},
#                            callback=self.parse_page)

    # 初始化item
    def init_item(self, item):
        # 爬取微博的时间
        item['crawl_timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        item['uid'] = []
        item['mid'] = []
        item['bid'] = []
        item['retweeted_mid'] = []
        item['text'] = []
        item['isLongText'] = []
        item['source'] = []
        item['reposts_count'] = []
        item['comments_count'] = []
        item['attitudes_count'] = []
        item['like_count'] = []
        item['hasPic'] = []
        item['hasGif'] = []
        item['hasOutlink'] = []
        item['created_timestamp'] = []

    # 填写item
    def fill_item(self, item, mblog):
        # 用户id
        if mblog['user']['id']:
            item['uid'].append(mblog['user']['id'])
        else:
            item['uid'].append('0')
        # 微博id
        if mblog['mid']:
            item['mid'].append(mblog['mid'])
        else:
            item['mid'].append('0')
        # 微博短id
        if mblog['bid']:
            item['bid'].append(mblog['bid'])
        else:
            item['bid'].append('0')
        # 原微博id
        if 'retweeted_status' in mblog.keys():
            item['retweeted_mid'].append(mblog['retweeted_status']['mid'])
        else:
            item['retweeted_mid'].append('0')
        # 微博内容
        if mblog['text']:
            item['text'].append("".join(re.findall(ur"[\u4e00-\u9fa5a-z0-9\w\-\.,@?^=%&amp;:/~\+#<>\s]+", mblog['text'])))
        else:
            item['text'].append('0')
        # 是否是长微博
        if mblog['isLongText']:
            if mblog['isLongText'] == 'true':
                item['isLongText'].append('1')
            else:
                item['isLongText'].append('0')
        else:
            item['isLongText'].append('0')
        # 微博来源
        if mblog['source']:
            item['source'].append(mblog['source'])
        else:
            item['source'].append('0')
        # 转发数
        if mblog['reposts_count']:
            item['reposts_count'].append(mblog['reposts_count'])
        else:
            item['reposts_count'].append('0')
        # 评论数
        if mblog['comments_count']:
            item['comments_count'].append(mblog['comments_count'])
        else:
            item['comments_count'].append('0')
        # 点赞数
        if mblog['attitudes_count']:
            item['attitudes_count'].append(mblog['attitudes_count'])
        else:
            item['attitudes_count'].append('0')
        # 点赞数，目前不清楚与attitude有什么区别
        if mblog['like_count']:
            item['like_count'].append(mblog['like_count'])
        else:
            item['like_count'].append('0')
        # 是否含有图片
        if mblog['pic_ids']:
            item['hasPic'].append('1')
        else:
            item['hasPic'].append('0')
        # 是否含有gif
        if mblog['gif_ids']:
            item['hasGif'].append('1')
        else:
            item['hasGif'].append('0')
        # 是否含有外链，可能是其他网站，也可能是一个视频
        if 'url_struct' in mblog:
            item['hasOutlink'].append('1')
        else:
            item['hasOutlink'].append('0')
        # 发微博的时间
        if mblog['created_timestamp']:
            item['created_timestamp'].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mblog['created_timestamp'])))
        else:
            item['created_timestamp'].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    # 填写dItem
    def fill_dItem(self, item, mblog):
        # 用户id
        item['uid'].append('0')
        # 微博id
        if mblog['mid']:
            item['mid'].append(mblog['mid'])
        else:
            item['mid'].append('0')
        # 微博短id
        if mblog['bid']:
            item['bid'].append(mblog['bid'])
        else:
            item['bid'].append('0')
        # 原微博id
        item['retweeted_mid'].append('0')
        # 微博内容
        if mblog['text']:
            item['text'].append("".join(re.findall(ur"[\u4e00-\u9fa5a-z0-9\w\-\.,@?^=%&amp;:/~\+#<>\s]+", mblog['text'])))
        else:
            item['text'].append('0')
        # 是否是长微博
        item['isLongText'].append('0')
        # 微博来源
        if mblog['source']:
            item['source'].append(mblog['source'])
        else:
            item['source'].append('0')
        # 转发数
        item['reposts_count'].append('0')
        # 评论数
        item['comments_count'].append('0')
        # 点赞数
        item['attitudes_count'].append('0')
        # 点赞数，目前不清楚与attitude有什么区别
        item['like_count'].append('0')
        # 是否含有图片
        item['hasPic'].append('0')
        # 是否含有gif
        item['hasGif'].append('0')
        # 是否含有外链，可能是其他网站，也可能是一个视频
        item['hasOutlink'].append('0')
        # 发微博的时间
        if mblog['created_timestamp']:
            item['created_timestamp'].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mblog['created_timestamp'])))
        else:
            item['created_timestamp'].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    # 填写uItem
    def fill_uItem(self, uItem, user):
        uItem['uid'] = user['id'] if user['id'] else '0'
        uItem['screen_name'] = user['screen_name'] if user['screen_name'] else '0'
        uItem['profile_image_url'] = user['profile_image_url'] if user['profile_image_url'] else '0'
        uItem['statuses_count'] = user['statuses_count'] if user['statuses_count'] else '0'
        uItem['verified'] = user['verified'] if user['verified'] else '0'
        uItem['verified_reason'] = user['verified_reason'] if user['verified_reason'] else '0'
        uItem['gender'] = user['gender'] if user['gender'] else '0'
        uItem['mbtype'] = user['mbtype'] if user['mbtype'] else '0'
        uItem['ismember'] = user['ismember'] if user['ismember'] else '0'
        uItem['fansNum'] = user['fansNum'] if user['fansNum'] else '0'
        uItem['description'] = "".join(re.findall(ur"[\u4e00-\u9fa5a-z0-9\w\-\.,@?^=%&amp;:/~\+#<>\s]+", user['description'])) if user['description'] else '0'
        uItem['verified_type'] = user['verified_type'] if user['verified_type'] else '0'
        uItem['insert_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
