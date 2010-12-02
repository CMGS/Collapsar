#coding:utf8
#
# Author: CMGS
# Created on 2010-8-24
#

import gevent
from gevent import Greenlet

from utils import feedparser as _feed
from common import config as _conf

class Crawler(Greenlet):
    
    def __init__(self, url, timeout = _conf.CRAWLER_TIMEOUT, etag = None, modified = None):
        Greenlet.__init__(self)
        self.url = url
        self.etag = etag
        self.modified = modified
        
    def _run(self):        
        return _feed.parse(self.url, etag = self.etag, modified = self.modified)

    def __str__(self):
        return 'Crawl %s' % self.url
    
def show(i):
    rss = i.value
    for x in rss['entries']:
        print x['title'] 
    
if __name__ == '__main__':
    url = u'http://feeds.feedburner.com/CMGS'
    c = Crawler(url)
    c.rawlink(show)
    c.start()
    print 1
    gevent.sleep(1)
