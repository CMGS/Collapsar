#coding:utf8
#
# Author: CMGS
# Created on 2010-8-23
#
'''
mysql 数据库连接池
'''

__all__ = [
    'pool',
    'escape',
]

import _mysql
import common.config as _config

from _mysql_exceptions import IntegrityError
from threading import local

def escape(sql):
    '''这里假定连接数据库都是使用utf8的。'''
    if sql is None:
        return ''
    if isinstance(sql, unicode):
        sql = sql.encode('utf8')
    return _mysql.escape_string(sql)

class SqlPool(local):
    '''全局线程变量，继承于local类'''
    KEY_ERROR = -2
    RET_TUPLE = 0
    RET_DICT_ROW_FOR_KEY = 1
    RET_DICT_TABLE_ROW_FOR_KEY = 2
    def __init__(self, db, host, user, passwd, port = 3306):
        self._db = db
        self._host = host
        self._user = user
        self._passwd = passwd
        self._port = int(port)
        self._connection = None
        
    class SqlConn():
        '''这是一个SqlPool的嵌套类'''
        def __init__(self, conn, ownner):
            '''应该由SqlPool的getConn方法去初始化本类'''
            self.conn = conn
            self.ownner = ownner

        def __del__(self):
            self.close()

        def execute(self, sqlCmd):
            '''@return: 成功返回影响行数,失败返回 小于零的整数.-2为主键冲突,其它负数未定义错误类型.'''
            try:
                self.conn.query(sqlCmd)
                return self.affectRows()
            except IntegrityError:
                return (SqlPool.KEY_ERROR) #发生主键冲突
            except Exception, e:
                print sqlCmd
                print e
                raise e # SQL 语句执行失败就拖异常,程序必需处理,以免数据异常

        def query(self, sqlCmd, how = 0):
            '''执行一条查询的SQL语句，返回查询结果,也可以马上调用result方法对能取得. 每次的query对应一次的result.'''
            assert (sqlCmd).lower().startswith("select") == True or (sqlCmd).lower().startswith("show") == True, 'must readonly query.'
            try:
                self.conn.query(sqlCmd)
                return self.result(how)
            except Exception, e:
                print e
                print sqlCmd
                raise e # SQL 语句执行失败就拖异常,程序必需处理,以免数据异常

        def result(self, how = 0):
            '''@param how:
                0 -- tuples (default), RET_TUPLE
                1 -- dictionaries, key=column or table.column if duplicated
                2 -- dictionaries, key=table.column.'''
            res = self.conn.store_result()
            if res:
                return res.fetch_row(res.num_rows(), how)
            else:
                return ()

        def affectRows(self):
            '''查看最后一次query影响几行数据.'''
            r = self.conn.affected_rows()
            #TODO 这个值与驱动、系统、硬件CPU位数都可能有关
            if r == 0xFFFFFFFFFFFFFFFF: #64位的-1
                return 0
            return r

        def close(self):
            '''关闭连接'''
            self.ownner.close(self)
            self.conn = None

    def _valid_connection(self):
        if self._connection is not None:
            try:
                self._connection.ping()
                return True
            except:
                self._connection.close()
                self._connection = None
        return False

    def getConn(self):
        '''获取连接'''
        if not self._valid_connection():
            self._connection = _mysql.connect(
                db = self._db,
                host = self._host,
                user = self._user,
                passwd = self._passwd,
                port = self._port)
            self._connection.set_character_set('utf8')
        return SqlPool.SqlConn(self._connection, self)

    def close(self, conn):
        '''关闭连接'''
        #不做任何事情
        pass

    def execute(self, sqlCmd):
        '''执行语句, 返回影响行数'''
        sqlConn = self.getConn()
        retCode = sqlConn.execute(sqlCmd)
        sqlConn.close()
        return retCode

    def executeReturnInsertId(self, sqlCmd):
        '''执行语句, 返回影响行数及LAST_INSERT_ID'''
        sqlConn = self.getConn()
        insertResult = sqlConn.execute(sqlCmd)
        if insertResult < 1:
            return (int(insertResult), 0)
        insertId = sqlConn.query('SELECT LAST_INSERT_ID()')[0][0]
        sqlConn.close()
        return (int(insertResult), int(insertId))

    def query(self, sqlCmd, how = 0):
        '''执行语句，返回查询结果'''
        sqlConn = self.getConn()
        retData = sqlConn.query(sqlCmd, how)
        sqlConn.close()
        return retData

sqlPool = SqlPool(
    db = _config.MYSQL_NAME,
    host = _config.MYSQL_HOST,
    user = _config.MYSQL_USER,
    passwd = _config.MYSQL_PASSWORD,
    port = _config.MYSQL_PORT
)
