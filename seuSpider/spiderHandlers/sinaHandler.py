# -*- coding:utf-8 -*-  
'''
Created on 2016年12月30日

@author: MQ
'''
import re
import logging
import time
from seuSpider.items.sinaItems import sinaRelationItem,sinaRelationItemLs,\
    sinaBlogItem, sinaBlogItemLs, sinaCommentItem, sinaCommentItemLs,\
    sinaUserItem, sinaUserItemLs
import MySQLdb

class sinaHandler(object):
    """
    """
    def __init__(self):
        print "---sinaHandler starting---"
    
    def relationHandler(self,json_data,url):
        """用户关系处理函数
        @json_data 获得的json数据
        @url 爬取的url地址
        """
        relationItem = sinaRelationItem()
        relationItemLs = sinaRelationItemLs()
        current_total = {'current':-2,'total':-2}
        extract_uid = re.findall("100505(.+)_-_FOLLOWERS",url)
        extract_page = int(re.findall("FOLLOWERS&page=(.+)",url)[0])
        if len(extract_uid)!=1:
            logging.error('\nextract_uid %s ur::%s::'%(extract_uid,url))
        else:
            if (not json_data.has_key('count')) or json_data['count'] == None or json_data['count'] == 0 or str(json_data['count'])=='':
                logging.info(str(url)+'have no information !!!!! write file...')
#                 #方案1：单独写一个文件之后处理；方案2：push到redis里面，重新做此url；方案3：循环请求，yield request；
#                 with open('noInfomationUrls.txt','a') as filee:
#                     filee.write("rpush frelation:start_urls "+str(url)+'\n')
                itemList = []
                itemList.append(int(extract_uid[0]))
                itemList.append(-1)
                itemList.append(current_total)
                relationItemLs.sinaRelationLs.append(itemList)
            else:
                if json_data.has_key('maxPage'):
                    current_total['total'] = json_data['maxPage']
                else:
                    current_total['total'] = -1
                for card in json_data['cards']:
                    itemList = []
                    itemList.append(int(extract_uid[0]))
                    itemList.append(int(card['user']['id']))
                    current_total['current'] = extract_page
                    itemList.append(current_total)
                    relationItemLs.sinaRelationLs.append(itemList)
                    
            relationItem['sinaRelation'] = relationItemLs.sinaRelationLs
            return relationItem
            
    def blogHander(self,json_data):
        """用户微博处理函数
        @json_data 获得的json数据
        """
        item = sinaBlogItem()
        itemLs = sinaBlogItemLs()
        
        for mblog in json_data['cards']:
            item_list = self.fillBlog(mblog['mblog'])
            itemLs.sinaBlogEntityLs.append(item_list)
            #处理转发微博
            if mblog.has_key('retweeted_status'):
                item_list = self.fillBlog(mblog['retweeted_status'])
                itemLs.sinaBlogEntityLs.append(item_list)
        item['sinaBlogEntity'] = itemLs.sinaBlogEntityLs
        return item
    
    def fillBlog(self,mblog):
        item_list = []
        item_list.append(mblog['user']['id'])
        item_list.append(mblog['id'])
        #获得转发微博id和用户id
        if mblog.has_key('retweeted_status'):
            item_list.append(mblog['retweeted_status']['id'])
            if mblog['retweeted_status'].has_key('user'):
                item_list.append(mblog['retweeted_status']['user']['id'])
            else:
                item_list.append(0)     
        else:
            item_list.append(0)
            item_list.append(0)
            
        item_list.append(self.filter_emoji('emoji', mblog['text']))
        item_list.append(mblog['source'])
        item_list.append(mblog['reposts_count'])
        item_list.append(mblog['comments_count'])
        item_list.append(mblog['attitudes_count'])
        item_list.append(mblog['bid'])
        item_list.append(self.timeFormat(mblog['created_at']))
