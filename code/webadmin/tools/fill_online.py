#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import time
from random import randint, sample
from pymongo import MongoClient

def fill(db, more=False):
    cn = db['log_online']
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
    all_pids = range(1, 1000)
    number = 0 
    for i in xrange(rows_count):
        ct = start + 300 * i;
        if number > 30:
            number += randint(-(number / 3), 3)
        else:
            number += randint(-2, 3)

        # 为了方便验算平均值，只使用偶数
        if number % 2 != 0:
            number += 1

        _id = i + 1
        if (number < 0):
            number = 0;
        # 瞬间在线
        c = number - randint(0, 5)
        if c < 0:
            c = 0
        # 时间段内登录过
        pids = sample(all_pids, number)

        doc = dict(_id=_id, c=c, ct=ct, pids=pids)
        cn.save(doc)

def main():
    db = MongoClient('mongodb://127.0.0.1/rich9_log').get_default_database()
    more = len(sys.argv) > 1
    fill(db, more)

if __name__ == '__main__':
    main()

