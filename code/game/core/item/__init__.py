#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'
# from game.common.ctn import CPstContainerBase
from game.common.utility import *
import game.mgr.player
import time
from game import Game
import weakref
import conf
import game.define.constant

ONE_DAY_SEC = 60 * 60 * 24  # 一天的秒数
MAX_AMOUNT = 999
# dKEYS = {1: "LIFE", 2: "SPEED", 3: "COUNT", 4: "POWER"}





if not globals().has_key("giTestLastId"):
    giTestLastId = 0

# 神兽基类定义
class CItem(CEasyPersist):
    def __init__(self, iNo, owner=None):
        super(CItem, self).__init__()
        global giTestLastId
        giTestLastId += 1
        self.iUID = giTestLastId
        self.iNo = iNo
        self.OwnerObj = None
        self.iOwner = 0 #拥有者id
        self.iNum = 0 #数量  默认为1
        self.iBirthday = int(time.time()) #生成时间
        self.itemTranceNo = ""
        self.endTime = 0 #过期时间
        self.itemDataRes = None # 物品数据表对象
        if owner:
            self.set_owner(owner)

    def ClearDirtyFlag(self):  # override
        self.dirty = False

    def SetNo(self, iNo):
        self.iNo = iNo

    def set_owner(self, owner):
        self.OwnerObj = owner
        if not self.itemTranceNo:
            self.iOwner = self.OwnerObj.id
            self.itemTranceNo = "%s-%s"%(self.iOwner, self.OwnerObj.data.GenerateItemTranceNo())
            self.MarkDirty()

    def MarkDirty(self):
        super(CItem, self).markDirty()
        who = self.getOwnerObj()
        if who:
            who.bag.MarkDirty()
        pass

    def UID(self):
        return self.iUID

    def OnBorn(self, who, *tArgs):
        self.iBirthday = GetDayNo()  # 生产日期
        self.itemDataRes = Game.res_mgr.res_itemData.get(self.iNo, None)
        if tArgs:
            num = tArgs[0]
            self.SetAmount(num)
        if who:
            self.OwnerObj = who
        print "------------item onBorn", self.iNo, self.iNum
        # import traceback
        # traceback.print_stack()
        self.MarkDirty()

    # override
    def Save(self):
        dData = {}
        dSuper = super(CItem, self).Save()
        if dSuper:
            dData["Sp"] = dSuper
        if self.iBirthday:
            dData["Bd"] = self.iBirthday
        # self.dData["iNo"] = self.iNo
        dData["itemTranceNo"] = self.itemTranceNo
        dData["iOwner"] = self.iOwner
        dData["iNum"] = self.iNum
        dData["endTime"] = self.endTime
        return dData

    def SaveEx(self):
        dData = self.Save()
        dData["UID"] = self.iUID
        return dData

    def OnRemove(self):
        pass

    # override
    def Load(self, dData):
        super(CItem, self).Load(dData.get("Sp", {}))
        # print "-------------item Load",dData
        self.iBirthday = dData.get("Bd", 0)
        self.itemTranceNo = dData.get("itemTranceNo", "")
        self.iOwner = dData.get("iOwner", 0)
        self.iNum = dData.get("iNum", self.iNum)
        self.endTime = dData.get("endTime", "")
        self.itemDataRes =  Game.res_mgr.res_itemData.get(self.iNo, None)

    def Setup(self, bIsLoad, who):
        pass

    def No(self):
        return self.iNo

    def Name(self):
        return self.itemDataRes.name

    def Type(self):
        return self.itemDataRes.itype

    def Res(self):
        return self.itemDataRes.res

    # 物品数量限制
    def MaxAmount(self):
        return self.itemDataRes.maxAmount

    # 描述
    def Desc(self):
        return self.itemDataRes.desc

    # 功能类型1 = 增加声明, 2 = 增加速度, 3 = 增加泡泡数量, 4 = 增加泡泡威力
    def SpType(self):
        return self.itemDataRes.spType

    #功能参数1（物品类型1：增加次数）
    def Param1(self):
        return self.itemDataRes.param1

    # 功能参数2（物品类型2：持续场数）
    def Param2(self):
        return self.itemDataRes.param2

    # 功能参数2（物品类型2：持续场数）
    # 功能类型1的时候代表生效的关卡类型{1:PVP,3:关卡}
    def Param3(self):
        return self.itemDataRes.param3

    def getGiftData(self):
        return self.itemDataRes.getGiftData()

    # 物品使用后持续周期
    def cycle(self):
        return self.itemDataRes.cycle

    # 被放入容器时的唯一标识
    def ContainerKey(self):
        return self.iUID

    def OwnerId(self):
        return self.iOwner

    def SetOwnerID(self, iOwner):
        self.iOwner = iOwner

    def getOwnerObj(self):
        if self.OwnerObj:
            return self.OwnerObj
        return game.mgr.player.get_rpc_player(int(self.iOwner))

    def RoleId(self):
        return self.iOwner

    def Birthday(self):
        return self.iBirthday

    def Num(self):
        return self.iNum

    def Des(self):
        return self.itemDataRes.desc

    def SetAmount(self, iAmount):
        if iAmount > self.MaxAmount():
            iRemain = iAmount - self.MaxAmount()
            iAmount = self.MaxAmount()
        else:
            iRemain = 0
        if iAmount > 0:
            self.iNum += iAmount
        if self.iNum > self.MaxAmount():
            self.iNum = self.MaxAmount()
        self.MarkDirty()
        return iRemain

    def canAdd(self, needAdd = 0):
        return (self.iNum + needAdd) < self.MaxAmount()

    # 是否限时道具
    def IsTimeLimit(self):
        return 0

    # 结束时间
    def getEndTime(self):
        return 0

    '''
    使用道具
    功能类型
      1 = 增加生命, 
      2 = 增加速度, 
      3 = 增加泡泡数量, 
      4 = 增加泡泡威力
    功能参数1（增加次数）
    功能参数2（持续场数）
    有效周期
    '''
    def useItem(self, who):
        if self.SpType(): # 功能道具
            pass
        if self.iNum <= 0:
            self.removeItem(who)
            return 0
        self.iNum -= 1 # 扣除数量
        dKEYS = {conf.CItemType.ADD_LIFE:"LIFE",
                 conf.CItemType.ADD_SPEED:"SPEED",
                 conf.CItemType.ADD_COUNT:"COUNT",
                 conf.CItemType.ADD_POWER:"POWER"}
        value = self.Param1()
        if self.SpType() in [conf.CItemType.ADD_LIFE,
                             conf.CItemType.ADD_SPEED,
                             conf.CItemType.ADD_COUNT,
                             conf.CItemType.ADD_POWER]: # 战斗特效类
            num = value
            times = self.Param2()
            cycle = self.cycle()
            fight_mode = self.Param3()
            # fight_mode = int(fight_mode)
            if not fight_mode:
                fight_mode = game.define.constant.APP_MODE_PVE_GUANKA
            else:
                fight_mode = int(fight_mode)
            KEY = dKEYS.get(self.SpType(), "")
            if KEY:
                who.addFightEffect(KEY, num, times, cycle, fight_mode)
        elif self.SpType() == conf.CItemType.ADD_COIN:
            who.base.setCoin(value)
        elif self.SpType() == conf.CItemType.ADD_DIAMOND:
            who.base.setDiamond(value)
        elif self.SpType() == conf.CItemType.ADD_DIY_MAP_CNT:
            who.addDiyMapCnt(value)
        elif self.SpType() == conf.CItemType.ADD_EXP:
            who.Upgrade(value)
        elif self.SpType() == conf.CItemType.ADD_LIKE:
            who.addLikeCnt(value)
        elif self.SpType() == conf.CItemType.PAO_PAO_SKIN:
            self.iNum = 1
            skin_id = value
            who.setUseSkin(skin_id)
        elif self.SpType() == conf.CItemType.BOX:
            num = self.Param1()
            giftData = self.getGiftData()
            openGiftBox(who, num, giftData)
            pass
        elif self.SpType() == conf.CItemType.UNLOCK_CLASS:
            # 解锁角色
            iClass = self.Param1()
            who.rc_buyClass(iClass, True)
            pass
        elif self.SpType() == conf.CItemType.UNLOCK_FUNC:
            # 解锁功能
            funcNo = str(self.Param1())
            subFunc = self.Param2()
            UnluckFunc = who.Query("UnlockFunc", {})
            if not UnluckFunc.has_key(funcNo):
                UnluckFunc[funcNo] = []
            if subFunc:
                if subFunc not in UnluckFunc.get(funcNo,[]):
                    UnluckFunc.append(subFunc)
            who.Set("UnlockFunc", UnluckFunc)
        elif self.SpType() == conf.CItemType.ADD_TILI: # 增加体力道具
            who.addTiliCnt(value, game.define.constant.CTili.TOOL_ADD)
        if self.iNum <= 0:
            # 没有数量的时候，删除对象
            self.removeItem(who)
            return 0
        return self.iNum

    def removeItem(self, who):
        itemCtn = who.bag
        itemCtn.RemoveItem(self)



