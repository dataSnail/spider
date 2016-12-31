# -*- coding:utf-8 -*-  
'''
Created on 2016年10月10日

@author: MQ
'''
import sys
import platform

class daemon():
    def __init__(self,processName,time):
        self.system = platform.system()
        #守护的进程名称
        self.processName = processName
        #检查间隔时间
        self.time = time
    def process_is_running(self):
        #判断系统类型
        if self.system == 'Windows':
            pass
            
        if self.system == 'Linux':
            pass
    
    def restart_process(self):
        pass
    



if __name__ == '__main__':
    print '-----------------daemon start-----------------'
