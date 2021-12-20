#!/usr/bin/env python
# -*- coding:utf-8 -*-

from game.common import utility
import weakref

#角色基础信息
class PlayerBase(utility.CEasyPersist):
    def __init__(self, owner):
        utility.DirtyFlag.__init__(self)
        self.owner = weakref.proxy(owner)  # 拥有者
        self.name = ""      # 昵称
        self.realname = ""  #真实姓名
        self.wxId = ''      # 微信号
        self.telNum = 0     # 手机号
        self.areaWXID = ''  # 区域客户微信号
        self.coin = 0       # 金币
        self.diamond = 0    # 钻石
        self.headPic = ''   # 头像
        self.lv = 1         # 等级
        self.exp = 0        # 经验
        self.curexp = 0     # 当前经验
        self.gender = 0     # 性别

        # 战斗属性
        self.lift = 1        # 多少条命
        self.speed = 1       # 速率
        self.power = 1       # 威力
        self.paopaocount = 1 # 范围

        self.iClass = 1      # 角色
        self.dSkill = {}     # 技能数据
        self.dData = {}     # 用來存放可伸缩持久化数据，包括容器数据
        self.save_cache= {} #存储缓存

    def markDirty(self):
        utility.DirtyFlag.markDirty(self)
        if self.owner:
            self.owner.markDirty()

    def setGender(self, gender):
        self.gender = int(gender)
        self.markDirty()

    def setName(self, name):
        self.name = name
        self.markDirty()

    def setRealName(self, realname):
        self.realname = realname
        self.markDirty()

    def getRealName(self):
        return self.realname

    def setWeixin(self, weixin):
        self.wxId = weixin
        self.markDirty()

    def getWeixin(self):
        return self.wxId

    def setIcon(self, icon):
        self.headPic = icon
        self.markDirty()

    def getIcon(self):
        return self.headPic

    def setCoinBack(self, coin):
        self.coin = int(coin)
        self.markDirty()

    def getCoin(self):
        return self.coin

    # 添加金币
    def setCoin(self, iAdd):
        iAdd = int(iAdd)
        print "-----------setCoin%s"%(self.coin), iAdd
        self.coin += int(iAdd)
        if self.coin <=0:
            self.coin = 0
        if iAdd < 0:
            self.owner.notify("cost maincoin x%s"%iAdd)
        elif iAdd > 0:
            self.owner.notify("add maincoin x%s" %iAdd)

    # 获取钻石
    def getDiamond(self):
        return self.diamond

    # 添加钻石
    def setDiamond(self, iAdd):
        iAdd = int(iAdd)
        self.diamond += int(iAdd)
        if self.diamond <=0:
            self.diamond = 0
        if iAdd < 0:
            self.owner.notify("cost subcoin x%s"%iAdd)
        else:
            self.owner.notify("add subcoin x%s" % iAdd)

    # 添加主币
    def setMainCoin(self,iMaincoin):
        self.coin = int(iMaincoin)
        self.markDirty()

    # 添加子币币
    def setSubCoin(self,iSubcoin):
        self.diamond = int(iSubcoin)
        self.markDirty()

    # 获得技能数据 {id:Lv, id:Lv}
    def getSkill(self):
        return self.dSkill

    def setSkill(self, dData):
        self.dSkill = dData
        self.markDirty()

    #存库数据
    def to_save_dict(self, forced=False):
        if self.isDirty() or forced:
            self.save_cache = {}
            self.save_cache["name"] = self.name
            self.save_cache["realname"] = self.realname
            self.save_cache["wxId"] = self.wxId
            self.save_cache["telNum"] = self.telNum
            self.save_cache["areaWXID"] = self.areaWXID
            self.save_cache["coin"] = self.coin
            self.save_cache["headPic"] = self.headPic
            self.save_cache["diamond"] = self.diamond
            self.save_cache["lv"] = self.lv
            self.save_cache["exp"] = self.exp
            self.save_cache["curexp"] = self.curexp
            self.save_cache["gender"] = self.gender
            self.save_cache["iClass"] = self.iClass
            self.save_cache["dSkill1"] = self.dSkill
            print "--------to_save_dict-------------",self.dSkill
        self.save_cache["dData"] = self.Save()
        return self.save_cache


    #读库数据初始化
    def load_from_dict(self, data):
        self.name = data.get("name","")          # 昵称
        self.realname = data.get("realname", '')    # 真实姓名
        self.wxId = data.get("wxId", '')            # 微信号
        self.telNum = data.get("telNum", 0)         # 手机号
        self.areaWXID = data.get("areaWXID", '')    # 区域客户微信号
        self.coin = data.get("coin", 0)             # 金币
        self.diamond = data.get("diamond", 0)       # 钻石
        self.headPic = data.get("headPic", '')      # 头像
        self.lv = data.get("lv", 1)                 # 等级
        self.exp = data.get("exp", 0)               # 经验
        self.curexp = data.get("curexp", 0)         # 当前经验
        self.gender = data.get("gender", 0)         # 性别
        self.iClass = data.get("iClass", 1)         # 角色职业
        self.dSkill = data.get("dSkill1", {})        # 技能数据
        self.Load(data.get("dData", {}))

    #登录初始化下发数据
    def to_init_dict(self):
        init_dict = {}
        init_dict["id"] = self.owner.data.id
        init_dict["name"] = self.owner.data.name
        init_dict["wxId"] = self.wxId
        init_dict["telNum"] = self.telNum
        init_dict["areaWXID"] = self.areaWXID
        init_dict["coin"] = self.coin
        init_dict["headPic"] = self.headPic
        init_dict["realname"] = self.realname
        init_dict["lv"] = self.lv
        init_dict["exp"] = self.exp
        init_dict["curexp"] = self.curexp
        init_dict["diamond"] = self.diamond
        init_dict["gender"] = self.gender
        init_dict["iClass"] = self.iClass
        init_dict["dSkill1"] = self.dSkill
        init_dict["dData"] = self.Save()
        return init_dict

    # 基本个人信息
    def to_base_dict(self):
        init_dict = {}
        init_dict["id"] = self.owner.data.id
        init_dict["name"] = self.owner.data.name
        init_dict["headPic"] = self.headPic
        init_dict["lv"] = self.lv
        init_dict["wxId"] = self.wxId
        init_dict["gender"] = self.gender
        init_dict["iClass"] = self.iClass
        return init_dict

    # 战斗属性
    def to_base_fight(self):
        init_dict = {}
        init_dict["id"] = self.owner.data.id
        init_dict["name"] = self.owner.data.name
        init_dict["wxId"] = self.wxId
        init_dict["coin"] = self.coin
        init_dict["lv"] = self.lv
        init_dict["exp"] = self.exp
        init_dict["curexp"] = self.curexp
        # init_dict["lift"] = self.lift           # 多少条命
        # init_dict["speed"] = self.speed         # 速率
        # init_dict["power"] = self.power         # 威力
        init_dict["gender"] = self.gender
        init_dict["dSkill"] = self.owner.packSkilltoFight()         # 技能数据
        # init_dict["paopaocount"] = self.paopaocount     # 范围
        return init_dict


    # 打包技能数据
    def packSkillToFight(self):

        pass


    def to_after_buy(self):
        init_dict = {}
        init_dict["id"] = self.owner.data.id
        init_dict["coin"] = self.coin
        init_dict["diamond"] = self.diamond
        return init_dict

    def to_reflash_simple(self):
        init_data = {}
        init_data["coin"] = self.coin
        init_data["diamond"] = self.diamond
        init_data["lv"] = self.lv
        init_data["exp"] = self.exp
        init_data["curexp"] = self.curexp
        return init_data


    def to_base_property(self):

        pass

    def claanAll(self):
        self.coin = 0       # 金币
        self.diamond = 0    # 钻石
        self.lv = 1         # 等级
        self.exp = 0        # 经验
        self.curexp = 0     # 当前经验
        self.gender = 0     # 性别

        # 战斗属性
        self.lift = 1        # 多少条命
        self.speed = 1       # 速率
        self.power = 1       # 威力
        self.paopaocount = 1 # 范围

        self.iClass = 1      # 角色
        self.dSkill = {}     # 技能数据
        self.dData = {}     # 用來存放可伸缩持久化数据，包括容器数据
        self.save_cache= {} #存储缓存
        pass