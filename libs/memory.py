#coding:utf8
#
# Author: CMGS
# Created on 2010-9-3
#

from common import config as _config
from utils.times import getTimes

class MemoryPool(object):
    
    def __init__(self, maxSize):
        self.maxSize = maxSize
        self.count = 0
        self.pool = {}
        self._nodeList = []
        
    def get(self, key, default = None):
        if self.has_key(key):
            return self.pool[key].getValue()
        return default
    
    def set(self, key, value):
        if self.has_key(key):
            self.pool[key].update(value, getTimes())
            # 从索引队列中删除
            self._nodeList.remove(key)
            # 加入到索引队列末尾
            self._nodeList.append(key)
            return True
        return False
    
    def add(self, key, value):
        if self.has_key(key):
            return False
        if self.count + 1 <= self.maxSize:
            cTime = getTimes()
            self.pool[key] = PoolNode(value, cTime)
            # 增加到索引队列中
            self._nodeList.append(key)
            self.count += 1
            return True
        else:
            dKey = self._nodeList[0]
            self.delete(dKey)
            self.add(key, value)
            return True

    def delete(self, key):
        if self.has_key(key):
            r = self.pool.pop(key)
            # 从索引队列中删除
            self._nodeList.remove(key)
            self.count -= 1
            return r.getValue()
        return None
    
    def getMany(self, keys = None):
        if isinstance(keys, list) is False:
            keys = self.pool.keys()
        return [self.get(k) for k in keys]
        
    def has_key(self, key):
        return self.pool.has_key(key)
    
    def getIndex(self):
        return self._nodeList

class PoolNode(object):
    _value = None
    _ctime = 0

    def __init__(self, _v = None, _c = None):
        self.update(_v, _c)

    def getValue(self):
        return self._value
    
    def setValue(self, _v):
        self._value = _v

    def update(self, _v = None, _b = None):
        self._value = _v or self._value
        self._ctime = _b or self._ctime

memoryPool = MemoryPool(_config.MEMORY_POOL_SIZE)

if __name__ == '__main__':
    for i in range(1, 12):
        memoryPool.add(str(i), i*100)
    print memoryPool.getIndex()
    memoryPool.set('2', 19)
    memoryPool.add('12', 12)
    print memoryPool.getIndex()
