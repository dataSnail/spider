# -*- coding:utf-8 -*-  
'''
Created on 2016年12月30日

@author: MQ
'''
from seuSpider.items.doubanItems import shortCommentItem,shortCommentItemLs
from seuSpider.items.doubanItems import reviewItem,reviewItemLs
import logging

class doubanHandler(object):
    """
    """
    def __init__(self):
        print '-----doubanHandler starting--------'
    
    
    def commentHandler(self,json_data):
        """豆瓣短评处理
        """
        print '-----commentHandler--------'
        item = shortCommentItem()
        itemLs = shortCommentItemLs()
        
        for interest in json_data["interests"]:
            itemLs.cuidLs.append(interest["user"]["id"])
            itemLs.commentIdLs.append(interest["id"])
            itemLs.commentLs.append(interest["comment"])
            if type(interest["rating"])== type(None):
                itemLs.ratingLs.append("null")
            else:
                itemLs.ratingLs.append(str(interest["rating"]["count"])+","+str(interest["rating"]["max"])+","+str(interest["rating"]["value"]))
            itemLs.vote_countLs.append(interest["vote_count"])
            itemLs.create_timeLs.append(interest["create_time"])
        item["cuid"] = itemLs.cuidLs
        item["commentId"] = itemLs.commentIdLs
        item["comment"]= itemLs.commentLs
        item["rating"] = itemLs.ratingLs
        item["vote_count"] = itemLs.vote_countLs
        item["create_time"] = itemLs.create_timeLs
        return item
    
    
    def reviewHandler(self,json_data):
        """豆瓣影评处理
        """
        print '-----reviewHandler--------'
        item = reviewItem()
        itemLs = reviewItemLs()
        
        for reviews in json_data["reviews"]:
            itemLs.cuidLs.append(reviews["user"]["id"])
            itemLs.reviewIdLs.append(reviews["id"])
            itemLs.titleLs.append(reviews["title"])
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
    
    def commentDBHandler(self,cur,item):
        commentSql = 'insert ignore into comments (cuid,commentId,comment,rating,vote_count,create_time,insert_time) values(%s,%s,%s,%s,%s,%s,now())'
        try:
            for i in range(len(item["cuid"])):
                cur.execute(commentSql,(int(item['cuid'][i]),int(item["commentId"][i]),item["comment"][i],item["rating"][i],int(item["vote_count"][i]),item["create_time"][i]))
        except Exception as e:
            logging.error('DBError---->uidList::'+str(item['cuid'][0])+' did not insert into table')
            logging.error(e)

    def reviewDBHandler(self,tx,item):
        commentSql = 'insert ignore into reviews (cuid,rid,title,rating,useful_count,likers_count,vote_status,useless_count,comments_count,create_time,insert_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())'
        try:
            for i in range(len(item["cuid"])):
                tx.execute(commentSql,(int(item['cuid'][i]),int(item["reviewId"][i]),item["title"][i],item["rating"][i],int(item["useful_count"][i]),int(item["likers_count"][i]),int(item["vote_status"][i]),int(item["useless_count"][i]),int(item["comments_count"][i]),item["create_time"][i]))
                
        except Exception as e:
            logging.error('DBError---->uidList::'+str(item['cuid'][0])+' did not insert into table')
            logging.error(e)