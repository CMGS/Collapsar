#coding:utf8
#
# Author: CMGS
# Created on 2010-8-23
#

import time

from utils import guid
from common import config as _config
from memory import memoryPool as _mPool

class SessionPool(object):
    _sessionIdKey = _config.SESSION_COOKIE_NAME
    _sessionUsrKey = _config.USER_COOKIE_NAME

    """存储Session的地方"""
    def __init__(self, session_store_time = 30):
        """初始化Session池
            @param session_store_time:session存储时间，单位：分钟
        """
        self.session_store_time = session_store_time
    
    def getSessions(self, usr):
        sessions = _mPool.get(usr, None)
        if sessions is not None:
            return sessions
        return None

    def getSessionByCookie(self, cookie):
        """根据Cookie信息找到session"""        
        sessionId = cookie.get(self._sessionIdKey, None)
        usr = cookie.get(self._sessionUsrKey, None)
        if sessionId is None or usr is None:
            return None
        session = self.getSession(usr, sessionId)
        if session is not None:
            session['lastAccessTime'] = time.time()
            self.setSession(usr, sessionId, session)
        return session

    def getSession(self, usr, sid):
        """从池中获取Session"""
        if _mPool.has_key(usr):
            sessions = _mPool.get(usr, None)
            # 清理过期session
#            if sessions is not None:
#                session = sessions.get(sid, None)
#                if(session is not None and self._isTimeOut(session)):
#                    self.removeSession(usr, sid)
#                else:
#                    return session
            if sessions is not None:
                return sessions.get(sid, None)
        return None

    def setSession(self, usr, key, value):
        if self.getSessions(usr) is None:
            sessions = self.createSession(usr)[1]
        else:
            sessions = self.getSessions(usr)
        sessions.update({key: value})
        _mPool.set(usr, sessions)
        return sessions

    def createSession(self, usr):
        """创建一个新的Session"""
        """返回一个元组，第一位为sid第二位为内容"""
        sessionId = self._newSessionId()
        session = {sessionId: {_config.USER_TIME_NAME: time.time()}}
        data = self.getSessions(usr)
        if data is None:
            _mPool.add(usr, session)
            data = self.getSessions(usr)
        else:
            data.update(session)
            _mPool.set(usr, data)
        return sessionId, data

    def removeSession(self, usr, sid):
        """删除Session"""
        """得到的是用户多次登录后的字典"""
        sessions = _mPool.get(usr, None)
        if sessions is not None and sessions.has_key(sid):
            userSessions = sessions[sid]
            del sessions[sid]
            return userSessions
        return None
    
    def delSessions(self, usr):
        return _mPool.delete(usr)

    def _isTimeOut(self, session):
        """判断是否已超时"""
        return time.time() - session['lastAccessTime'] > session['maxInactiveInterval'] * 60
    
    def _newSessionId(self):
        """创建一个新的SessionId"""
        return guid.generate()

sessionPool = SessionPool()

if __name__ == '__main__':
    usr = 'CMGS'
    s = sessionPool
    print 'sid1 :', s.createSession(usr)[0]
    print 'sid2 :', s.createSession(usr)[0]
    sid = s.createSession(usr)[0]
    print 'sid3 :', sid
    print 'set sessions :', s.setSession(usr, 'CMGS', 'God')
    print 'get session :', s.getSession(usr, sid)
    print 'delete session :', s.removeSession(usr, sid)
    print 'delete all :', s.delSessions(usr)
    print 'get delete :', s.getSessions(usr)
