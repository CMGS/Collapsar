#coding:utf8
#
# Author: CMGS
# Created on 2010-9-3
#

import json
import urllib2
from debugger import Debugger as _debugger
from common import config as _config
from common import defcode as _defcode

class RPC(object):

    def post(self, url, data, header, timeout = _config.SOCKET_TIMEOUT):
        try:
            req = urllib2.Request(url, data, header)
            res = urllib2.urlopen(req, timeout = timeout)
            ret = res.read()
            return _defcode.RPC_POST_OK, ret
        except Exception, e:
            _debugger.exc(e)
            return _defcode.RPC_POST_FAILED, e
    
    def get(self, url, timeout = _config.SOCKET_TIMEOUT):
        try:
            res = urllib2.urlopen(url, timeout = timeout)
            ret = res.read()
            return _defcode.RPC_GET_OK, ret
        except Exception, e:
            _debugger.exc(e)
            return _defcode.RPC_GET_FAILED, e
    
    def toJson(self, data):
        try:
            return json.dumps(data)
        except Exception, e:
            return None
    
    def loadJson(self, data):
        try:
            return json.loads(data)
        except Exception, e:
            return None
rpc = RPC()
