#!/usr/bin/env python
# -*- coding:utf-8 -*-

from corelib import spawn
from game.gm import *
# app.frame.reload_modules(["game.player.player", "game.player.bag"])

lPath = ["game.gm.gmWebFunc",]


# 执行后台GM指令接口总入口
# 这里的who是rpc角色代理，只能执行对应方法
def ExecWebGmFunc(who, cmd, data):
    if not who:return {'err':errcode.EC_EXEC_WEBGM_RID_ERROR}
    func = None
    for sPath in lPath:
        mod = __import__(sPath)
        lPart=sPath.split('.')
        for sPart in lPart[1:]:
            mod=getattr(mod,sPart)
        if hasattr(mod, cmd):
            func = getattr(mod, cmd)
            if func:
                break
    if func:
        return func(who, data)
    else:
        return "Error: not exists gm function:%s !!"%cmd
    pass

# 回包统一封装
def packBack(data,success,err):
    res = {}
    if success:
        res["success"] = 1
        res["err"] = 0
        res["data"] = data
    else:
        res["success"] = 0
        res["err"] = err
        res["data"] = data
    return json.dumps(res)
#
# def setName(who, data):
#     '''修改昵称'''
#     param = data.get('name')
#     if param:
#         rs = who.setName(param)
#         who.save(forced=True)
#         if rs:
#             rs = packBack(rs, 1, 0)
#             return rs
#         else:
#             rs = packBack(rs, 1, errcode.EC_EXEC_WEBGM_ERROR)
#             return rs
#     else:
#         return ''
#
# def GM_setCanMail(who, data):
#     '''GM设置发邮件权限'''
#     param = data.get('canmail', 0)
#     rid = int(data.get('rid', 0))
#     if param:
#         print "who.base.isAgent", who
#         rs = who.GM_setCanMail(rid,int(param))
#         if rs:
#             rs = packBack(rs, 1 , 0)
#             return rs
#         else:
#             rs = packBack(rs, 1, errcode.EC_EXEC_GM_NOT_AGENT)
#             return rs
#     pass
#
# def GM_creatRole(who, data):
#     '''GM创建代理'''
#     account = data.get('account')
#     password = data.get('password')
#     isAgent = data.get('isAgent', 0) #是否代理号
#     if account and password:
#         ok, rs = who.GM_createAgentByWeb(account, password, isAgent)
#         if ok == 1:
#             return packBack(rs, 1, 0)
#         else:
#             return packBack(rs, 1, errcode.EC_EXEC_GM_NOT_AGENT)
#
# def GM_sendMail(who, data):
#     '''GM发邮件'''
#     param1 = data.get('mailTitle', '邮件标题') # 邮件标题
#     param2 = data.get('mailContent', '邮件内容') # 邮件内容
#     if param1 and param2:
#         canMail = who.GM_getCanMail(rid)
#         if not canMail:
#             rs = errcode.EC_EXEC_GM_MAIL_NO_AUTH
#         else:
#             rs = who.GM_sendMail(rid, param1, param2)
#         if rs and type(rs) == types.DictType:
#             rs = packBack(rs, 1 , 0)
#             return rs
#         elif rs and type(rs) == types.IntType:
#             rs = packBack({}, 1, rs)
#             return rs
#         else:
#             rs = packBack(rs, 1, errcode.EC_EXEC_WEBGM_ERROR)
#             return rs
#
# def GM_setPasswod(who, data):
#     '''修改密码'''
#     param = data.get('newpassword')
#     if param:
#         rs = {"id":who.getUID(), "password": param}
#         res = who.setPasswordForce(param)
#         if res:
#             who.save(forced=True)
#             rs = packBack(rs, 1, 0)
#             return rs
#         else:
#             rs = packBack(rs, 1, errcode.EC_EXEC_WEBGM_ERROR)
#             return rs
#
#
# def GM_transfer(who, data):
#     '''转账 代理和代理之间'''
#     rid = int(data.get('rid', 0)) # 发起转账人
#     playerId = int(data.get('rid', 0)) # 转账给谁
#     transCoin = int(data.get('transCoin', 0)) # 转账金额
#     player = get_rpc_player(int(rid))
#     toplayer = get_rpc_player(int(playerId))
#     if not player.IsAgent() or not toplayer.IsAgent():
#         return packBack({}, 1, errcode.EC_EXEC_GM_NOT_AGENT)
#     rs1 = player.setCoinTrans(-transCoin)
#     rs2 = toplayer.setCoinTrans(transCoin)
#     if rs1 and rs2:
#         d = {rid: rs1, playerId: rs2}
#         return packBack(d, 1, 0)
#     else:
#         return packBack({}, 1, errcode.EC_EXEC_WEBGM_ERROR)
#     pass
#
#
# def GM_shangfen(who, data):
#     '''上分（充值）'''
#     pass
#
#
# def GM_xiafen(who, data):
#     '''下分（回收、提现）'''
#     pass
#
#
# def GM_getCount(who=None, data=None):
#     '''获取在线人数'''
#     ret_val = {}
#     logics = Game.rpc_logic_game.count
#     max_logics = config.max_players / config.logic_players
#     user = Game.rpc_player_mgr.get_count()
#     max_user = config.max_players
#     ret_val.update({'logics': logics, 'max_logics': max_logics,
#                     'user': user, 'max_user': max_user})
#     rs = packBack(ret_val, 1, 0)
#     return rs
#
# # 模式1用到, 设置根抽水比例
# def GM_setRootBeget(who, data):
#     BigBeget = data.get('BigBeget', 0)
#     from game.common.db import new_game_store
#     store = new_game_store()
#     lRootPlayer = store.query_loads(Player.DATA_CLS.TABLE_NAME,
#                                          dict(account=config.root_player_account, password=config.root_player_password))
#     pdata = lRootPlayer[0]
#     root_rid = pdata.get("id")
#     rootplayer = get_rpc_player(int(root_rid))
#     print "root_rid:",root_rid,"rootplayer:",rootplayer
#     rs = rootplayer.setBeGet(float(BigBeget))
#     rootplayer.save(forced=True)
#     if rs:
#         rs = packBack(rs, 1, 0)
#     else:
#         rs = packBack(rs, 1, errcode.EC_EXEC_WEBGM_ERROR)
#     return rs
#
# # 设置代理佣金比例
# def GM_setAgentBeget(who, data):
#     '''修改佣金比例'''
#     Beget = data.get('Beget', 0) #
#     rs = who.setBeGet(float(Beget))
#     if rs:
#         who.save(forced=True)
#         rs = packBack(rs, 1, 0)
#     else:
#         rs = packBack(rs, 1, errcode.EC_EXEC_WEBGM_ERROR)
#     return rs
#
# # 查找某账号的所有下家信息
# def GM_getChildrenInfo(who):
#     from game.common.db import new_game_store
#     store = new_game_store()
#     lChildren = Game.rpc_membtree_svr.rc_getAllChildren(who.base.code)
#     # who.notify(str(lChildren))
#     # print "---lChildren:", lChildren
#     l = []
#     for iCode in lChildren:
#         d = {}
#         iRid = Game.rpc_membtree_svr.getRidByCode(iCode)
#         lRootPlayer = store.query_loads(Player.DATA_CLS.TABLE_NAME,
#                                              dict(id=iRid))
#         dplayer = lRootPlayer[0]
#         # print "-->",iRid,dplayer.get("password"),dplayer.get("account")
#         d["id"] = iRid
#         d["name"] = dplayer.get("name", "")
#         d["account"] = dplayer.get("account", "")
#         d["coin"] = dplayer.get("coin", 0)
#         l.append(d)
#     return l
#
# # 获取玩家在线信息
# # 玩家账号 玩家ID 游戏名称 桌子号 桌子类型 金币总数 所属代理
# def GM_playerOnlineInfo(who):
#     pass


import config
import types
from game.define import  errcode
from corelib.data import json, json_dumps
from game import Game
import game.mgr.player
from game.core.player import Player
from game.mgr.player import *

