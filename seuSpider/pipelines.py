# -*- coding: utf-8 -*-

from seuSpider.utils.dbManager import dbManager
from seuSpiderHandlers.sinaHandler import sinaHandler
import logging
import MySQLdb
from seuSpiderHandlers.doubanHandler import doubanHandler

class sinaPipeline(object):
    sinaHandlerInstance = sinaHandler()
    def __init__(self):
        self.dbpool = dbManager().get_dbpool()

    def process_item(self, item, spider):
        if 'fid' in item:
            self.dbpool.runInteraction(self.sinaHandlerInstance.sinaRelationDBHandler,item)
        if 'scree_name' in item:
            self.dbpool.runInteraction(self.sinaHandlerInstance.sinaUserInfoDBHandler,item)
        return item
    
class WblogPipeline(object):
    def __init__(self):
        self.dbpool = dbManager().get_dbpool()

    def process_item(self, item, spider):
        if 'insert_time' in item.keys():
            self.dbpool.runInteraction(self.ui_insert, item)
#         elif 'wblog_flag' in item.keys():
#             query = self.dbpool.runInteraction(self.sf_update, item)
#             query.addErrback(self.handle_error)
#             pass
        elif 'allJson' not in item.keys():
            self.dbpool.runInteraction(self.wblog_insert, item)

        return item

    # 插入新用户
    def ui_insert(self, cur, item):
        which_table = str(long(item['uid']) % 200)
        sql = 'INSERT IGNORE INTO userinfo_' + which_table + ' (uid, ' \
                                                     'screen_name, ' \
                                                     'profile_image_url, ' \
                                                     'statuses_count, ' \
                                                     'verified, ' \
                                                     'verified_reason, ' \
                                                     'gender, ' \
                                                     'mbtype, ' \
                                                     'ismember, ' \
                                                     'fansNum, ' \
                                                     'description, ' \
                                                     'verified_type, ' \
                                                     'insert_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cur.execute(sql, (
                item['uid'], item['screen_name'], item['profile_image_url'], item['statuses_count'], item['verified'],
                item['verified_reason'], item['gender'], item['mbtype'], item['ismember'], item['fansNum'],
                item['description'], item['verified_type'], item['insert_time']))
        except MySQLdb.Error, e:
            logging.info("uf_insert:%s" % str(e))
        except Exception as e:
            logging.error('error in ui_insert, the item is%s\n'%str(item))
            logging.error(e)

    # 更新scra_flags表
#     def sf_update(self, cur, item):
#         which_table = str(long(item['uid']) % 200)
#         sql = 'UPDATE scra_flags_' + which_table + ' SET wblog_flag=' + item['wblog_flag'] + ' WHERE uid=' + str(item['uid'])
#         try:
#             cur.execute(sql)
#         except MySQLdb.Error, e:
#             logging.info("sf_update:%s" % str(e))

    # 插入微博
    def wblog_insert(self, cur, item):
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


class CommentPipeline(object):
    def __init__(self):
        # self.dbpool1 = dbManager().get_dbpool()
        self.dbpool = dbManager(my_db='newdb').get_dbpool()

    def process_item(self, item, spider):
        # if 'comment_flag' in item.keys():
        #     self.dbpool1.runInteraction(self.wblog_update, item)
        # else:
        self.dbpool.runInteraction(self.comment_insert, item)
        return item
        # raise DropItem("nothing")

    # 插入评论
    def comment_insert(self, cur, item):
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

    # 更新wblog表
    # def wblog_update(self, cur, item):
    #     which_table = str(long(item['uid']) % 1000)
    #     sql = 'UPDATE wblog_' + which_table + ' SET comment_flag=' + item['comment_flag'] + ' WHERE mid=' + str(item['mid'])
    #     try:
    #         cur.execute(sql)
    #     except MySQLdb.Error, e:
    #         logging.info("sf_update:%s" % str(e))
    #     except Exception as e:
    #         logging.error('error in wblog_update, the item is:%s\n'%str(item))
    #         logging.error(e)


class WblogJsonPipeline(object):
    def __init__(self):
        self.dbpool = dbManager(my_db='sina_wblog_json').get_dbpool()

    def process_item(self, item, spider):
        if 'allJson' in item.keys():
            self.dbpool.runInteraction(self.wblog_json_insert, item)
        else:
            pass
        return item

    # 插入微博
    def wblog_json_insert(self, cur, item):
        which_table = str(long(item['uid'][0]) % 1000)
        sql = 'INSERT IGNORE INTO wblog_json_' + which_table + ' (mid, json_text) VALUES (%s,%s)'
        try:
            cur.execute('SET CHARSET utf8mb4')
            for i in range(len(item['uid'])):
                cur.execute(sql,(item['uid'][i], str(item['allJson'][i])))
        except MySQLdb.Error, e:
            logging.info("wblog_json_insert:%s" % str(e))
        except Exception as e:
            logging.error('error in wblog_json_insert, the item is:%s\n'%str(item))
            logging.error(e)


class doubanPipeline(object):
    doubanHandlerInstance = doubanHandler()
    def __init__(self):
        self.dbpool = dbManager().get_dbpool()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.doubanHandlerInstance.commentDBHandler,item)
        return item

class doubanReviewPipeline(object):
    doubanHandlerInstance = doubanHandler()
    def __init__(self):
        self.dbpool = dbManager().get_dbpool()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.doubanHandlerInstance.reviewDBHandler,item)
        return item

