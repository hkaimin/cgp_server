#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bson.code import Code
from webadmin.library.utils import unixtime

def _timespan(db, start, end, key_func):
    ''' 分组统计 '''

    condition_doc = {
        'tNew': {'$gte': start, '$lte': end}
    }

    initial_doc = {
        'summation': 0,
    }

    reduce_func = Code('''
function(cur, group) {
    if (group.summation === 0) {
        group.start = cur.tNew;
    }
    group.end = cur.tNew;
    group.summation += 1;
}
''')

    rows = db['player'].group(
                    key=key_func,
                    condition=condition_doc,
                    initial=initial_doc,
                    reduce=reduce_func)

    entries = rows
    return entries

def minute(db, start, end, minutes):
    ''' 按分统计 '''

    start = unixtime(start)
    end = unixtime(end)
    seconds = minutes * 60
    key_func = Code('''
function(doc) {
    var key = Math.floor((doc.tNew  - %d)/ %d);
    return {key: key};
}
''' % (start, seconds))
    return _timespan(db, start, end, key_func)

def month(db, start, end):
    ''' 按月统计 '''

    start = unixtime(start)
    end = unixtime(end)
    key_func = Code('''
function(doc) {
    var date = new Date(doc.tNew * 1000);
    date.setTime(date.getTime() - date.getTimezoneOffset() * 1000 * 60);
    var key = date.toISOString().replace('T', ' ').slice(0, 7);
    return {key: key};
}
''')
    return _timespan(db, start, end, key_func)
