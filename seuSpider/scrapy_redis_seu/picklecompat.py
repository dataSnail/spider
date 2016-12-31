# -*- coding:utf-8 -*-  
'''
Created on 2016年10月18日

@author: MQ
'''
"""A pickle wrapper module with protocol=-1 by default."""

try:
    import cPickle as pickle  # PY2
except ImportError:
    import pickle


def loads(s):
    return pickle.loads(s)


def dumps(obj):
    return pickle.dumps(obj, protocol=-1)