# -*- coding:utf-8 -*-  
'''
Created on 2016年12月30日

@author: MQ
'''
import re
from seuSpider.items.doubanItems import doubanShortCommentItem,shortCommentItemLs,\
    doubanRelationItem, relationItemLs,doubanReviewItem,reviewItemLs,\
    doubanReviewCommentItem, doubanReviewCommentItemLs,doubanUserInfoItem,\
    doubanUserGroupRelationItem, doubanUserGroupRelationItemLs,\
    doubanFilmItem, doubanFilmItemLs, doubanGroupInfoItem, doubanGroupInfoItemLs
    
# from seuSpider.items.doubanItems import userItem,userItemLs
import logging

class doubanHandler(object):
    """
    """
    def __init__(self):
        pass
    
    
    def commentHandler(self,json_data,movie_id):
        """豆瓣短评处理
        """
        print '-----commentHandler--------'
        item = doubanShortCommentItem()
        itemLs = shortCommentItemLs()
        itemLs.movie_idLs.append(movie_id)
        for interest in json_data["interests"]:
            itemLs.cuidLs.append(interest["user"]["id"])
            itemLs.commentIdLs.append(interest["id"])
            #替换短评内容中的emoji
            comment_tem = self.filter_emoji('(emoji)',interest["comment"])
            itemLs.commentLs.append(comment_tem)
            if type(interest["rating"])== type(None):
                itemLs.ratingLs.append("null")
            else:
                itemLs.ratingLs.append(str(interest["rating"]["count"])+","+str(interest["rating"]["max"])+","+str(interest["rating"]["value"]))
            itemLs.vote_countLs.append(interest["vote_count"])
            itemLs.create_timeLs.append(interest["create_time"])
        item["movie_id"] = itemLs.movie_idLs
        item["cuid"] = itemLs.cuidLs
        item["commentId"] = itemLs.commentIdLs
        item["comment"]= itemLs.commentLs
        item["rating"] = itemLs.ratingLs
        item["vote_count"] = itemLs.vote_countLs
        item["create_time"] = itemLs.create_timeLs
        return item
    
    
    def reviewHandler(self,json_data,movie_id):
        """豆瓣影评处理（长评）
        """
        print '-----reviewHandler--------'
        item = doubanReviewItem()
        itemLs = reviewItemLs()
        #电影id增加，爬取多个电影的长评
        itemLs.movie_idLs.append(movie_id)
        for reviews in json_data["reviews"]:
            itemLs.cuidLs.append(reviews["user"]["id"])
            itemLs.reviewIdLs.append(reviews["id"])
            #替换emoji表情
            title_tem = self.filter_emoji('(emoji)', reviews["title"])
            itemLs.titleLs.append(title_tem)
            if type(reviews["rating"])== type(None):
                itemLs.ratingLs.append("null")
            else:
                itemLs.ratingLs.append(str(reviews["rating"]["count"])+","+str(reviews["rating"]["max"])+","+str(reviews["rating"]["value"]))
            itemLs.useful_countLs.append(reviews["useful_count"])
            itemLs.likers_countLs.append(reviews["likers_count"])
            itemLs.vote_statusLs.append(reviews["vote_status"])
            itemLs.useless_countLs.append(reviews["useless_count"])
            itemLs.create_timeLs.append(reviews["create_time"])
            itemLs.comments_countLs.append(reviews["comments_count"])
        
        item["movie_id"] = itemLs.movie_idLs    
        item["cuid"] = itemLs.cuidLs
        item["reviewId"] = itemLs.reviewIdLs
        item["title"]= itemLs.titleLs
        item["rating"] = itemLs.ratingLs
        item["useful_count"] = itemLs.useful_countLs
        item["likers_count"] = itemLs.likers_countLs
        item["vote_status"] = itemLs.vote_statusLs
        item["useless_count"] = itemLs.useless_countLs
        item["comments_count"] = itemLs.comments_countLs
        item["create_time"] = itemLs.create_timeLs
        return item
    
    def relationHandler(self,json_data,url):
        """豆瓣用户关注关系 夹带 用户信息
        2017.1.20去掉电影长评所带用户信息
        """
        logging.info(url)
        item = doubanRelationItem()
        itemLs = relationItemLs()
        
