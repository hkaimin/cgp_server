#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time

def base26(number):
    # 把数字转换成类似 excel 的表格头
    # http://stackoverflow.com/questions/4447550/
    X=lambda n:~n and X(n/26-1)+chr(65+n%26)or''
    return X(number)





def unixtime(reabletime):
    return int(time.mktime(time.strptime(reabletime, '%Y-%m-%d %H:%M:%S')))

def date2time(d):
    return int(time.mktime(d.timetuple()))

def time2date(t):
    return datetime.datetime.fromtimestamp(t)

def time2str(t):
    d = datetime.datetime.fromtimestamp(t)
    return d.strftime('%Y-%m-%d %H:%M:%S')

def timeindex(group):
    # 2013-12-06 17:00:00
    # 0123456789012345679
    sliceIndex = {
        'month': 7,
        'day': 10,
        'hour': 13
    }
    return sliceIndex[group]
