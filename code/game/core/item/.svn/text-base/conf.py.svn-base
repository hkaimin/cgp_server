#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'
# from game.common.ctn import CPstContainerBase
from game.common.utility import *
import game.mgr.player
import time
from game import Game
import weakref

ONE_DAY_SEC = 60 * 60 * 24  # 一天的秒数
MAX_AMOUNT = 999
# dKEYS = {1: "LIFE", 2: "SPEED", 3: "COUNT", 4: "POWER"}
class CItemType(object):
    ADD_LIFE = 1 # PVP 增加生命
    ADD_SPEED = 2 # PVP 增加速度
    ADD_COUNT = 3 # PVP 增加次數
    ADD_POWER = 4 # PVP 增加威力
    ADD_COIN = 5
    ADD_DIAMOND = 6
    ADD_DIY_MAP_CNT = 71
    ADD_EXP = 8
    ADD_LIKE = 9 # 增加点赞次数
    PAO_PAO_SKIN = 10 #泡泡皮肤
    BOX = 11 # 宝箱
    UNLOCK_CLASS = 12 # 解锁职业
    UNLOCK_FUNC = 13 # 解锁功能
    ADD_TILI = 14 # 增加体力道具
    ADD_SKILL = 15

class CItemUnlockFunc(object):
    UL_DIYMAP_FUNC = 1 # DIY地图

class CItemUnlockDIYMapType(object):
    DIY_FUNC = 1
    MAP_TYPE_TWO = 2
    MAP_TYPE = 3



