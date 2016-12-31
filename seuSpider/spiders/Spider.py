# -*- coding:utf-8 -*-
'''
Created on 2016年10月3日

@author: MQ
'''
from seuSpider.scrapy_redis_seu.spiders import RedisSpider
from scrapy import Request
import json
from seuSpider.items.items import UserRelationItem
from seuSpider.items.items import UserInfoItem
from seuSpider.utils.dbManager2 import dbManager2
import sys
import re
import time
import logging

class UserRelationSpider(RedisSpider):
    name = 'user_relation'
    redis_key = 'frelation:start_urls'
#     allowed_domains = ['weibo.cn']
    start_urls = []
    user_list = []
    conn = dbManager2()

    pre_user_count = 1
    custom_settings={
                     'ITEM_PIPELINES' : {
                                            'sina_scra.pipelines.SinaScraPipeline': 300,
                                        }
                     }
    user_current_index = 0
    def __init__(self, *args, **kwargs):
        print '-----__init__--------'
        super(UserRelationSpider, self).__init__(*args, **kwargs)

    #redis 爬取
    def parse(self,response):
#         print '-----parse--------'
        try:
            #获取返回json数据
            json_data = json.loads(response.body)
        except Exception as e:
            #重新请求
            logging.error('\n----------url error----------\n%s\n----------url error---------\njson data is error and the Exception e is ========>%s'%(response.url,str(e)))
#             time.sleep(5)
            #重新请求 ,返回到redis里面，设置优先级
            yield Request(response.url,meta={'dont_redirect': True},dont_filter=True,callback=self.parse)
        else:
            item = UserRelationItem()
            extract_uid = re.findall("100505(.+)_-_FOLLOWERS",response.url)
            extract_page = re.findall("page=(.+)",response.url)
            if len(extract_uid)!=1:
                logging.error('\n----------extract_uid %s error----------%s----------'%(extract_uid,response.url))
            else:
                logging.info('----------------------------------------uid,page=%s,%s'%(extract_uid[0],extract_page[0]))
                item['uid'] = extract_uid
                followerLs = []
                uItem = UserInfoItem()
                #封装关注列表
                uidLs = []
                screenNameLs = []
                profileImgUrlLs = []
                statusCountLs = []
                verifiedLs = []
                verifiedReasonLs = []
                verifiedTypeLs = []
                genderLs = []
                mbtypeLs = []
                ismemberLs = []
                fansNumLs = []
                descriptionLs = []

                if json_data['count'] == None or json_data['count'] == 0 or str(json_data['count'])=='':
                    logging.info('uid::::::'+str(item['uid'])+'at page :::'+str(response.url)+'have no information---------------------------!!!!!write file...')
                    #方案1：单独写一个文件之后处理；方案2：push到redis里面，重新做此url；方案3：循环请求，yield request；
                    try:
                        f = open('noInfomationUrls.txt','a')
                        f.write("rpush frelation:start_urls "+str(response.url)+'\n')
                    except Exception as e:
                        logging.info('uid::::::'+str(item['uid'])+'at page :::'+str(response.url)+'can not write to file noInfomationUrls---------------!!!!!!!')
                    finally:
                        f.close()
                else:
                    for card in json_data['cards'][0]['card_group']:
            #             userLs.append(str(self.user_list[self.user_current_index]))
                        followerLs.append(card['user']['id'])

                        uidLs.append(str(card['user']['id']))
                        screenNameLs.append(card['user']['screen_name'])
                        profileImgUrlLs.append(card['user']['profile_image_url'])
                        statusCountLs.append(card['user']['statuses_count'])
                        verifiedLs.append(card['user']['verified'])
                        verifiedReasonLs.append(card['user']['verified_reason'])
                        descriptionLs.append("".join(re.findall(ur"[\u4e00-\u9fa5a-z0-9\w\-\.,@?^=%&amp;:/~\+#<>\s]+", card['user']['description'])))
                        verifiedTypeLs.append(card['user']['verified_type'])
                        genderLs.append(card['user']['gender'])
                        mbtypeLs.append(card['user']['mbtype'])
                        ismemberLs.append(card['user']['ismember'])
                        fansNumLs.append(card['user']['fansNum'])


                    uItem['uid'] = uidLs
                    uItem['scree_name'] = screenNameLs
                    uItem['profile_img_url'] = profileImgUrlLs
                    uItem['status_count'] = statusCountLs
                    uItem['verified'] = verifiedLs
                    uItem['verified_reason'] = verifiedReasonLs
                    uItem['gender'] = genderLs
                    uItem['mbtype'] = mbtypeLs
                    uItem['ismember'] = ismemberLs
                    uItem['fansNum'] = fansNumLs
                    uItem['description'] = descriptionLs
                    uItem['verified_type'] = verifiedTypeLs


                    item['fid'] = followerLs
            #         item.extend([Request(url,callback=self.parse_page) for url in urls])
                    yield item
                    yield uItem


    def start_requests_bak(self):
