#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bson.code import Code
from webadmin.library.utils import unixtime

def _timespan(db, start, end, key_func):
    ''' 分组统计 '''

    condition_doc = {
        't': 2, # 登出类型
        'ct': {'$gte': start, '$lte': end}
    }

    initial_doc = {
        'count': 0,
        'items': [],
        'sum': 0,
    }

    reduce_func = Code('''
function(cur, result) {
    if (result.count === 0) {
        result.start = cur.ct;
    }
    result.end = cur.ct;

    var length = cur.ct - cur.login;
    result.count += 1;
    result.items.push(length);
    result.sum += length;
}
''')

    finalize_func = Code('''
function(result) {
    result.avg = Math.round(result.sum / result.count);
    result.min = Math.min.apply(Math, result.items);
    result.max = Math.max.apply(Math, result.items);
    delete result.items;
}
''')

    rows = db['log_info'].group(
                        key=key_func,
                        condition=condition_doc,
                        initial=initial_doc,
                        reduce=reduce_func,
                        finalize=finalize_func)

    entries = rows
    return entries

def day(db, start, end):
    ''' 按天统计 '''

    start = unixtime(start)
    end = unixtime(end)
    key_func = Code('''
function(doc) {
    var date = new Date(doc.ct * 1000);
    date.setTime(date.getTime() - date.getTimezoneOffset() * 1000 * 60);
    var key = date.toISOString().replace('T', ' ').slice(0, 10);
    return {key: key};
}
''')
    return _timespan(db, start, end, key_func)

def retain(db, start, end, days):
    ''' 留存率 '''

    start = unixtime(start)
    end = unixtime(end)
    seconds = 3600 * 24 * days
    key_func = Code('''
function(doc) {
    var key = Math.floor((doc.login - %d) / %d);
    return {key: key};
}
''' % (start, seconds))

    condition_doc = {
        't': 2, # 登出类型
        'login': {'$gte': start, '$lte': end}
    }

    initial_doc = {
        'pids': [],
    }

    reduce_func = Code('''
function(cur, result) {
    if (result.pids.length === 0) {
        result.start = cur.login;
    }
    result.end = cur.login;

    // 人次
    result.pids.push(cur.p);
}
''')

    rows = db['log_info'].group(
                    key=key_func,
                    condition=condition_doc,
                    initial=initial_doc,
                    reduce=reduce_func)

    entries = []
    for i, row in enumerate(rows):
        entry = {}

        # 登录人次
        entry['count'] = len(row['pids'])

        # 唯一账户数
        row['uni_pids'] = set(row['pids'])
        entry['uni'] = len(row['uni_pids'])

        # 第一条记录无比较，留存率当 0 处理
        if i == 0:
            entry['retain'] = 0
            entry['rate'] = 0
        else:
            last_row = rows[i - 1]
            last_entry = entries[i - 1]

            retain_pids = last_row['uni_pids'] & row['uni_pids']
            entry['retain'] = len(retain_pids)
            entry['rate'] = entry['retain'] * 100 / last_entry['uni']

        entry['start'] = row['start']
        entry['end'] = row['end']
        entries.append(entry)

    return entries