#         uitem = userItem()
#         uitemLs = userItemLs()
        
        extract_uid = re.findall("user/(.+)/followers",url)#url相关
        itemLs.uidLs.append(int(extract_uid[0]))
        for user in json_data['users']:
            itemLs.fidLs.append(int(user['id']))
            
            #用户信息封装            
#             uitemLs.uidLs.append(user['id'])
#             uitemLs.unidLs.append(user['uid'])
#             if user['loc'] == None:
#                 uitemLs.locLs.append('Null')
#             else:
#                 uitemLs.locLs.append(user['loc']['id']+','+user['loc']['name']+','+user['loc']['uid'])
#             uitemLs.nameLs.append(user['name'])
#             if user['gender'] == '':
#                 uitemLs.genderLs.append('Null')
#             else:
#                 uitemLs.genderLs.append(user['gender'])
#             uitemLs.introLs.append(user['abstract'].strip())
#             uitemLs.followers_countLs.append(user['followers_count'])
        
        item['uid'] = itemLs.uidLs
        item['fid'] = itemLs.fidLs
        
#         uitem['uid'] = uitemLs.uidLs
#         uitem['unid'] = uitemLs.unidLs
#         uitem['loc'] = uitemLs.locLs
#         uitem['name'] = uitemLs.nameLs
#         uitem['gender'] = uitemLs.genderLs
#         uitem['intro'] = uitemLs.introLs
#         uitem['followers_count'] = uitemLs.followers_countLs

        return item#,uitem
    
    def reviewCommentHandler(self,json_data,url):
        """豆瓣影评的评论（回应）夹带 相关用户
        2017.1.20去掉电影长评所带用户信息
        """
        logging.info(url)
        item = doubanReviewCommentItem()
        itemLs = doubanReviewCommentItemLs()
        
#         uitem = userItem()
#         uitemLs = userItemLs()
        extract_rid = re.findall("review/(.+)/comments",url)#url相关
        itemLs.ridLs.append(int(extract_rid[0]))
        for reviewComment in json_data['comments']:
            itemLs.rcidLs.append(reviewComment['id'])
            itemLs.uidLs.append(reviewComment['author']['id'])
            if reviewComment['ref_comment'] == None:
                itemLs.rrcidLs.append(0)
            else:
                itemLs.rrcidLs.append(reviewComment['ref_comment']['id'])
            itemLs.textLs.append(reviewComment['text'])
            itemLs.create_timeLs.append(reviewComment['create_time'])
            
#             #用户信息封装
#             uitemLs.uidLs.append(reviewComment['author']['id'])
#             uitemLs.unidLs.append(reviewComment['author']['uid'])
#             if reviewComment['author']['loc'] == None:
#                 uitemLs.locLs.append('Null')
#             else:
#                 uitemLs.locLs.append(reviewComment['author']['loc']['id']+','+reviewComment['author']['loc']['name']+','+reviewComment['author']['loc']['uid'])
#             uitemLs.nameLs.append(reviewComment['author']['name'])
#             if reviewComment['author']['gender'] == '':
#                 uitemLs.genderLs.append('Null')
#             else:
#                 uitemLs.genderLs.append(reviewComment['author']['gender'])
#             uitemLs.introLs.append(reviewComment['author']['abstract'].strip())
        
        item['rcid'] = itemLs.rcidLs
        item['rid'] = itemLs.ridLs
        item['uid'] = itemLs.uidLs
        item['rrcid'] = itemLs.rrcidLs
        item['text'] = itemLs.textLs
        item['create_time'] = itemLs.create_timeLs
        
#         uitem['uid'] = uitemLs.uidLs
#         uitem['unid'] = uitemLs.unidLs
#         uitem['loc'] = uitemLs.locLs
#         uitem['name'] = uitemLs.nameLs
#         uitem['gender'] = uitemLs.genderLs
#         uitem['intro'] = uitemLs.introLs
        
        return item#,uitem
    
    def userInfoHandler(self,json_data):
        """处理豆瓣用户详细信息
        """
        item = doubanUserInfoItem()
        
        item['id'] = json_data['id']
        item['uid'] = json_data['uid']
        item['following_count'] = json_data['following_count']
        item['seti_channel_count'] = json_data['seti_channel_count']
        item['photo_albums_count'] = json_data['photo_albums_count']
