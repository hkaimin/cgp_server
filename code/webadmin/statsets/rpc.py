#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bson.code import Code
from webadmin.library.utils import unixtime

def rpc(db, start, end, type):
    ''' 统计 RPC '''

    start = unixtime(start)
    end = unixtime(end)

    condition_doc = {
        'ct': {'$gte': start, '$lte': end},
        't': type,
    }

    initial_doc = {
        'index': 0,
        'total': 0,
        'use': 0,
        'err': 0,
    }

    key_func = Code('''
function(doc) {
    return {key: doc.func};
}
''')

    reduce_func = Code('''
function(doc, group) {
    if (group.index === 0) { group.start = doc.ct; }
    group.end = doc.ct;
    group.t = doc.t;
    group.total += doc.total;
    group.use += doc.use;
    group.err += doc.err;
}
''')

    finalize_func = Code('''
function(group) {
    delete group.index;
}
''')

    rows = db['log_rpc'].group(
                        key=key_func,
                        condition=condition_doc,
                        initial=initial_doc,
                        reduce=reduce_func,
                        finalize=finalize_func)

    # 默认按总耗时排序
    entries = sorted(rows, key=lambda r: r['use'])
    return entries
