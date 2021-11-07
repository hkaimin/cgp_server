#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import time
from random import randint
from pymongo import MongoClient

def fill(db, more):
    cn = db['player']
    cn.drop()

    a_day_seconds = 60 * 60 * 24

    # 从凌晨开始
    base = int(time())
    base = base - (base % a_day_seconds) - 8 * 3600
    if more:
        start = base - a_day_seconds * 31 * 7
        end = base + a_day_seconds * 31 * 1
    else:
        start = base - a_day_seconds * 3
        end = base

    # 每 5 分钟一组
    rows_count = (end - start) / (5 * 60)

    # 随机塞数据
    for i in xrange(rows_count):
        _id = i + 1
        # 让注册时间随机
        tNew = start + 300 * i + randint(-300, 300);
        name = '玩家%d' % i
        level = randint(0, i % 60)
        doc = dict(_id=_id, tNew=tNew, level=level, name=name)
        cn.save(doc)

def main():
    db = MongoClient('mongodb://127.0.0.1/rich9').get_default_database()
    more = len(sys.argv) > 1
    fill(db, more)

if __name__ == '__main__':
    main()

