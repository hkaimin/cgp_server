#!/usr/bin/env python
# -*- coding:utf-8 -*-

from corelib import spawn
from game.define import constant
from game import Game
import app
import time
from datetime import datetime
from corelib.gtime import current_time
import config
import types

# 记录GM执行日志
def log_ExecGM_sql(who, pid, oneCmd, lcmd):
    data = {
        "uid": pid,
        "cmd": oneCmd,
        "lcmd": lcmd}
    Game.glog.log2FileByDict("ExecGM", data, flag=1)
    pass

# 记录创建角色日志
def log_CreateRole_sql(rid, account, password, pcode, Code, newTime, isAgent):
    # TimeKey = time.strftime("%Y-%m-%d %H:%M:%S", LocalTime())
    data = {
        "uid": rid,
        "account": account,
        "password": password,
        "pcode": pcode,
        "Code": Code,
        "creatime": newTime,
        "isAgent":isAgent,
    }
    Game.glog.log2FileByDict("CreateRole", data, flag=1)


# 记录创建角色日志
# 1 登录，0 下线
def log_RoleLogin_sql(rid, Code, loginStatus, times):
    data = {
        "uid": rid,
        "pcode": Code,
        "Code": Code,
        "status" : loginStatus,
        "logintimes": times # 登录次数
    }
    Game.glog.log2FileByDict2("playerLogin", rid, data, flag=1)

def log_RoleLogout_sql(rid, Code, loginStatus, times):
    data = {
        "uid": rid,
        "pcode": Code,
        "Code": Code,
        "status" : loginStatus,
        "logintimes": times # 登录次数
    }
    Game.glog.log2FileByDict2("playerLogout", rid, data, flag=1)


# 记录玩节目记录
def log_PlayGame_sql(rid, logData):
    dt = datetime.now()
    TimeKey = dt.strftime('%Y-%m-%d')
    logData["TimeKey"] = TimeKey
    Game.glog.log2FileByDict("PlayGame", logData, flag=1)





