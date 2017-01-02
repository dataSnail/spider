# -*- coding:utf-8 -*-  
'''
Created on 2016年12月30日

@author: MQ
'''
import re
import logging
from seuSpider.items.sinaItems import userRelationItem,userRelationitemLs
from seuSpider.items.sinaItems import userInfoItem,userInfoItemLs
import MySQLdb

class sinaHandler(object):
    """
    """
    def __init__(self):
        print "---sinaHandler starting---"
    
    def userRelationHandler(self,json_data,url):
        """用户关系处理函数
        @json_data 获得的json数据
        @url 爬取的url地址
        """
        uiItem = userInfoItem()
        uiItemLs = userInfoItemLs()
        
        urItem = userRelationItem()
        urItemLs = userRelationitemLs()
        
        extract_uid = re.findall("100505(.+)_-_FOLLOWERS",url)
        extract_page = re.findall("page=(.+)",url)
        if len(extract_uid)!=1:
            logging.error('\n----------extract_uid %s error----------%s----------'%(extract_uid,url))
        else:
            logging.info('----------------------------------------uid,page=%s,%s'%(extract_uid[0],extract_page[0]))
            urItem['uid'] = extract_uid

            if json_data['count'] == None or json_data['count'] == 0 or str(json_data['count'])=='':
                logging.info('uid::::::'+str(urItem['uid'])+'at page :::'+str(url)+'have no information---------------------------!!!!!write file...')
                #方案1：单独写一个文件之后处理；方案2：push到redis里面，重新做此url；方案3：循环请求，yield request；
                with open('noInfomationUrls.txt','a') as file:
                    file.write("rpush frelation:start_urls "+str(url)+'\n')
            else:
                for card in json_data['cards']:
        #             userLs.append(str(self.user_list[self.user_current_index]))
                    urItemLs.fidLs.append(card['user']['id'])

                    uiItemLs.uidLs.append(str(card['user']['id']))
                    uiItemLs.scree_nameLs.append(card['user']['screen_name'])
                    uiItemLs.profile_img_urlLs.append(card['user']['profile_image_url'])
                    uiItemLs.status_countLs.append(card['user']['statuses_count'])
                    uiItemLs.verifiedLs.append(card['user']['verified'])
                    if card['user']['verified']:
                        uiItemLs.verified_reasonLs.append(card['user']['verified_reason'])
                    else:
                        uiItemLs.verified_reasonLs.append("None")
                    uiItemLs.descriptionLs.append("".join(re.findall(ur"[\u4e00-\u9fa5a-z0-9\w\-\.,@?^=%&amp;:/~\+#<>\s]+", card['user']['description'])))
                    uiItemLs.verified_typeLs.append(card['user']['verified_type'])
                    uiItemLs.genderLs.append(card['user']['gender'])
                    uiItemLs.mbtypeLs.append(card['user']['mbtype'])
                    uiItemLs.mbrankLs.append(card['user']['mbrank'])
                    uiItemLs.followers_countLs.append(card['user']['followers_count'])

                urItem['fid'] = urItemLs.fidLs
                
                uiItem['uid'] = uiItemLs.uidLs
                uiItem['scree_name'] = uiItemLs.scree_nameLs
                uiItem['profile_img_url'] = uiItemLs.profile_img_urlLs
                uiItem['status_count'] = uiItemLs.status_countLs
                uiItem['verified'] = uiItemLs.verifiedLs
                uiItem['verified_reason'] = uiItemLs.verified_reasonLs
                uiItem['gender'] = uiItemLs.genderLs
                uiItem['mbtype'] = uiItemLs.mbtypeLs
                uiItem['mbrank'] = uiItemLs.mbrankLs
                uiItem['followers_count'] = uiItemLs.followers_countLs
                uiItem['description'] = uiItemLs.descriptionLs
                uiItem['verified_type'] = uiItemLs.verified_typeLs

                return uiItem,urItem
            
            
            
#---------pipeline DBHandler---------
    def sinaRelationDBHandler(self,cur,item):
        """处理新浪关系的数据库操作
        """
        try:
            for i in range(len(item['fid'])):
                f_sql = 'insert ignore into frelation_0 (uid,fid,insert_time) values(%s,%s,now())'
    #                 s_sql = 'insert ignore into scra_flags_2 (uid) values(%s)'
                cur.execute(f_sql,(item['uid'][0],item['fid'][i]))
    #                 tx.execute(s_sql,(item['fid'][i],))
        except Exception as e:
