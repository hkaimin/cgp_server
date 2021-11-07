#!/usr/bin/env python'
# -*- coding: utf-8 -*-

#玩家操作类型
PL_LOG_LOGIN = 1
PL_LOG_LOGOUT = 2
PL_LOG_START_GAME = 3
PL_LOG_END_GAME = 4
PL_LOG_REG_HERO = 5

#一天秒数
DAY_FOR_SEC = 86400


#存留率规格
RRT_NEXTDAY = 1
RRT_3DAY = 3
RRT_7DAY = 7

class MDBOpe(object):

    # ope = {}
    # ope["="] = '$eq'
    # ope[">"] = "$gt"
    # ope["<"] = "$lt"
    # ope["<="] = "$lte"
    # ope[">="] = "$gte"
    # ope["!="] = "$ne"
    def __init__(self):
        pass

    def __ge__(self, other):
        return {"$gte": other}

    def __gt__(self, other):
        return {"$gt": other}

    def __lt__(self, other):
        return {"$lt": other}

    def __le__(self, other):
        return {"$lte": other}

    def __ne__(self, other):
        return {"$ne": other}

    def __eq__(self, other):
        return {"$ep": other}

    def interval(self, start, end):
        return {"$gte": start, "$lt": end}

    def oror(self, other):
        return {'$or': other}
