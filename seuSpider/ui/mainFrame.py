# -*- coding:utf-8 -*-  
'''
Created on 2017年1月9日

@author: MQ
'''
import wx
import scrapy.cmdline
from seuSpider.utils.dbManager2 import dbManager2

class MainWindow(wx.Frame):
    def __init__(self, parent, myid, title = u"\u722c\u866b\u96c6\u6210\u5e73\u53f0\u0056\u0030\u002e\u0031"):
        wx.Frame.__init__(self, parent, -1, title, size = (500, 800),
              style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.panel = wx.Panel(self, -1)
#         self.control = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE)
        #建立数据库按钮
        self.dbBt = wx.Button(self.panel, -1, u"\u5efa\u7acb\u6570\u636e\u5e93\u8868", pos=(20, 100),size =(150,40),style=0,name='start_button')
        self.Bind(wx.EVT_BUTTON, self.OndbBtClick, self.dbBt)
        self.dbBt.SetDefault()
        
        spidersLs = [u'\u8c46\u74e3\u722c\u866b',u'\u65b0\u6d6a\u722c\u866b']
        self.spidersRadio = wx.RadioBox(self.panel,-1,u"\u722c\u866b",(20,10),wx.DefaultSize,spidersLs,2,wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.OnRadioBox, self.spidersRadio)
        
        #填写电影id文本框
        self.filmIDText=wx.TextCtrl(self.panel,-1,'',pos=(200,20),size=(175,-1),style=wx.TE_CENTER)
        #添加电影Id按钮
        self.addFilmIdBt = wx.Button(self.panel, -1, u"\u6dfb\u52a0", pos=(385, 20),size =(65,25),style=0,name='start_button')
        self.Bind(wx.EVT_BUTTON, self.onAddFilmBtClick, self.addFilmIdBt)

        #添加完成的电影id列表（待选）
        self.fileIdsCheckListBox = wx.CheckListBox(self.panel,-1,pos=(200,60),size = (250,80),choices=[],style=0,name='xxxx')
#         sinaSpiderLs = ['sinaUser','sinaFRelation']
#         doubanSpiderLs = ['doubanUser','doubanFRelation','doubanFilmComment','doubanFilmReview']
#         self.sinaRadioBox = wx.RadioBox(self.panel,-1,"sina Spiders",(10,80),wx.DefaultSize,sinaSpiderLs,2,wx.RA_SPECIFY_COLS)
#         self.doubanRadioBox =wx.RadioBox(self.panel,-1,"douban Spiders",(10,80),wx.DefaultSize,doubanSpiderLs,2,wx.RA_SPECIFY_COLS)
#             
#         self.doubanRadioBox.Hide()
        self.showDouBanPanel()

    def OnRadioBox(self,event):
        if self.spidersRadio.GetSelection() == 1:
            '''radio选择新浪爬虫面板安排
            '''
            self.showDouBanPanel(0)
#             self.sinaRadioBox.Show()
#             self.doubanRadioBox.Hide()
        if self.spidersRadio.GetSelection() == 0:
            '''radio选择豆瓣爬虫面板安排
            '''
#             self.sinaRadioBox.Hide()
#             self.doubanRadioBox.Show()
            self.showDouBanPanel(1)
    def OndbBtClick(self,event):
        self.__db = dbManager2(dbname="douban")
        
        filmLs = self.fileIdsCheckListBox.GetCheckedStrings()
        for i in filmLs:
            self.__db.execute("CREATE TABLE `comments_"+str(i)+"` (\
                                `cuid`  bigint(20) NOT NULL COMMENT '发表comment的用户ID' ,\
                                `commentId`  bigint(20) NOT NULL COMMENT 'comment编号' ,\
                                `comment`  text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'comment内容' ,\
                                `rating`  varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '评分' ,\
                                `vote_count`  bigint(20) NOT NULL DEFAULT '-1' COMMENT '投票数' ,\
                                `create_time`  datetime NOT NULL COMMENT '发布时间' ,\
                                `insert_time`  datetime NOT NULL COMMENT '此条记录发布时间' ,\
                                PRIMARY KEY (`commentId`)\
                                )\
                                ENGINE=InnoDB\
                                DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci\
                                ROW_FORMAT=DYNAMIC\
                                ;")
            print i
        
        self.dbBt.SetLabel(u'\u6570\u636e\u5e93\u5efa\u7acb\u5b8c\u6210')
        #self.dbBt.Enabled = False
        scrapy.cmdline.execute(argv=['scrapy', 'crawl','spider_main'])
    def onAddFilmBtClick(self,event):
#         print self.filmIDText.GetValue()
        self.fileIdsCheckListBox.Append(str(self.filmIDText.GetValue()))
    def OnReviewBtClick(self,event):
        self.reviewBt.SetLabel(u"\u7535\u5f71\u957f\u8bc4\u4fe1\u606f(\u7ed3\u675f)")
        self.reviewGauge.SetValue(70)
        self.reviewBt.Enabled = False
        
    def OnUserBtClick(self,event):
        self.userBt.SetLabel(u"\u7535\u5f71\u957f\u8bc4\u4fe1\u606f(\u7ed3\u675f)")
        self.userGauge.SetValue(50)
        self.userBt.Enabled = False
        
    def showDouBanPanel(self,showFlag=1):
        if showFlag == 0:
            self.reviewBt.Shown = False
            self.reviewGauge.Shown = False
            self.userBt.Shown = False
            self.userGauge.Shown = False
        else:
            #电影长评信息爬虫按钮
            self.reviewBt = wx.Button(self.panel, -1, u"\u7535\u5f71\u957f\u8bc4\u4fe1\u606f(\u5f00\u59cb)", pos=(20, 160),size =(150,40),style=0,name='start_button')
            self.Bind(wx.EVT_BUTTON, self.OnReviewBtClick, self.reviewBt)
            #电影长评进度条
            self.reviewGauge= wx.Gauge(self.panel,-1,100,pos=(200,160),size=(250,40),style=wx.GA_PROGRESSBAR)
    
            #用户信息爬虫按钮
            self.userBt = wx.Button(self.panel, -1, u"\u7535\u5f71\u957f\u8bc4\u4fe1\u606f(\u5f00\u59cb)", pos=(20, 220),size =(150,40),style=0,name='start_button')
            self.Bind(wx.EVT_BUTTON, self.OnUserBtClick, self.userBt)
            #进度条
            self.userGauge= wx.Gauge(self.panel,-1,100,pos=(200,220),size=(250,40),style=wx.GA_PROGRESSBAR)  


class SpiderApp(wx.App):
    def OnInit(self):
        frame = MainWindow(None, -1)
        self.SetTopWindow(frame)
        frame.Show()
        return True
    
    def OnExit(self):
        print "onExit..."
        
if __name__ == '__main__':
    app = SpiderApp()
    app.MainLoop()