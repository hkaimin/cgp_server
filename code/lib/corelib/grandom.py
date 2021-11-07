#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import bisect
from random import choice, randint


def rom(*args):
    """ rom((<count>,<rate>), (1,10), (2,25)) """
    rr = RandomRegion(args)
    return rr()


def roms(*args):
    """ roms(([<int>|<str>],<rate>), ...)
     (1,10), (2,25)
     ('ran(1,10), ran(2,6)', 10), ('ran(10,20), ran(20,30)', 25)
    """
    rr = RandomRegion(args)
    v = rr()
    if isinstance(v, (int, float,)):
        return v
    return eval(v, globals())


def ran(start, end):
    return random.randint(start, end)


def ran_bool(rate):
    """
    爆击率等倍率开关有关的地方使用
    rate: 10%时， rate = 10, 例子：if ran_bool(10): xxx
    如：
        暴击率80%,就是百分之80的机会暴击
    """
    if rate >= 100:
        return True
    elif rate <= 0:
        return False
    ran = random.uniform(0, 100)
    return ran <= rate


class RandomRegion(object):
    """ 概率运算,regions是字典或列表([(k,v),...]), 每一个value都代表一个概率 """
    __slots__ = ('sum', 'items', 'rates', 'values')
    def __init__(self, regions):
        self.sum = 0
        if isinstance(regions, (str, unicode)): #<rid>:rate|<rid>:rate|...
            items = map(lambda i: tuple(map(int, i.strip().split(':'))), regions.split('|'))
        elif hasattr(regions, 'iteritems'):
            items = [(k, v) for k,v in regions.iteritems()]
        else:
            items = list(regions)
        items.sort()
        self.items = items
        self.values = None
        self.rates = []
        for item in items:
            self.sum += item[1]
            self.rates.append(self.sum)

    def random(self):
        """ 随机取值 """
        ran_num = random.randint(0, self.sum)
        i = bisect.bisect_left(self.rates, ran_num)
        return self.items[i][0]

    def randoms(self, count):
        """ 随机取特定数量的值,会保证返回的数量 """
        if not self.values:
            self.values = [(v,k) for k,v in self.items]
            self.values.sort(reverse=1)
        rs = set()
        n = min(100, max(5, count/2))
        for i in xrange(count + n):
            v = self.random()
            if v in rs:
                continue
            rs.add(v)
            if len(rs) == count:
                return rs
        for v,k in self.values:
            if k in rs:
                continue
            rs.add(k)
            if len(rs) == count:
                return rs
        return rs

    def __call__(self, *args, **kwargs):
        if args:
            return self.randoms(*args)
        return self.random()

    def left(self, num):
        i = bisect.bisect_left(self.rates, num)
        return self.items[i][0]

    def right(self, num):
        i = bisect.bisect_right(self.rates, num)
        return self.items[i][0]


def ran_region(regions, max_rate=100):
    """ 获取随机区间(列表结构),保留两位小数,从0开始 """
    if len(regions) == 0:
        return -1
    cur_num, index = 0, (len(regions) - 1)
    index = index if regions[index] > regions[0] else 0
    num = random.uniform(0, max_rate)
    for _index, region in enumerate(regions):
        cur_num += region
        if num <= cur_num:
            return _index
    return index


def ran_regions(regions):
    """ 概率运算,regions是字典, 每一个value都代表一个概率 """
    _sum = int(sum(regions.itervalues()))
    ran_num = random.randint(0, _sum)
    for k, v in regions.iteritems():
        _sum -= v
        if ran_num >= _sum:
            return k
    return k

def ran_addition(ids, id, add_rate, base_rate):
    """ 获取id, 特殊id有加成, 概率基数默认100 """
    if id not in ids or add_rate == 0:
        return random.choice(ids)

    r = random.randint(1, len(ids) * base_rate + add_rate)
    max = 0
    for i in ids:
        if i != id:
            max += base_rate
        else:
            max += base_rate + add_rate
        if r <= max:
            return i
    return random.choice(ids)


global_evals = dict(rom=rom, roms=roms, ran=randint, choice=choice)

#---------------------
#---------------------