#         item['abstract'] = json_data['abstract'].strip()
        item['intro'] = json_data['intro'].strip()
        item['notes_count'] = json_data['notes_count']
        if json_data['loc'] == None:
            item['loc'] = 'Null'
        else:
            item['loc'] = json_data['loc']['id']+','+json_data['loc']['name']+','+json_data['loc']['uid']
        item['reg_time'] = json_data['reg_time']
        item['joined_group_count'] = json_data['joined_group_count']
        item['followers_count'] = json_data['followers_count']
        item['is_phone_bound'] = json_data['is_phone_bound']
        item['verify_type'] = json_data['verify_type']
        item['updated_profile'] = json_data['updated_profile']
        item['type'] = json_data['updated_profile']
        item['statuses_count'] = json_data['statuses_count']
        item['group_chat_count'] = json_data['group_chat_count']
        item['owned_doulist_count'] = json_data['owned_doulist_count']
        item['birthday'] = json_data['birthday']
        item['collected_subjects_count'] = json_data['collected_subjects_count']
        item['name'] = json_data['name']
        if json_data['gender'] == '':
            item['gender'] = 'Null'
        else:
            item['gender'] = json_data['gender']
        item['verify_reason'] = json_data['verify_reason']
        item['ark_published_count'] = json_data['ark_published_count']
        item['following_doulist_count'] = json_data['following_doulist_count']
        item['is_normal'] = json_data['is_normal']
        
        return item
    
    def userGroupRelationHandler(self,json_data,url):
        """用户群组加入关系
        """
        extract_uid = re.findall("user/(.+)/joined_groups",url)#url相关
        
        item = doubanUserGroupRelationItem()
        itemLs = doubanUserGroupRelationItemLs()
        itemLs.uidLs.append(int(extract_uid[0]))
        for ugrelation in json_data['groups']:
            itemLs.gidLs.append(ugrelation['id'])
            itemLs.gnameLs.append(self.filter_emoji("emoji", ugrelation['name']))
            
        item['uid'] = itemLs.uidLs
        item['gid'] = itemLs.gidLs
        item['gname'] = itemLs.gnameLs
        
        return item
    
    def filmInfoHandler(self,json_data):
        """豆瓣电影信息
        """
