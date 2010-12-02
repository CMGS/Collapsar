#coding:utf8
#
# Author: CMGS
# Created on 2010-8-26
#

from threading import local
from utils.times import getTimes
from utils.times import makeTimes

class CachePool(local):
    _cache = {}
    # 默认超时 60秒
    _defaultTimeOut = 600

    def __init__(self, timeout = 600):
        self._defaultTimeOut = timeout

    def get(self, key):
        if self.delete(key):
            return self._cache[key].getValue()
        return None

    def set(self, key, value, timeout = None):
        if self.delete(key):
            self._cache[key].update(value, timeout or self._defaultTimeOut, getTimes())
            return True

        self.add(key, value, timeout)
        return True

    def add(self, key, value, timeout = None):
        if self._cache.has_key(key):
            return False

        self._cache[key] = CacheNode(value, timeout or self._defaultTimeOut, getTimes())
        return True

    def delete(self, key):
        if self._cache.has_key(key) and (self._cache[key].isInvaild() is not True):
            self._cache.pop(key)
            return False

        return self._cache.has_key(key)
        
    def getTimeOut(self, key):
        if self.delete(key):
            return makeTimes(self._cache[key].getTimeOut())
        return None

    def get_many(self, keys):
        ret = {}
        for k in keys:
            val = self.get(k)
            if self.delete(k):
                ret[k] = val.getValue()
        
        return ret

    def has_key(self, key):
        return self._cache.has_key(key)

class CacheNode(object):
    _value = None
    _timeout = 0
    _btime = 0

    def __init__(self, _v = None, _t = None, _b = None):
        self.update(_v, _t, _b)

    def isInvaild(self):
        now  = getTimes()
        if now > self._btime + self._timeout:
            return False
        
        return True

    def getValue(self):
        return self._value
    
    def setValue(self, _v):
        self._value = _v

    def getTimeOut(self):
        return self._btime + self._timeout

    def setTimeOut(self, _t):
        self._timeout = _t

    def update(self, _v = None, _t = None, _b = None):
        self._value = _v or self._value
        self._timeout = _t or self._timeout
        self._btime = _b or self._btime

cachePool = CachePool()
