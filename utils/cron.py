#coding:utf8
#
# Author: CMGS
# Created on 2010-9-20
#

from gevent.core import timer

class PeriodicCallback(object):
    
    def __init__(self, callback, callback_time, start = True, *arg, **argv):
        self.callback = callback
        self.callback_time = callback_time
        self._running = True
        if start:
            self.start(*arg, **argv)

    def start(self, *arg, **argv):
        timer(self.callback_time, self._run, *arg, **argv)

    def stop(self):
        self._running = False

    def _run(self, *arg, **argv):
        if not self._running: return
        try:
            self.callback(*arg, **argv)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception, e:
            # 发生异常的考虑
            print e
        self.start(*arg, **argv)
