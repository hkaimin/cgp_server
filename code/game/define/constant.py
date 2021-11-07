#!/usr/bin/env python
#-*- coding:utf-8 -*-
from datetime import timedelta

#一天
ONE_DAY_DELTA = timedelta(days=1)
ONE_DAY_TIME = 60 * 60 * 24

#是否启用重连
RECONNECTED = 1

#登录登出标识
FLAG_LOGIN = 1
FLAG_LOGOUT = 2


#---------------------
# 战斗模式
APP_MODE_PVP = 1
APP_MODE_PVE = 2
APP_MODE_PVE_GUANKA = 3


# 捡到道具
# 速度 Type : 1
# 泡泡数量道具 Type : 2
# 泡泡威力道具 Type : 3
# 生命 Type : 4
# 问号红包 Type : 5
# 屎 : 6
# 通关门： 7
class CFightToolType(object):
    SPEED = 1
    NUM = 2
    POWER = 3
    LIFE = 4
    REDBAO = 5
    SHIT = 6
    DOOR = 7


class CTili(object):
    DEFAULT_TILI = 100 # 基础体力
    RECOVERY_CD = 300 # 恢复体力CD 秒
    REC_SPEED = 10 # 每次恢复体力 点数
    MAX_TILI = 200 # 最大体力点数
    NORMAL_ADD = 1 # 普通增加体力
    TOOL_ADD = 2 # 道具增加体力
    GM_ADD = 3 # GM增加体力
    pass

# 使用增加属性道具的战斗模式
class CUseItemFightMode(object):
    PVP = 1
    PVE_GUANKA = 2

