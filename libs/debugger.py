#coding:utf8
#
# Author: CMGS
# Created on 2010-10-9
#

import traceback
from common import config as _config

class Debugger(object):
    @classmethod
    def out(cls, c):
        if _config.DEBUG:
            print c
    
    @classmethod
    def exc(cls, e):
        if _config.DEBUG:
            print traceback.format_exc()
    
if __name__ == '__main__':
    Debugger.out('xxoo')
    try:
        1/0
    except Exception, e:
        Debugger.exc(e)
