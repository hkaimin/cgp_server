#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import time
from random import randint
from pymongo import MongoClient

def fill(db, more=False):
    cn = db['log_info']
    cn.drop()

    a_day_seconds = 60 * 60 * 24

    # 从凌晨开始
    base = int(time())
    base = base - (base % a_day_seconds) - 8 * 3600

    if more:
        start = base - a_day_seconds * 31 * 3
        end = base
    else:
        start = base - a_day_seconds * 3
        end = base

    # 每 5 分钟一组
    rows_count = (end - start) / (5 * 60)

    # 随机塞数据
    for i in xrange(rows_count):
        _id = i + 1
        ct = start + 300 * i;
        t = 2 # 登出
        p = randint(1, 300)
        login = ct - randint(0, 3600)
        doc = dict(_id=_id, ip='', t=t, p=p, ct=ct, login=login)
        cn.save(doc)

def main():
    db = MongoClient('mongodb://127.0.0.1/rich9_log').get_default_database()
    more = len(sys.argv) > 1
    fill(db, more)

if __name__ == '__main__':
    main()

