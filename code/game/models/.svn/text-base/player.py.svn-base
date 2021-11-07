#!/usr/bin/env python
# -*- coding:utf-8 -*-
from game.define.store_define import TN_P_PLAYER

from store.store import StoreObj

from game import Game
import weakref
import sys

class ModelPlayer(StoreObj):
    """玩家数据"""
    TABLE_NAME = TN_P_PLAYER

    def init(self):
        self.owner = None     # 所属玩家对象
        self.id = None        # rid
        self.gm = 0           # 是否gm 先默认都是GM
        self.name = ''        # 名字
        self.account = ''     # 账号
        self.password = ''    # 密码
        self.newTime = 0      # 创建时间
        self.loginTime = 0    # 最后登录时间
        self.logoutTime = 0   # 最后登出时间
        self.itemTranceNo = 0 #用于生成物品唯一id的自增值
        self.mailTranceNo = 0 #用于生成邮件唯一id的自增值
        self.shopTranceNo = 0 #用于生成物品唯一id的自增值
        self.loginNum = 0  # 角色历史登陆次数

        # new add
        self.base = {}    # 角色基础数据（微信号，推广号，手机号，区域客户微信号，金币，头像）
        self.bagDict = {} # 背包
        self.shopDict = {} # 商城
        self.mailDict = {}  # 角色邮件(已读信息等)
        # 周期数据
        self.cycleHourDict = {}  # 小时周期数据
        self.clcleDayDict = {}   # 天周期数据
        self.clcleDay7Dict = {}  # 天周期数据 保存7天内的
        self.cycleWeekDict = {}  # 周周期数据
        self.cycleMonthDict = {} # 月周期数据
        self.cycleHourBytes = "" # 小时周期数据
        self.clcleDayBytes = ""  # 天周期数据
        self.clcleDay2Bytes = "" # 天周期数据 保存2天内的
        self.clcleDay7Bytes = "" # 天周期数据 保存7天内的
        self.cycleWeekBytes = ""  # 周周期数据
        self.cycleMonthBytes = ""  # 月周期数据


    def set_owner(self, who):
        self.owner = weakref.proxy(who)

    def to_save_dict(self, copy=False, forced=False):
        #todo:针对各个模块做cache，避免每次都全量打包，提高性能
        save = {}
        save['id'] = self.id
        save['name'] = self.name
        save['account'] = self.account
        save['password'] = self.password
        save['newTime'] = self.newTime
        save['loginTime'] = self.loginTime
        save['logoutTime'] = self.logoutTime
        save['itemTranceNo'] = self.itemTranceNo
        save['mailTranceNo'] = self.mailTranceNo
        save['shopTranceNo'] = self.shopTranceNo
        save['gm'] = self.gm
        save['loginNum'] = self.loginNum
        # new add
        # if not self.owner: return
        save['base'] = self.owner.base.to_save_dict(forced=forced)  # 角色基础信息
        bagDict = self.owner.bag.Save(forced=forced)  # 角色背包
        if bagDict != None:
            save['bagDict'] = bagDict  # 角色背包
        shopDict = self.owner.shop.Save(forced=forced)  # 角色商城
        if shopDict != None:
            save['shopDict'] = shopDict  # 角色商城
        # save['mail'] = self.owner.mail.to_save_dict(forced=forced)  # 角色邮件
        # 周期数据
        # save['cycleHour'] = self.owner.cycleHour.to_save_bytes()  # 小时周期数据
        # save['cycleDay'] = self.owner.cycleDay.to_save_bytes()  # 天周期数据
        # save['cycleDay_7'] = self.owner.cycleDay_7.to_save_bytes()  # 天周期数据 保存7天内的
        # save['cycleWeek'] = self.owner.cycleWeek.to_save_bytes()  # 周周期数据
        # save['cycleMonth'] = self.owner.cycleMonth.to_save_bytes()  # 月周期数据
        save['cycleHourBytes'] = self.owner.cycleHour.to_save_bytes()  # 小时周期数据
        save['clcleDayBytes'] = self.owner.cycleDay.to_save_bytes()  # 天周期数据
        save['clcleDay2Bytes'] = self.owner.cycleDay_2.to_save_bytes()  # 天周期数据 保存2天内的
        save['clcleDay7Bytes'] = self.owner.cycleDay_7.to_save_bytes()  # 天周期数据 保存7天内的
        save['cycleWeekBytes'] = self.owner.cycleWeek.to_save_bytes()  # 周周期数据
        save['cycleMonthBytes'] = self.owner.cycleMonth.to_save_bytes()  # 月周期数据
        # print '-====== player to_save_dict',save
        return save

    #overwrite
    def save(self, store, forced=False):
        StoreObj.save(self,store, forced=forced)
        self.owner.base.cleanDirty()  # 角色基础信息
        # self.owner.mail.cleanDirty()  # 角色邮件
        self.owner.bag.ClearDirtyFlag()  # 角色背包
        # self.owner.shop.ClearDirtyFlag()  # 角色商城
        # 周期数据
        self.owner.cycleHour.cleanDirty()  # 小时周期数据
        self.owner.cycleDay.cleanDirty()  # 天周期数据
        self.owner.cycleDay_7.cleanDirty()  # 天周期数据 保存7天内的
        self.owner.cycleWeek.cleanDirty()  # 周周期数据
        self.owner.cycleMonth.cleanDirty()  # 月周期数据

    def setPassword(self, oldpassword, newpassword):
        if oldpassword != self.password:
            return False
        self.password = newpassword
        self.modify()
        return True

    def setPasswordForce(self, newpassword):
        self.password = newpassword
        self.modify()
        return True

    def AddLoginNum(self):
        self.loginNum += 1
        self.modify()

    def SetLoginTime(self, iTime):
        self.loginTime = iTime
        self.modify()

    def SetLogoutTime(self, iTime):
        self.logoutTime = iTime
        self.modify()

    def GenerateItemTranceNo(self):
        self.itemTranceNo += 1
        self.modify()
        return self.itemTranceNo

    def GenerateMailTranceNo(self):
        self.mailTranceNo += 1
        self.modify()
        return self.mailTranceNo

    def GenerateShopTranceNo(self):
        self.shopTranceNo += 1
        self.modify()
        return self.shopTranceNo

    def setName(self, name):
        self.name = name
        self.modify()

    def getName(self):
        if not self.name:
            return self.account
        return self.name

    def IsGm(self):
        if sys.platform == 'win32':
            return 1
        if self.account in ["odEtK5HADfkfNcWdpowlFfTGvuSc",
                            "odEtK5BTmDapF1PpRMiLMhldtV3o",
                            "op5ea5G1QLjBTTZA-qYej-bNrjj0",
                            "op5ea5GgcOUvzYYdPKOFJLzQPy_k",
                            "op5ea5GYMdoHRkMtBloIOoQ0vpIo",
                            ]:
            return 1
        return 0

    @classmethod
    def name_to_id(cls, name):
        rs = Game.store.values(cls.TABLE_NAME, None, dict(name=name))
        if rs:
            return rs[0]['id']

    @classmethod
    def id_to_name(cls, pid):
        rs = Game.store.values(cls.TABLE_NAME, ['name'], dict(id=pid))
        if rs:
            return rs[0]['name']