#         item = doubanFilmInfo()
#         itemLs = doubanFilmInfoLs()
#         
#         for filmInfo in json_data:
#             itemLs.idLs.append(re.findall("subject/(.+)",filmInfo['url'])[0])
#             itemLs.scoreLs.append(filmInfo['score'])
#             itemLs.starsLs.append(filmInfo['stars'])
#             itemLs.directorLs.append(filmInfo['desc'][0])
#             itemLs.starringLs.append(filmInfo['desc'][1])
#             itemLs.typeLs.append(filmInfo['desc'][2])
#             itemLs.countryLs.append(filmInfo['desc'][3])
#             itemLs.yearLs.append(filmInfo['desc'][4])
#             
#         item['id']       = itemLs.idLs
#         item['score']    = itemLs.scoreLs
#         item['stars']    = itemLs.starsLs
#         item['director'] = itemLs.directorLs
#         item['starring'] = itemLs.starringLs
#         item['type']     = itemLs.typeLs
#         item['country']  = itemLs.countryLs
#         item['year']     = itemLs.yearLs
        
        item = doubanFilmItem()
        itemLs = doubanFilmItemLs()
        
        for filmInfo in json_data:
            item_list = []
            if filmInfo.has_key('url'):
                item_list.append(int(re.findall("subject/(.+)",filmInfo['url'])[0]))
            else:
                continue
            if filmInfo.has_key('title'):
                item_list.append(filmInfo['title'])
            else:
                item_list.append('')
            if filmInfo.has_key('score'):
                item_list.append(filmInfo['score'])
            else:
                item_list.append('')
            if filmInfo.has_key('stars'):   
                item_list.append(int(filmInfo['stars']))
            else:
                item_list.append(-1)
            
            director = ''
            starring = ''
            type_film = ''
            country = ''
            year = ''
            for desc in filmInfo['desc']:
                if u'导演' in desc:
                    director = desc
                elif u'主演' in desc:
                    starring = desc
                elif u'类型' in desc:
                    type_film = desc
                elif u'制片国家' in desc:
                    country = desc
                elif u'年份' in desc:
                    year = desc
                else:
                    director = u'描述错误'
                    
                    
            item_list.append(director)
            item_list.append(starring)
            item_list.append(type_film)
            item_list.append(country)
            item_list.append(year)
            
            itemLs.doubanEntityLs.append(tuple(item_list))
            
        item['doubanEntity'] = itemLs.doubanEntityLs
        return item
    
    def groupInfoHandler(self,json_data):
        """豆瓣小组信息处理函数
        """
        
        item = doubanGroupInfoItem()
        itemLs = doubanGroupInfoItemLs()
        
        item_tmp = []
        item_tmp.append(int(json_data['id']))
        item_tmp.append(json_data['name'])
        item_tmp.append(int(json_data['member_count']))
        item_tmp.append(json_data['manager_name']+"|"+json_data['member_name'])
        item_tmp.append(json_data['create_time'])
        item_tmp.append(int(json_data['owner']['id']))
        item_tmp.append(self.filter_emoji('(emoji)',json_data['desc']))
        
        itemLs.groupInfoLs.append(tuple(item_tmp))
        
        item['groupInfo'] = itemLs.groupInfoLs
        
        return item
        
        
        
        
    
    
#---------- ------------
    def commentDBHandler(self,cur,item):
        """豆瓣短评数据库处理函数
        """
        commentSql = 'insert ignore into comments (movie_id,cuid,commentId,comment,rating,vote_count,create_time,insert_time) values(%s,%s,%s,%s,%s,%s,%s,now())'
        try:
            for i in range(len(item["cuid"])):
                cur.execute(commentSql,(int(item['movie_id'][0]),int(item['cuid'][i]),int(item['commentId'][i]),item['comment'][i],item['rating'][i],int(item['vote_count'][i]),item['create_time'][i]))
        except Exception as e:
            logging.error('DBError---->uidList::'+str(item['cuid'][0])+' did not insert into table')
            logging.error(e)

    def reviewDBHandler(self,cur,item):
        """豆瓣长评数据库处理函数
        """
        reviewSql = 'insert ignore into reviews (movie_id,cuid,rid,title,rating,useful_count,likers_count,vote_status,useless_count,comments_count,create_time,insert_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
        try:
            for i in range(len(item['cuid'])):
                cur.execute(reviewSql,(int(item['movie_id'][0]),int(item['cuid'][i]),int(item['reviewId'][i]),item['title'][i],item['rating'][i],int(item['useful_count'][i]),int(item['likers_count'][i]),int(item['vote_status'][i]),int(item['useless_count'][i]),int(item['comments_count'][i]),item['create_time'][i]))
                
        except Exception as e:
            logging.error('DBError---->uidList::'+str(item['cuid'][0])+' did not insert into table')
            logging.error(e)
            
    def relationDBHandler(self,cur,item):
        """豆瓣用户关注关系数据库处理函数
        """
#         relationSql = 'insert ignore into relations (uid,fid,insert_time) values (%s,%s,now())'
        followerSql = 'insert ignore into followers (uid,fid,insert_time) values (%s,%s,now())'
        try:
            for i in range(len(item['fid'])):
                cur.execute(followerSql,(item['uid'][0],item['fid'][i]))
        except Exception as e:
            logging.error("relationDBHandler: "+str(e))
    