#         print '-----start_requests--------'
        #开始的第一个id
        start_id = self.get_pre_user_list()
        try:
            init_url = 'http://m.weibo.cn/page/json?containerid=100505%s_-_FOLLOWERS&page=1'%start_id[0]
            self.start_urls.append(init_url)
            return [Request(url,meta={'currentPage':0,'maxPage':0,'dont_redirect': True},callback=self.parse_page) for url in self.start_urls]
        finally:
            pass

#     def error_function(self,response):
#         print response.url

    def parse_page_bak(self, response):
#         print '-----parse--------'
        try:
            #获取返回json数据
            json_data = json.loads(response.body)
        except Exception as e:
            #重新请求
            logging.error('json data is error and the Exception e is ========>'+str(e))
            time.sleep(5)
            yield Request(response.url,meta={'currentPage':response.meta['currentPage'],'maxPage':response.meta['maxPage'],'dont_redirect': True},dont_filter=True,callback=self.parse_page)
        else:
            #user_list处理完毕或者user_list 是空的，重新获得user_list
            if self.user_current_index == len(self.user_list) or len(self.user_list) == 0:
                self.user_list = self.get_pre_user_list(self.pre_user_count)
            #第一页有maxPage
            if json_data['cards'][0].has_key('maxPage'):
                response.meta['maxPage'] = int(json_data['cards'][0]['maxPage'])
                #纠正第一次的currentPage值
                response.meta['currentPage'] = 2
            item = UserRelationItem()
            item['uid'] = self.user_list[self.user_current_index]
            #当前用户爬完,启动下一用户
            if response.meta['currentPage'] == response.meta['maxPage']+1:
    #             print '=====>over'
                #处理用户flag
                update_sql = 'update scra_flags_0 set frelation_flag = 1 where uid = '+str(self.user_list[self.user_current_index][0])
                cur = self.conn.get_cur('sina')
                cur.execute(update_sql)
                self.conn.commit()
                #user_list index 下移一位
                self.user_current_index = self.user_current_index + 1
                response.meta['currentPage'] = 1
    #             url = 'http://m.weibo.cn/page/json?containerid=100505%s_-_FOLLOWERS&page=1'%str(self.user_list[self.user_current_index][0])
    #             yield Request(url,meta={'currentPage':response.meta['currentPage']+1,'maxPage':response.meta['maxPage']},callback=self.parse_page)

    #         userLs = []
            followerLs = []
            uItem = UserInfoItem()
            #封装关注列表
            uidLs = []
            screenNameLs = []
            profileImgUrlLs = []
            statusCountLs = []
            verifiedLs = []
            verifiedReasonLs = []
            verifiedTypeLs = []
            genderLs = []
            mbtypeLs = []
            ismemberLs = []
            fansNumLs = []
            descriptionLs = []

            if json_data['count'] == None or json_data['count'] == 0 or str(json_data['count'])=='':
                logging.info('user'+str(item['uid'])+'does not follow anyone or '+str(response.url)+'have no information--------------------!!!!!!!')
            else:
                for card in json_data['cards'][0]['card_group']:
        #             userLs.append(str(self.user_list[self.user_current_index]))
                    followerLs.append(card['user']['id'])

                    uidLs.append(str(card['user']['id']))
                    screenNameLs.append(card['user']['screen_name'])
                    profileImgUrlLs.append(card['user']['profile_image_url'])
                    statusCountLs.append(card['user']['statuses_count'])
                    verifiedLs.append(card['user']['verified'])
                    verifiedReasonLs.append(card['user']['verified_reason'])
                    descriptionLs.append("".join(re.findall(ur"[\u4e00-\u9fa5a-z0-9]+", card['user']['description'])))
                    verifiedTypeLs.append(card['user']['verified_type'])
                    genderLs.append(card['user']['gender'])
                    mbtypeLs.append(card['user']['mbtype'])
                    ismemberLs.append(card['user']['ismember'])
                    fansNumLs.append(card['user']['fansNum'])


                uItem['uid'] = uidLs
                uItem['scree_name'] = screenNameLs
                uItem['profile_img_url'] = profileImgUrlLs
                uItem['status_count'] = statusCountLs
                uItem['verified'] = verifiedLs
                uItem['verified_reason'] = verifiedReasonLs
                uItem['gender'] = genderLs
                uItem['mbtype'] = mbtypeLs
                uItem['ismember'] = ismemberLs
                uItem['fansNum'] = fansNumLs
                uItem['description'] = descriptionLs
                uItem['verified_type'] = verifiedTypeLs


                item['fid'] = followerLs
        #         item.extend([Request(url,callback=self.parse_page) for url in urls])
                yield item
                yield uItem

            #如果当前user_list已经遍历完，则请求新的user_list
            if self.user_current_index == len(self.user_list):
                self.user_list = self.get_pre_user_list(self.pre_user_count)
                self.user_current_index = 0
            url = 'http://m.weibo.cn/page/json?containerid=100505%s_-_FOLLOWERS&page=%s'%(str(self.user_list[self.user_current_index][0]),response.meta['currentPage'])
    #         print url
            logging.info(url)
            yield Request(url,meta={'currentPage':response.meta['currentPage']+1,'maxPage':response.meta['maxPage'],'dont_redirect': True},callback=self.parse_page)


    #从数据库获得num个用户列表
    def get_pre_user_list(self,num=1):
        pre_user_list = []
        cur = self.conn.get_cur('sina')
        sql = 'SELECT uid from scra_flags_0 where frelation_flag = 0 ORDER BY id ASC LIMIT 0,%s'%num
        count = cur.execute(sql)
        if count>0:
            pre_user_list = cur.fetchall()
        else:
            sys.exit()
            print 'end=======================================>'
        return pre_user_list


