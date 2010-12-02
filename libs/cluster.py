#coding:utf8
#
# Author: CMGS
# Created on 2010-9-3
#

from common import config as _config
from rpc import RPC as _RPC

class Server(object):
    
    def __init__(self, apis, ip):
        self.apis = apis
        self.ip = ip
        self._mixin()
        
    def _mixin(self):
        for api in self.apis:
            self.__dict__.update({api: _RPC(self.ip, api)})

class Cluster(list):
    
    def __init__(self, servers, apis):
        for ip in servers:
            self.append(Server(apis, ip))

cluster = Cluster(_config.CLUSTER, _config.APIS)