#     def userDBHandler(self,cur,item):
#         """豆瓣用户信息数据库处理函数
#         """
#         userSql = "insert ignore into users (uid,unid,intro,loc,followers_count,name,gender) values (%s,%s,%s,%s,%s,%s,%s)"
#         try:
#             for i in range(len(item['uid'])):
#                 cur.execute(userSql,(item['uid'][i],item['unid'][i],item['intro'][i],item['loc'][i],item['followers_count'][i],item['name'][i],item['gender'][i]))
#         except Exception as e:
#             logging.error("userDBHandler: "+str(e))
            
    def userInfoDBHandler(self,cur,item):
        """豆瓣用户详细信息页面用户信息
        """
        userInfoSql = "insert ignore into userInfo (id,uid,following_count,seti_channel_count,photo_albums_count,intro,notes_count,loc,reg_time,joined_group_count,followers_count,is_phone_bound,verify_type,updated_profile,type,statuses_count,group_chat_count,owned_doulist_count,birthday,collected_subjects_count,name,gender,verify_reason,ark_published_count,following_doulist_count,is_normal) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cur.execute('SET CHARSET utf8mb4')
            cur.execute(userInfoSql,(item['id'],item['uid'],item['following_count'],item['seti_channel_count'],item['photo_albums_count'],item['intro'],item['notes_count'],item['loc'],item['reg_time'],item['joined_group_count'],item['followers_count'],item['is_phone_bound'],item['verify_type'],item['updated_profile'],item['type'],item['statuses_count'],item['group_chat_count'],item['owned_doulist_count'],item['birthday'],item['collected_subjects_count'],item['name'],item['gender'],item['verify_reason'],item['ark_published_count'],item['following_doulist_count'],item['is_normal']))
        except Exception as e:
            logging.error("userInfoDBHandler: "+str(e))

    def reviewCommentDBHandler(self,cur,item):
        """豆瓣用户影评评论（回应）数据库处理函数
        """
        reviewCommentSql = "insert ignore into reviewComment (rcid,rid,uid,rrcid,text,create_time) values (%s,%s,%s,%s,%s,%s)"
#         print reviewCommentSql%(item['rcid'][0],item['rid'],item['uid'][0],item['rrcid'][0],item['text'][0],item['create_time'][0])
        try:
            for i in range(len(item['rcid'])):
                cur.execute(reviewCommentSql,(item['rcid'][i],item['rid'][0],item['uid'][i],item['rrcid'][i],item['text'][i],item['create_time'][i]))
        except Exception as e:
            logging.error("reviewCommentDBHandler: "+str(e))
            
    def groupInformationDBHandler(self,cur,item):
        """豆瓣小组信息数据库处理函数
        """
        try:
            for i in range(len(item['xx'])):
                cur.execute()
        except Exception as e:
            logging.error("groupInformationDBHandler: "+str(e))
    
    def userGroupRelationDBHandler(self,cur,item):
        """用户加入小组关系数据库处理函数
        """
        userGroupSql = "insert ignore into userGroupRelation(uid,groupid,group_name,insert_time) values(%s,%s,%s,now())"
        try:
            for i in range(len(item['gid'])):
                cur.execute(userGroupSql,(item['uid'][0],item['gid'][i],item['gname'][i]))
        except Exception as e:
            logging.error("userGroupRelationDBHandler "+str(e))

    def filmInfoDBHandler(self,cur,item):
        """豆瓣电影信息
        """
        filmInfoSql = "insert ignore into movies2016 (id,title,score,stars,director,starring,type,country,year) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            for i in range(len(item['doubanEntity'])):
                cur.execute(filmInfoSql,item['doubanEntity'][i])
        except Exception as e:
            logging.error("filmInfoDBHandler "+str(e))
            
    def groupInfoDBHandler(self,cur,item):
        """豆瓣小组信息处理函数
        """
        groupInfoSql = "insert ignore into groupInfo(id,name,member_count,manager_member,create_time,owner_id,description,insert_time) values (%s,%s,%s,%s,%s,%s,%s,now())"
#         print groupInfoSql%item['groupInfo'][0]
        try:
            cur.execute(groupInfoSql,item['groupInfo'][0])
        except Exception as e:
            logging.error('doubanGroupInfoDBHandler'+str(e))
            
        
    def filter_emoji(self,restr,desstr):
        """去除emoji表情
                                由于数据库中频频出现表情插入不合法，直接把文字中表情符号去除
        """
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub(restr, desstr)