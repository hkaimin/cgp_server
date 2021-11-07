#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from random import randint
from bson.code import Code
from pymongo import MongoClient

db = MongoClient('mongodb://127.0.0.1/rich9_log').get_default_database()
cn = db['log_online']
cn.drop()

code = Code('''
db.log_online.group({
    keyf: function(doc) {
        var date = new Date(doc.ct * 1000);
        date.setTime(date.getTime() - date.getTimezoneOffset() * 1000 * 60);
        var key = date.toISOString().replace('T', ' ').slice(0, 13);
        return {time: key};
    },
    initial: {items: [], total: 0, count: 0},
    reduce: function(cur, result) {
        result.items.push(cur.c);
        result.count += 1;
        result.total += cur.c;
    },   
    finalize: function(result) {
        result.avg = result.total / result.count;
        result.min = Math.min.apply(Math, result.items);
        result.max = Math.max.apply(Math, result.items);
    }
});
''')

from IPython import embed; embed() 