#             logging.error('DBError---->uidList::'+str(item['uid'][0])+' and fidList::'+str(item['fid'])+'did not insert into table')
            logging.error(e)
            
    def sinaUserInfoDBHandler(self,cur,item):
        """处理新浪用户信息的数据库操作
        """
        try:
            for i in range(len(item['uid'])):
    #                 tableLs.append(str(thash().uhash(uItem['uid'][i],200)))
                user_info_sql = 'insert ignore into userinfo_0 (uid,screen_name,profile_image_url,statuses_count,verified,verified_reason,description,verified_type,gender,mbtype,ismember,fansNum,insert_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
                user_info_tuple =(item['uid'][i],item['scree_name'][i],item['profile_img_url'][i],item['status_count'][i],item['verified'][i],item['verified_reason'][i],\
                item['description'][i],item['verified_type'][i],item['gender'][i],item['mbtype'][i],item['mbrank'][i],item['followers_count'][i])
                cur.execute(user_info_sql,user_info_tuple)
    #             logging.info('userinfo_'+','.join(tableLs)+' is inserting.....|||||')
        except Exception as e:
    #             logging.error('DBError---->userInfo::'+str(uItem['uid'])+' did not insert into table'+','.join(tableLs))
            logging.error(e)
            
    def sinaMblogDBHandler(self, cur, item):
        which_table = str(long(item['uid'][0]) % 1000)
        sql = 'INSERT IGNORE INTO wblog_' + which_table + ' (uid, ' \
                                                  'mid, ' \
                                                  'bid, ' \
                                                  'retweeted_mid, ' \
                                                  'text, ' \
                                                  'isLongText, ' \
                                                  'source, ' \
                                                  'reposts_count, ' \
                                                  'comments_count, ' \
                                                  'attitudes_count, ' \
                                                  'like_count, ' \
                                                  'hasPic, ' \
                                                  'hasGif, ' \
                                                  'hasOutlink, ' \
                                                  'created_timestamp, ' \
                                                  'crawl_timestamp, ' \
                                                  'comment_flag) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            for i in range(len(item['uid'])):
                if item['comments_count'][i] == 0:
                    comment_flag = '1'
                else:
                    comment_flag = '0'
                cur.execute(sql,
                            (item['uid'][i], item['mid'][i], item['bid'][i], item['retweeted_mid'][i], item['text'][i],
                             item['isLongText'][i], item['source'][i],
                             item['reposts_count'][i], item['comments_count'][i], item['attitudes_count'][i],
                             item['like_count'][i], item['hasPic'][i],
                             item['hasGif'][i], item['hasOutlink'][i], item['created_timestamp'][i],
                             item['crawl_timestamp'], comment_flag))
        except MySQLdb.Error, e:
            logging.info("uf_insert:%s" % str(e))
        except Exception as e:
            logging.error('error in wblog_insert, the item is:%s\n'%str(item))
            logging.error(e)
            
    def sinaCommentDBHandler(self, cur, item):
        which_table = str(0)#str(long(item['mid'][0]) % 1000)
        sql = 'INSERT IGNORE INTO comment_' + which_table + ' (uid, ' \
                                                    'cid, ' \
                                                    'mid, ' \
                                                    'reply_id, ' \
                                                    'text, ' \
                                                    'source, ' \
                                                    'like_counts, ' \
                                                    'created_at, ' \
                                                    'crawl_timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
#             cur.execute('SET CHARSET utf8mb4')
            for i in range(len(item['cid'])):
                cur.execute(sql,
                            (item['uid'][i], item['cid'][i], item['mid'][i], item['reply_id'][i], item['text'][i],
                             item['source'][i],
                             item['like_counts'][i], item['created_at'][i],
                             item['crawl_timestamp']))
        except MySQLdb.Error, e:
            logging.info("uf_insert:%s" % str(e))
        except Exception as e:
            logging.error('error in comment_insert, the item is:%s\n'%str(item))
            logging.error(e)