#             item_list.append(1)
        return tuple(item_list)
        
    def commentHandler(self,json_data,url):
        """用户微博处理函数
        @json_data 获得的json数据
        """
        item = sinaCommentItem()
        itemLs = sinaCommentItemLs()
        blogId = int(re.findall("&id=(.+)&type=",url)[0])
        for comment in json_data[1]['card_group']:
            item_list = []
            item_list.append(comment['id'])
            item_list.append(comment['user']['id'])
            item_list.append(blogId)
            if comment.has_key('reply_id'):
                item_list.append(comment['reply_id'])
            else:
                item_list.append(0)
            item_list.append(self.filter_emoji('emoji',comment['text']))
            item_list.append(comment['source'])
            item_list.append(comment['like_counts'])
            item_list.append(self.timeFormat(comment['created_at']))
            itemLs.sinaCommentEntityLs.append(tuple(item_list))
        
        item['sinaCommentEntity'] = itemLs.sinaCommentEntityLs
        return item
        
    def userHandler(self,json_data,url):
        
        item = sinaUserItem()
        itemLs = sinaUserItemLs()
        uid = int(re.findall("containerid=230283(.+)_-_INFO",url)[0])
        item_dic = {}
        for info_0 in json_data['cards']:
            for info_1 in info_0['card_group']:
                #昵称
                if info_1['item_name'] == u"昵称":
                    item_dic['nickName'] = info_1['item_content']
                #认证
                if info_1['item_type'] == 'verify_yellow':
                    item_dic['verify'] = info_1['item_content']
                #标签
                if info_1['item_name'] == u"标签":
                    item_dic['tag'] = info_1['item_content']
                #性别
                if info_1['item_name'] == u"性别":
                    item_dic['gender'] = info_1['item_content']
                #所在地
                if info_1['item_name'] == u"所在地":
                    item_dic['location'] = info_1['item_content']
                #简介
                if info_1['item_name'] == u"简介":
                    item_dic['intro'] = info_1['item_content']
                #博客
                if info_1['item_name'] == u"博客":
                    item_dic['blog'] = info_1['item_content']
                #等级
                if info_1['item_name'] == u"等级":
                    item_dic['degree'] = info_1['item_content']
                #信用
                if info_1['item_name'] == u"阳光信用":
                    item_dic['confidence'] = info_1['item_content']
                #注册时间
                if info_1['item_name'] == u"注册时间":
                    item_dic['regtime'] = info_1['item_content']
            if len(item_dic) == 10:
                break
        item_list = []
        item_list.append(uid)
        item_list.append(item_dic['nickName'])
        item_list.append(item_dic['verify'])
        item_list.append(item_dic['tag'])
        item_list.append(item_dic['gender'])
        item_list.append(item_dic['location'])
        item_list.append(item_dic['intro'])
        item_list.append(item_dic['blog'])
        item_list.append(item_dic['degree'])
        item_list.append(item_dic['confidence'])
        item_list.append(item_dic['regtime'])
        itemLs.sinaUserEntityLs.append(tuple(item_list))
        item['sinaUserEntity'] = itemLs.sinaUserEntityLs
        item_list = []
        item_dic = {}
        return item    
        
#---------pipeline DBHandler---------
    def relationDBHandler(self,cur,item):
        """处理新浪关系的数据库操作
        """
#         try:
        if item['sinaRelation'][0][2]['current'] == 1:
            update_sql1 = 'update flag set total = %s where uid = %s'
            cur.execute(update_sql1%(item['sinaRelation'][0][2]['total'],item['sinaRelation'][0][0]))

        update_sql = 'update flag set end_page = %s where uid = %s'
        cur.execute(update_sql%(item['sinaRelation'][0][2]['current'],item['sinaRelation'][0][0]))
        for i in range(len(item['sinaRelation'])):
            relationSql = 'insert ignore into sinaFrelation (uid,fid,insert_time) values(%s,%s,now())'
            cur.execute(relationSql,(item['sinaRelation'][i][0],item['sinaRelation'][i][1]))
#         except Exception as e:
#             logging.error(e)
            
    def sinaUserInfoDBHandler(self,cur,item):
        """处理新浪用户信息的数据库操作
        """
        try:
            user_info_sql = 'insert ignore into userinfo_'+str(0) +\
            ' (uid,screen_name,statuses_count,verified,verified_reason,description,verified_type,gender,mbtype,ismember,fansNum,insert_time)' \
            'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
            cur.execute(user_info_sql,)
        except Exception as e:
#             logging.error('DBError---->userInfo::'+str(item['uid'])+' did not insert into table'+','.join(tableLs))
            logging.error(e)
            
    def sinaBlogDBHandler(self, cur, item):
        which_table = '0'#str(long(item['uid'][0]) % 1000)
        sql = 'INSERT IGNORE INTO wblog_' + which_table + ' (uid,' \
                                                  'mid,retweeted_mid,retweeted_uid,blogtext,source, ' \
                                                  'reposts_count, comments_count, attitudes_count, bid,created_time, ' \
                                                  'crawl_time ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
        try:
            for i in range(len(item['sinaBlogEntity'])):
                cur.execute(sql,item['sinaBlogEntity'][i])
        except MySQLdb.Error, e:
            logging.info("uf_insert:%s" % str(e))
        except Exception as e:
            logging.error('error in wblog_insert, the item is:%s\n'%str(item))
            logging.error(e)
            
    def sinaCommentDBHandler(self, cur, item):
        which_table = str(0)#str(long(item['mid'][0]) % 1000)
        sql = 'INSERT IGNORE INTO comment_' + which_table + ' (cid, ' \
                                                    'uid, ' \
                                                    'mid, ' \
                                                    'reply_id, ' \
                                                    'text, ' \
                                                    'source, ' \
                                                    'like_counts, ' \
                                                    'created_at, ' \
                                                    'crawl_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,now())'
        try:
#             cur.execute('SET CHARSET utf8mb4')
            for i in range(len(item['sinaCommentEntity'])):
                cur.execute(sql,item['sinaCommentEntity'][i])
        except MySQLdb.Error, e:
            logging.info("uf_insert:%s" % str(e))
        except Exception as e:
            logging.error('error in comment_insert, the item is:%s\n'%str(item))
            logging.error(e)
            
            
#-------------------------util-----------------------------
    def filter_emoji(self,restr,desstr):
        """去除emoji表情
                                由于数据库中频频出现表情插入不合法，直接把文字中表情符号去除
        """
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub(restr, desstr)
    
    def timeFormat(self,t):
        """time格式
        """
        formattedTime = '1970-01-01 10:00'
        if len(t.split('-'))==2:
            formattedTime = '2017-'+t
        elif u'分钟前' in t:
            formattedTime = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()-60*int(t.split(u'分钟前')[0])))
        elif u'今天' in t:
            formattedTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))+str(t.split(u'今天')[1])
        return formattedTime
        