#     def fill_userinfoItem(self,card):
#         uidLs = []
#         screenNameLs = []
#         profileImgUrlLs = []
#         statusCountLs = []
#         verifiedLs = []
#         verifiedReasonLs = []
#         verifiedTypeLs = []
#         genderLs = []
#         mbtypeLs = []
#         ismemberLs = []
#         fansNumLs = []
#
#         uidLs.append(str(card['user']['id']))
#         screenNameLs.append(card['user']['screen_name'])
#         profileImgUrlLs.append(card['user']['profile_image_url'])
#         statusCountLs.append(card['user']['statuses_count'])
#         verifiedLs.append(card['user']['verified'])
#         verifiedReasonLs.append(card['user']['verified_reason'])
#         genderLs.append("".join(re.findall(ur"[\u4e00-\u9fa5a-z0-9]+", card['user']['description'])))
#         verifiedTypeLs.append(card['user']['verified_type'])
#         genderLs.append(card['user']['gender'])
#         mbtypeLs.append(card['user']['mbtype'])
#         ismemberLs.append(card['user']['ismember'])
#         fansNumLs.append(card['user']['fansNum'])
#
#         return None
    @staticmethod
    def close(spider, reason):
        logging.error('Spider closed ==========================================>'+str(reason))
        #重启spider
