#!/usr/bin/env python
#-*- coding:utf-8 -*-
from datetime import timedelta

# 购买类型
class BUY_TYPE(object):
    NOT_LIMIT       = 1 # 没限制
    HAS_LIMIT       = 2 # 有总限制
    DAY_LIMIT       = 3 # 天限制
    WEEK_LIMIT      = 4 # 周限制
    TIME_LIMIT      = 5 # 时间限制
    SERVER_DAY_LIMIT  = 6 # 全服每天限制
    SERVER_WEEK_LIMIT = 7  # 全服周限制


# 商品类型
class SHOP_TYPE(object):
    ALL_TYPE            = 0  # 全部道具
    NORMAL_TYPE         = 1  # 普通道具
    PAOPAOSHOW_TYPE     = 2  # 泡泡外观道具
    PAOPAOEFFECT_TYPE   = 3  # 泡泡爆炸效果道具


# 支付类型
class PAY_TYPE(object):
    COIN_PAY            = 1 # 金币
    DIAMOND_PAY         = 2 # 钻石
    VIDIO_PAY           = 3 # 观看视频