#coding:utf8
#
# Author: CMGS
# Created on 2010-3-26
#

import sys
import traceback

from debugger import Debugger as _debugger
from common.config import DEBUG

def getExceptInfo(e):
    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
    infoList = traceback.format_exception(exceptionType, exceptionValue, exceptionTraceback)
    return ''.join(infoList)

class EventCenter(object):

    def __init__(self):
        self.__ecEventMapping = {}
        self.__ecCather = []

    def catch(self, callback):
        self.__ecCather.append(callback)
    
    def attach(self, e, callback):
        _debugger.out('%s %s' % (e, callback))
        if not self.__ecEventMapping.has_key(e):
            self.__ecEventMapping[e] = [callback]
        else:
            self.__ecEventMapping[e].append(callback)

    def dispatch(self, e, **args):
        for c in self.__ecCather:
            try:
                c(e, **args)
            #pragma: no cover 1    
            except Exception,e:
                _debugger.out(e)
                if DEBUG:raise

        callbacks = self.__ecEventMapping.get(e, None)
        if callbacks is None:
            return False
        for callback in self.__ecEventMapping[e]:
            try:
                callback(e, **args)
            #pragma: no cover 1
            except Exception, e:
                _debugger.out(e)
                if DEBUG:raise
            
        return True

ec = EventCenter()