if not globals().has_key("gdTestModule"):
    gdTestModule = {}

def Create(iNo, owner=None, num=1):
    obj = New(iNo, owner, num)
    return obj

def New(iNo, who=None, *tArgs):
    obj = CItem(iNo, who)
    obj.OnBorn(who, *tArgs)
    return obj

def Load(iNo, dData, owner):
    obj = New(iNo, owner)
    obj.Load(dData)
    return obj

# 添加道具，有cota, 就直接在原来对象上增加，无就New一个出来
def CloneItem(iNo, owner=None, num=1):
    if not owner:
        return
    itemObj = owner.bag.getItemCanAdd(iNo, num)
    if itemObj:
        itemObj.SetAmount(num)
    else:
        print "------CloneItem---111-",iNo, owner, num
        itemObj = New(iNo, owner, num)
        owner.bag.AddItem(itemObj)
        owner.save(forced=True)
    return itemObj

# 打开礼盒
def openGiftBox(who, openNum, giftData):
    print openNum, giftData, type(giftData)
    if not giftData:
        return
    lGet = []
    for i in xrange(openNum):
        itemID = RandomKey(giftData)
        lGet.append(itemID)
    print "lGet:", lGet
    if lGet:
        for igetID in lGet:
            obj = who.AddItem(who, igetID)
            who.notify("开宝箱获得:%s"%(obj.Name()))

import game.core.item.net
