#!/usr/bin/env python
# -*- coding: utf-8 -*-
from webadmin.define.constant import *

def level(db):
    ''' 统计玩家等级 '''

    group_phase  = {'$group': {'_id': '$level', 'count': {'$sum': 1}}}
    sort_phase  = {'$sort': {'_id': 1}}
    rows = db['player'].aggregate([group_phase, sort_phase])['result']

    entries = []
    for row in rows:
        entry = {}
        entry['level'] = row['_id']
        entry['count'] = row['count']
        entries.append(entry)
    return entries


def reg(db, start, end, logtype):
    """ 统计当前注册人数"""
    cond_dict = {'t': logtype, 'ct': MDBOpe().interval(start, end)}
    cond_dict = {'t': logtype}
    cond_dict = {}
    entries = db['log_info'].find(cond_dict, {'_id': 0,
                                              'ct': 0,
                                              't': 0,
                                              'login': 0,
                                              'ip': 0,
                                              'hid': 0})
    return entries

def rrt(db, ct, logtype, gid, svrid):
    """ 获取存留率 """
    cond_dict = {'ct': ct, 'rtype': logtype, 'gid': gid, 'svrid': svrid}
    entries = db['log_retention'].find(cond_dict)
    return entries

