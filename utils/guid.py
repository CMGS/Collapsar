#!/usr/bin/env python
import math
import socket
import random
import sys
import time
import threading

#############################
###     global module variables

#Makes a hex IP from a decimal dot-separated ip (eg: 127.0.0.1)
make_hexip = lambda ip: ''.join(["%04x" % long(i) for i in ip.split('.')]) # leave space for ip v6 (65K in each sub)
    
MAX_COUNTER = 0xfffffffe
counter = 0L
firstcounter = MAX_COUNTER
lasttime = 0
ip = ''
lock = threading.RLock()
try:    # only need to get the IP addresss once
    ip = socket.getaddrinfo(socket.gethostname(),0)[-1][-1][0]
    hexip = make_hexip(ip)
except: # if we don't have an ip, default to someting in the 10.x.x.x private range
    ip = '10'
    rand = random.Random()
    for i in range(3):
        ip += '.' + str(rand.randrange(1, 0xffff))    # might as well use IPv6 range if we're making it up
    hexip = make_hexip(ip)

    
#################################
###     Public module functions

def generate(ip=None):
    '''Generates a new guid.    A guid is unique in space and time because it combines
         the machine IP with the current time in milliseconds.    Be careful about sending in
         a specified IP address because the ip makes it unique in space.    You could send in
         the same IP address that is created on another machine.
    '''
    global counter, firstcounter, lasttime
    lock.acquire() # can't generate two guids at the same time
    try:
        parts = []

        # do we need to wait for the next millisecond (are we out of counters?)
        now = long(time.time() * 1000)
        while lasttime == now and counter == firstcounter: 
            time.sleep(.01)
            now = long(time.time() * 1000)

        # time part
        parts.append("%016x" % now)

        # counter part
        if lasttime != now:    # time to start counter over since we have a different millisecond
            firstcounter = long(random.uniform(1, MAX_COUNTER))    # start at random position
            counter = firstcounter
        counter += 1
        if counter > MAX_COUNTER:
            counter = 0
        lasttime = now
        parts.append("%08x" % (counter)) 

        # ip part
        parts.append(hexip)

        # put them all together
        return ''.join(parts)
    finally:
        lock.release()
        

def extract_time(guid):
    '''Extracts the time portion out of the guid and returns the 
         number of seconds since the epoch as a float'''
    return float(long(guid[0:16], 16)) / 1000.0


def extract_counter(guid):
    '''Extracts the counter from the guid (returns the bits in decimal)'''
    return int(guid[16:24], 16)


def extract_ip(guid):
    '''Extracts the ip portion out of the guid and returns it
         as a string like 10.10.10.10'''
    # there's probably a more elegant way to do this
    thisip = []
    for index in range(24, 40, 4):
        thisip.append(str(int(guid[index: index + 4], 16)))
    return '.'.join(thisip)
