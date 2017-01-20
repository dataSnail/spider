# -*- coding:utf-8 -*-  
'''
Created on 2017年1月9日

@author: MQ
'''
import wx
import scrapy.cmdline

class MainWindow(wx.Frame):
    def __init__(self, parent, myid, title = u"\u722c\u866b\u96c6\u6210\u5e73\u53f0\u0056\u0030\u002e\u0031"):
        wx.Frame.__init__(self, parent, -1, title, size = (500, 800),
              style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.panel = wx.Panel(self, -1)
#         self.control = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE)
        self.button = wx.Button(self.panel, -1, "Start", pos=(310, 20),size =(150,40),style=0,name='start_button')
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()
        
        spidersLs = ['SINA','DOUBAN']
        self.spidersRadio = wx.RadioBox(self.panel,-1,"Spiders",(10,10),wx.DefaultSize,spidersLs,2,wx.RA_SPECIFY_COLS)
        
        self.Bind(wx.EVT_RADIOBOX, self.OnRadioBox, self.spidersRadio)

        sinaSpiderLs = ['sinaUser','sinaFRelation']
        doubanSpiderLs = ['doubanUser','doubanFRelation','doubanFilmComment','doubanFilmReview']
        self.sinaRadioBox = wx.RadioBox(self.panel,-1,"sina Spiders",(10,80),wx.DefaultSize,sinaSpiderLs,2,wx.RA_SPECIFY_COLS)
        self.doubanRadioBox =wx.RadioBox(self.panel,-1,"douban Spiders",(10,80),wx.DefaultSize,doubanSpiderLs,2,wx.RA_SPECIFY_COLS)
            
        self.doubanRadioBox.Hide()


    def OnRadioBox(self,event):
        if self.spidersRadio.GetSelection() == 0:
            self.sinaRadioBox.Show()
            self.doubanRadioBox.Hide()
        if self.spidersRadio.GetSelection() == 1:
            self.sinaRadioBox.Hide()
            self.doubanRadioBox.Show()
    
    def OnClick(self,event):
        self.button.SetLabel('Stop')
        scrapy.cmdline.execute(argv=['scrapy', 'crawl','spider_main'])
        

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