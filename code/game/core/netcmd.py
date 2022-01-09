#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

from corelib.message import observable
from corelib import spawn_later, log, spawn
from corelib.gtime import current_time
from game import Game
from game.define import msg_define
from game.define.protocol_define import *
from game.define import horse_define

import game.core.PaoPaoPVP.net
import game.core.item.net
import game.core.diyMap.net
import game.core.rank.net
import game.core.shop.net
import game.core.login.net
import game.core.PaoPaoPVEGuanKa.net
import game.core.role.net
import game.core.guide.net
import game.core.skill.net

ticket_price_maincoin = 1

# @observable
# 用Player继承
class netCmd(game.core.PaoPaoPVP.net.netCmd,    # 泡泡PVP战斗协议处理模块
             game.core.item.net.netCmd,         # 物品背包
             game.core.diyMap.net.netCmd,       # DIY地图
             game.core.rank.net.netCmd,         # 排行榜
             game.core.shop.net.netCmd,         # 商城
             game.core.login.net.netCmd,         # 登陆奖励
             game.core.PaoPaoPVEGuanKa.net.netCmd,# 无尽模式
             game.core.role.net.netCmd,           # 角色系統
             game.core.guide.net.netCmd,           # 新手引导
             game.core.skill.net.netCmd,           # 技能
             ):

    # 协议处理模块
    def __init__(self):
        game.core.PaoPaoPVP.net.netCmd.__init__(self)
        game.core.diyMap.net.netCmd.__init__(self)
        game.core.shop.net.netCmd.__init__(self)
        game.core.item.net.netCmd.__init__(self)
        game.core.login.net.netCmd.__init__(self)
        game.core.PaoPaoPVEGuanKa.net.netCmd.__init__(self)
        game.core.role.net.netCmd.__init__(self)
        game.core.guide.net.netCmd.__init__(self)
        game.core.skill.net.netCmd.__init__(self)
        self.res_openCtrl = Game.res_mgr.res_openCtrlData

    # ============= 角色一般协议相关 ==============

    def getOpenCtrlData(self):
        # self.res_openCtrl
        dData = {}
        for id, crtlObj in self.res_openCtrl.iteritems():
            print id, crtlObj.Save()
            dData[id] = crtlObj.Save()
        return dData


    # 进入游戏返回
    def entergame(self, who):
        print "-1-----------------rc_entergame-",who.base.lv
        who.safe_pub(msg_define.MSG_ENTER_GAME)
        isMaxLv = 0 # 是否滿級
        self.pushBtnData()

        rs = who.base.to_init_dict()
        lv = who.Lv()
        if max(Game.res_mgr.res_upgrade.keys()) <= lv:
            isMaxLv = 1
        rs['maxExp'] = who.getExp() # 最大经验
        rs['isMaxLv'] = isMaxLv                       # 是否满级
        rs["mailUnRead"] = 0
        rs["playCount"] = 0
        rs["wujinDiffLevel"] = self.getwujinDiffLevel()
        rs["gm"] = who.data.IsGm()
        rs["token"] = who.relogin_token
        rs["btnCtrlData"] = self.getOpenCtrlData()

        rs["ticketPrice"] = horse_define.TICKET_COST_NUM
        # self.broadcast("entergame", rs)
        return rs

    def setName(self, who, name):
        """修改昵称"""
        print "-----------------set name"
        who.data.setName(name)
        return dict(name=who.data.getName())

    def setRealName(self, who, truename):
        """修改真实姓名"""
        who.base.setRealName(truename)
        return dict(name=who.base.getRealName())

    def setPassword(self, who, oldpassword, newpassword):
        """修改密码"""
        return who.data.setPassword(oldpassword, newpassword)

    def setPasswordForce(self, who, newpassword):
        """强行修改密码"""
        return who.data.setPasswordForce(newpassword)

    def setWeixin(self, who, weixin):
        """修改微信号"""
        who.base.setWeixin(weixin)
        return dict(weixin=who.base.getWeixin())

    def setIcon(self, who, icon):
        """修改头像"""
        who.base.setIcon(icon)
        return dict(icon=who.base.getIcon())

    def rc_getRoleDetail(self, who):
        '''获取角色详情'''
        pass



# # rpc协议总入口
# def netcmd_rpc_Opera(who, iSub, funcName, *args):
#     func = None
#     if iSub == PLAYER_PROTOCOL: # 角色基础协议处理模块
#         func = getattr(who.netCmd, funcName)
#     elif iSub == PAOPAO_PVP:#  泡泡PVP战斗协议处理模块
#         func = getattr(who.netCmd.PaoPaoPvpNet, funcName)
#     elif iSub == PAOPAO_PVE:  # 泡泡PVE战斗协议处理模块
#         pass
#     elif iSub == ITEM: # 物品背包
#         func = getattr(who.netCmd.ItemNet, funcName)
#     elif iSub == DIY_MAP: # DIY地图
#         func = getattr(who.netCmd.DiyMapNet, funcName)
#     elif iSub == RANK: # 排行榜
#         func = getattr(who.netCmd.RankNet, funcName)
#     elif iSub == SHOP: # 商城
#         func = getattr(who.netCmd.shopNet, funcName)
#     if not func: return
#     return func(who,*args)



