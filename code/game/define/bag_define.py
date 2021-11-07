#!/usr/bin/env python
#-*- coding:utf-8 -*-
from datetime import timedelta


# 背包类型
class BAG_TYPE(object):
    ALL_TYPE = 0  # 全部道具
    NORMAL_TYPE = 1  # 普通道具
    PAOPAOSHOW_TYPE = 2  # 泡泡外观道具
    PAOPAOEFFECT_TYPE = 3  # 泡泡爆炸效果道具
