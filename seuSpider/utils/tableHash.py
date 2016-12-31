# -*- coding:utf-8 -*-  
'''
Created on 2016年10月3日

@author: MQ
'''
class thash():
    def __init__(self):
        pass
    
    def uhash(self,uid,num):
        return int(uid)%num
        
        
if __name__ == '__main__':
    u =thash()
    print u.uhash('1244701800')