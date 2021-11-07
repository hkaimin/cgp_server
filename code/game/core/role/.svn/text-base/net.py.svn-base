#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'
# from game.common.ctn import CPstContainerBase
from game.common.utility import *
import game.mgr.player
import time
from game import Game

from corelib.message import observable
from corelib import spawn_later, log, spawn
from corelib.gtime import current_time
from game import Game
from game.define.shop_define import *
from game.define.constant import *
import random


DEFAULT_ROLE_ID = 1
SYS_GIVE_TYPE = 0 # 系统赠送类型

class CPlayVidioType(object):
    SHOP = 1    # 商城
    BUY_CLASS = 2 # 购买角色
    QIANDAO = 3 # 签到
    LEVEL_REWARD = 4 # 等级奖励


# 角色系統

# @observable
class netCmd(object):
    # 协议处理模块
    def __init__(self):
        self.GameConfData = Game.res_mgr.res_gameConfData
        self.RoleConfData = Game.res_mgr.res_roleData
        self.HelpData     = Game.res_mgr.res_helpData

    # 获取出战角色
    def getClass(self):
        iClass = self.base.iClass
        return iClass

    # 设置出战角色
    def setClass(self, iClass):
        self.Set("fightClass", iClass)
        self.base.iClass = iClass

    # 获取角色战斗属性
    def getRoleFightProperty(self, FightType=0):
        iClass = self.getClass()
        RoleInfoObj = self.RoleConfData.get(iClass)
        if FightType == APP_MODE_PVE_GUANKA:
            fightData = RoleInfoObj.getPveProperty()
        else:
            fightData = RoleInfoObj.getPvpProperty()
        return fightData

    # 获取角色详情
    def getRoleDetail(self):
        iClass = self.getClass()
        RoleInfoObj = self.RoleConfData.get(iClass)
        if not RoleInfoObj:
            self.notify("角色编号错误！")
            return

        id = RoleInfoObj.id
        pvp_life = RoleInfoObj.pvp_life
        pvp_speed = RoleInfoObj.pvp_speed
        pvp_power = RoleInfoObj.pvp_power
        pvp_cnt = RoleInfoObj.pvp_cnt
        # ================PVE属性==================
        pve_life = RoleInfoObj.pve_life
        pve_speed = RoleInfoObj.pve_speed
        pve_power = RoleInfoObj.pve_power
        pve_cnt = RoleInfoObj.pve_cnt
        lv = self.base.lv
        exp = self.base.exp
        dInfo = {
            "id":id,
            "lv": lv,
            "exp":exp,
            "life": "%s(PVE:%s)"%(pvp_life,pve_life),
            "speed": "%s(PVE:%s)"%(pvp_speed,pve_speed),
            "power": "%s(PVE:%s)"%(pvp_power,pve_power),
            "cnt": "%s(PVE:%s)"%(pvp_cnt,pve_cnt),
            "name": self.Name(),
        }
        return dInfo

    # 设置默认角色
    def initDefaultRole(self):
        myOwnClassList = self.Query("myOwnClassList", [])
        if not self.Query("fightClass") and not myOwnClassList:
            myOwnClassList.append(DEFAULT_ROLE_ID)
            self.setClass(DEFAULT_ROLE_ID)
        for id, RoleObj in self.RoleConfData.iteritems():
            if RoleObj.payType == SYS_GIVE_TYPE and id not in myOwnClassList:
                myOwnClassList.append(id)
        self.Set("myOwnClassList", myOwnClassList)
        return myOwnClassList

    # 获取我拥有的角色列表
    def getMyOwnClassList(self):
        myOwnClassList = self.Query("myOwnClassList", [])
        if not myOwnClassList:
            return self.initDefaultRole()
        return myOwnClassList


    # 获取所有角色列表
    def rc_showAllClassList(self):
        MyOwnClassList = self.getMyOwnClassList()
        AllRoleKey = self.RoleConfData.keys()
        AllRoleKey.sort()
        allRoleList = []
        fightClass = self.Query("fightClass", 1)
        for iClass in AllRoleKey:
            RoleInfoObj = self.RoleConfData.get(iClass)
            isonline = RoleInfoObj.isonline
            if not isonline:
                continue
            pvp_life = RoleInfoObj.pvp_life
            pvp_speed = RoleInfoObj.pvp_speed
            pvp_power = RoleInfoObj.pvp_power
            pvp_cnt = RoleInfoObj.pvp_cnt
            # ================PVE属性==================
            pve_life = RoleInfoObj.pve_life
            pve_speed = RoleInfoObj.pve_speed
            pve_power = RoleInfoObj.pve_power
            pve_cnt = RoleInfoObj.pve_cnt
            desc = RoleInfoObj.desc # 角色描述
            price = RoleInfoObj.price  # 售价
            payType = RoleInfoObj.payType # 支付类型  0,自动赠送 1，金币购买 2，钻石购买

            smallHead = RoleInfoObj.smallHead # 小头像
            bgHead = RoleInfoObj.bgHead # 角色背景
            aminRes = RoleInfoObj.aminRes # 角色展示动画
            name = RoleInfoObj.name # 角色名字

            isOwn = 0 # 是否已拥有
            if iClass in MyOwnClassList:
                isOwn = 1
            isUse = 0
            if fightClass==iClass:
                isUse = 1
            dInfo = {
                "iClass": iClass, # 角色编号
                "life": "%s" % (pvp_life),
                "speed": "%s" % (pvp_speed),
                "power": "%s" % (pvp_power),
                "cnt": "%s" % (pvp_cnt),
                "desc": desc,       # 角色描述
                "payType": payType, # 支付类型  0,自动赠送 1，金币购买 2，钻石购买
                "price": price,     # 售价
                "isOwn": isOwn,     # 是否已拥有
                "smallHead": smallHead,  # 小头像
                "bgHead": bgHead,   # 角色背景
                "aminRes": aminRes, # 角色展示动画
                "name":name, # 角色名字
                "isUse": isUse# 是否出战中
            }
            # print "------dInfo---",iClass,dInfo
            allRoleList.append(dInfo)
        return {
            "allRoleList": allRoleList
        }

    # 刷新角色列表
    def reflashClassList(self):
        data = self.rc_showAllClassList()
        spawn(self.broadcast, 'reflashClassList', data)

    # 购买角色
    def rc_buyClass(self, iClass, isTool=False):
        myOwnClassList = self.Query("myOwnClassList", [])
        if iClass in myOwnClassList:
            self.notify("该角色已购买!")
            return {}
        RoleInfoObj = self.RoleConfData.get(iClass)
        if not isTool:
            price = RoleInfoObj.price  # 售价
            payType = RoleInfoObj.payType  # 支付类型  0,自动赠送 1，1金币购买 2，钻石购买，3，视频
            if payType == 1:
                own_coin = self.base.getCoin()
                if own_coin < price:
                    self.notify("金币不足！")
                    return False
                self.base.setCoin((-1 * price))
                pass
            elif payType == 2:
                own_diamond = self.base.getDiamond()
                if own_diamond < price:
                    self.notify("钻石不足!")
                    return False
                self.base.setDiamond((-1 * price))
                pass
            elif payType == 3:
                pass

        dReflashData = self.base.to_reflash_simple()
        self.broadcast("reflashsimple", dReflashData)
        myOwnClassList.append(iClass)
        self.Set("myOwnClassList", myOwnClassList)
        self.reflashClassList()
        self.notify("购买角色成功")
        try:
            Game.glog.log2File("buyClass",
                               "%s|%s|%s|%s" % (
                                   self.id, self.Name(), self.data.account, iClass))
        except:
            pass
        return {}

    # 使用角色
    def rc_useClass(self, iClass):
        myOwnClassList = self.Query("myOwnClassList", [])
        if iClass in myOwnClassList:
            self.setClass(iClass)
            self.reflashClassList()
            self.notify("出战成功")
            return {"iuseClass":iClass, "err":"ok"}
        self.notify("该角色还没购买")
        return {"err":"notbuy"}

    # 刷新角色属性
    def rc_reflashProperty(self):
        data ={

        }
        spawn(self.broadcast, 'reflashProperty', data)
        pass

    # 帮助界面
    def rc_getHelp(self, helpID):
        helpID = int(helpID)
        _help = self.HelpData.get(helpID, None)
        if not _help:
            return
        data = {}
        data["name"] = _help.name
        data["content"] = _help.content
        return data

    # 找出推荐角色
    def G2CRecommendClass(self):
        lOwnRole = self.getMyOwnClassList()
        fightClass = self.Query("fightClass", 1)
        AllRoleKey = self.RoleConfData.keys()
        AllRoleKey.sort()
        if fightClass == max(AllRoleKey):
            return 
        lrec = []
        for classID in AllRoleKey:
            if classID not in lOwnRole and classID > fightClass:
                lrec.append(classID)
        if lrec:
            recClass = random.choice(lrec)


    # iType : 类型
    # iNo : 商品ID 或 角色 id , 没用到传0
    # pageType : 购买后刷新哪页，只有商城才用到, 没用到传0
    def playVidioBefore(self, iType, iNo, pageType=1):
        if not iType or not iNo:
            self.notify("信息有误iType：%s, iNo：%s"%(iType, iNo))
            return
        data = {
            "iType":iType,
            "iNo":iNo,
            "pageType":pageType
        }
        self.Set("PlayerVidioInfo", data)

    def playVidioFinish(self):
        PlayerVidioInfo = self.Query("PlayerVidioInfo")
        print "PlayerVidioInfo", PlayerVidioInfo
        iType = PlayerVidioInfo.get("iType")
        iNo = PlayerVidioInfo.get("iNo")
        pageType = PlayerVidioInfo.get("pageType", 1)
        if not iType or not iNo:
            self.notify("信息有误 iType：%s, iNo：%s" % (iType, iNo))
            return
        if iType == CPlayVidioType.SHOP:
            print 111111, iNo
            self.rc_Buy(self, iNo, pageType)
        elif iType == CPlayVidioType.BUY_CLASS:
            iClass = iNo
            print 1111112, iNo
            self.rc_buyClass(iClass)
        elif iType == CPlayVidioType.QIANDAO:
            print 1111113, iNo
            self.rc_getSeventDayReward()
        elif iType == CPlayVidioType.LEVEL_REWARD:
            iLv = iNo
            print 1111114, iNo
            self.getUpgradeReward(iLv)
        self.Set("PlayerVidioInfo", {})