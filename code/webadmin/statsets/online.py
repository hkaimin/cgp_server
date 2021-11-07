#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bson.code import Code
from webadmin.library.utils import unixtime

def _timespan(db, start, end, key_func):
    ''' 分组统计 '''

    condition_doc = {
        'ct': {'$gte': start, '$lte': end}
    }

    initial_doc = {
        'counts': [],
        'pidsList': [],
    }

    reduce_func = Code('''
function(doc, group) {
    if (group.counts.length === 0) { group.start = doc.ct; }
    group.end = doc.ct;
    group.counts.push(doc.pids.length);
    group.pidsList.push(doc.pids);
}
''')

    finalize_func = Code('''
function(group) {
    // 对于 6 个月的数据量，这三个操作花了约 1 秒时间
    group.avg = Math.round(Array.avg(group.counts));
    group.min = Math.min.apply(Math, group.counts);
    group.max = Math.max.apply(Math, group.counts);

    // 而这一个操作花了约 2 秒时间
    var allPids = [];
    group.pidsList.forEach(function(pids) {
        allPids.push.apply(allPids, pids);
    });
    group.uni = Array.unique(allPids).length;

    delete group.pidsList;
    delete group.counts;
}
''')

    rows = db['log_online'].group(
                        key=key_func,
                        condition=condition_doc,
                        initial=initial_doc,
                        reduce=reduce_func,
                        finalize=finalize_func)

    entries = rows
    for entry in entries:
        for key, value in entry.iteritems():
            if key == 'key':
                continue
            entry[key] = int(value)
    return entries

def detail(db, start, end):
    ''' 原始数据 '''

    start = unixtime(start)
    end = unixtime(end)

    criteria = {
        'ct': {'$gte': start, '$lte': end}
    }
    projection = {'_id': 0}
    rows = db['log_online'].find(criteria, projection).sort('ct', 1)

    entries = []
    for row in rows:
        entry = {}
        entry['time'] = row['ct']
        entry['unique'] = len(row['pids'])
        entry['instant'] = row['c']
        entries.append(entry)
    return entries


def minute(db, start, end, minutes):
    ''' 按分统计 '''
    start = unixtime(start)
    end = unixtime(end)
    seconds = minutes * 60
    key_func = Code('''
function(doc) {
    var key = Math.floor((doc.ct - %d)/ %d);
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
    var date = new Date(doc.ct * 1000);
    date.setTime(date.getTime() - date.getTimezoneOffset() * 1000 * 60);
    var key = date.toISOString().replace('T', ' ').slice(0, 7);
    return {key: key};
}
''')
    return _timespan(db, start, end, key_func)
