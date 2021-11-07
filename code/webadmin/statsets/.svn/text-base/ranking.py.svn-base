#!/usr/bin/env python
# -*- coding: utf-8 -*-

def level(db, limit):
    ''' 统计玩家等级排行 '''

    sort_doc = [['level', -1], ['tNew', -1]]
    rows = db['player'].find().sort(sort_doc).limit(limit)

    entries = []
    for i, row in enumerate(rows):
        entry = {}
        entry['pid'] = row['_id']
        entry['name'] = row['name']
        entry['level'] = row['level']
        entry['register_time'] = row['tNew']
        entries.append(entry)
    return entries
