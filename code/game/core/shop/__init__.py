#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'
# from game.common.ctn import CPstContainerBase
from game.common.utility import *
import game.mgr.player
import time
from game import Game
import weakref
from game.define.shop_define import *

ONE_DAY_SEC = 60 * 60 * 24  # 一天的秒数
MAX_AMOUNT = 999

if not globals().has_key("giShopId"):
    giShopId = 0

# 商品基础类
# 已经被购买过的物品才会有
class CShopItem(CEasyPersist):
    def __init__(self, iNo, owner=None):
        super(CShopItem, self).__init__()
        global giShopId
        giShopId += 1
        self.iUID = giShopId
        self.iNo = iNo
        self.OwnerObj = None
        self.iOwner = 0 #拥有者id
        self.iNum = 1
        self.ihasBuyCount = 0 #已经被购买的次数
        self.iBirthday = int(time.time()) #生成时间
        self.shopTranceNo = ""
        self.endTime = 0 #过期时间
        self.shopDataRes = None # 商品数据表对象
        self.isGet = 0 # 是否已拥有
        self.cycleDay = CycleDay(self)  # 天周期数据
        self.cycleWeek = CycleWeek(self)  # 周周期数据
        self.cycleMonth = CycleMonth(self)  # 月周期数据
        if owner:
            self.set_owner(owner)

    def UID(self):
        return self.iUID

    def No(self):
        return self.iNo

    def SetNo(self, iNo):
        self.iNo = iNo

    # 物品ID
    def itemId(self):
        return self.shopDataRes.iItemId

    # 购买物品数量
    def buyitemNum(self):
        return self.shopDataRes.iBuyitemNum

    # 商品名称
    def Name(self):
        return self.shopDataRes.sName

    # 商品类型
    def Type(self):
        return self.shopDataRes.iType

    # 购买类型
    def buyType(self):
        return self.shopDataRes.iBuyType

    # 支付类型 1：金币，2：钻石，3：播放广告次数
    def PayType(self):
        return self.shopDataRes.iPayType

    # 需要金币数
    def NeedCoin(self):
        return self.shopDataRes.iNeedCoin

    # 需要钻石
    def NeedDiamond(self):
        return self.shopDataRes.iNeedDiamond

    # 需要播放广告数量
    def NeedADTime(self):
        return self.shopDataRes.iNeedADTime

    # 购买次数
    def buycount(self):
        return self.shopDataRes.iBuycount

    # 结束时间
    def endTime(self):
        return self.shopDataRes.sEndTime

    # 商品描述
    def sDesc(self):
        return self.shopDataRes.desc

    def Res(self):
        return self.shopDataRes.sRes

    def ClearDirtyFlag(self):  # override
        self.dirty = False

    def set_owner(self, owner):
        self.OwnerObj = owner
        if not self.shopTranceNo:
            self.iOwner = self.OwnerObj.id
            self.shopTranceNo = "%s-%s"%(self.iOwner, self.OwnerObj.data.GenerateShopTranceNo())
            self.MarkDirty()

    def MarkDirty(self):
        super(CShopItem, self).markDirty()
        who = self.getOwnerObj()
        if who:
            who.shop.MarkDirty()
        pass



    def OnBorn(self, who, isInit=False, *tArgs):
        self.iBirthday = GetDayNo()  # 生产日期
        self.shopDataRes = Game.res_mgr.res_shopData.get(self.iNo, None) # 读取数据

        if who:
            self.OwnerObj = who
        # print "------------item onBorn", self.iNo, self.shopDataRes, dir(self.shopDataRes), self.itemId()
        # import traceback
        # traceback.print_stack()
        # if isInit:
        #     self.buyShopItem(who, self.No())
        self.MarkDirty()

    # override
    def Save(self):
        dData = {}
        dSuper = super(CShopItem, self).Save()
        if dSuper:
            dData["Sp"] = dSuper
        if self.iBirthday:
            dData["Bd"] = self.iBirthday
        # self.dData["iNo"] = self.iNo
        dData["shopTranceNo"] = self.shopTranceNo
        dData["iOwner"] = self.iOwner
        dData["endTime"] = self.endTime
        dData["ihasBuyCount"] = self.ihasBuyCount
        dData["isGet"] = self.isGet
        dData["cycleDay"] = self.cycleDay.to_save_bytes()
        dData["cycleWeek"] = self.cycleWeek.to_save_bytes()
        dData["cycleMonth"] = self.cycleMonth.to_save_bytes()
        return dData

    def SaveEx(self):
        dData = self.Save()
        dData["UID"] = self.iUID
        return dData

    def OnRemove(self):
        pass

    # override
    def Load(self, dData):
        super(CShopItem, self).Load(dData.get("Sp", {}))
        # print "-------------item Load",dData
        self.iBirthday = dData.get("Bd", 0)
        self.shopTranceNo = dData.get("shopTranceNo", "")
        self.iOwner = dData.get("iOwner", 0)
        self.iNum = dData.get("iNum", self.iNum)
        self.endTime = dData.get("endTime", "")
        self.ihasBuyCount = dData.get("ihasBuyCount", 0) #已经被购买的次数
        self.isGet = dData.get("isGet", 1)
        self.cycleDay.load_from_dict(dData.get("cycleDay", ""))
        self.cycleWeek.load_from_dict(dData.get("cycleWeek", ""))
        self.cycleMonth.load_from_dict(dData.get("cycleMonth", ""))
        self.shopDataRes =  Game.res_mgr.res_shopData.get(self.iNo, None)
        print "--->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>-cycleDay--:",self.cycleDay,self.getDayHasBuyCount(),self.getWeekHasBuyCount()


    def Setup(self, bIsLoad, who):
        pass

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


    # 添加已购买次数
    def addHasBuyCount(self):
        self.ihasBuyCount += 1

    # 获取已购买次数
    def getHasBuyCount(self):
        return self.ihasBuyCount

    # 添加天已购买次数
    def addDayHasBuyCount(self):
        iDayBuyCount = self.cycleDay.Query("DayBuyCount",0)
        iDayBuyCount += 1
        self.cycleDay.Set("DayBuyCount", iDayBuyCount)

    # 获取天已购买次数
    def getDayHasBuyCount(self):
        iDayBuyCount = self.cycleDay.Query("DayBuyCount", 0)
        return iDayBuyCount

    # 添加周已购买次数
    def addWeekHasBuyCount(self):
        iWeekBuyCount = self.cycleWeek.Query("WeekBuyCount",0)
        iWeekBuyCount += 1
        self.cycleWeek.Set("WeekBuyCount", iWeekBuyCount)

    # 获取周已购买次数
    def getWeekHasBuyCount(self):
        iWeekBuyCount = self.cycleWeek.Query("WeekBuyCount", 0)
        return iWeekBuyCount


    def setIsGet(self, bGet=0):
        self.isGet = bGet

    # 获取可以购买次数
    def canBuyCount(self):
        leftCount = self.buycount() - self.getHasBuyCount()
        if leftCount < 0:
            leftCount = 0
        return leftCount

    # 检测商品是否可购买
    def checkItemCanBuy(self):
        if self.buyType() == BUY_TYPE.NOT_LIMIT:
            return True
        elif self.buyType() == BUY_TYPE.HAS_LIMIT:
            if  self.buycount() > self.getHasBuyCount():
                return True
        elif self.buyType() == BUY_TYPE.DAY_LIMIT:
            if  self.buycount() > self.getDayHasBuyCount():
                return True
        elif self.buyType() == BUY_TYPE.WEEK_LIMIT:
            if  self.buycount() > self.getWeekHasBuyCount():
                return True
        elif self.buyType() == BUY_TYPE.TIME_LIMIT:
            return False
        return False

    # 购买道具
    def buyShopItem(self, who, iNo):
        if iNo != self.No():
            who.notify("购买商品与已有数据不一致")
        self.addHasBuyCount()
        if self.buyType() == BUY_TYPE.DAY_LIMIT:
            self.addDayHasBuyCount()
        if self.buyType() == BUY_TYPE.WEEK_LIMIT:
            self.addWeekHasBuyCount()
        if self.buyType() == BUY_TYPE.SERVER_DAY_LIMIT:
            addServerHasBuyCount(iNo)
        self.addItemToBag()

    # 添加物品到背包里
    def addItemToBag(self):
        itemId = self.itemId()
        num = self.buyitemNum()
        game.core.item.net.AddItem(self.OwnerObj, itemId, num)

    # 结束时间
    def getEndTime(self):
        return 0


def Create(iNo, owner=None, num=1):
    obj = New(iNo, owner, num)
    return obj

def New(iNo, who=None, *tArgs):
    obj = CShopItem(iNo, who)
    obj.OnBorn(who, *tArgs)
    return obj

def Load(iNo, dData, owner):
    if Game.res_mgr.res_shopData.get(iNo, None):
        obj = New(iNo, owner)
        obj.Load(dData)
        return obj
    else:
        return None


# 购买商品
# 如果已经购买过，在已购买对象上继续操作
def BuyItem(iNo, owner=None, num=1):
    if not owner:
        return
    shopInfoData = Game.res_mgr.res_shopData.get(iNo, None)
    if not shopInfoData:
        owner.notify("物品ID：%s有误"%(iNo))
        return
    PayType = shopInfoData.PayType() # 支付类型 1：金币，2：钻石，3：播放广告次数
    if PayType == PAY_TYPE.COIN_PAY: # 金币支付
        own_coin = owner.base.getCoin()
        needcoin = shopInfoData.NeedCoin()
        # print "----------->>><<>><><> needcoin",own_coin,needcoin
        owner.base.setCoin((-1*needcoin))
    elif PayType == PAY_TYPE.DIAMOND_PAY: # 钻石支付
        own_diamond = owner.base.getDiamond()
        needdiamond = shopInfoData.NeedDiamond()
        owner.base.setDiamond((-1*needdiamond))

    shopObj = owner.shop.GetItemByNo(iNo)
    if shopObj:
        if not shopObj.checkItemCanBuy():
            shopName = shopObj.Name()
            # owner.notify("%s,已达到最大购买上限！"%shopName)
            return
        shopObj.buyShopItem(owner, iNo)
    else:
        print "------BuyItem---111-",iNo, owner, num
        shopObj = New(iNo, owner, num)
        shopObj.buyShopItem(owner, iNo)
        owner.shop.AddItem(shopObj)
        shopObj.setIsGet(1)
        owner.save(forced=True)
    return shopObj

# 播放视频回调，检测是否达到播放要求
def playVidioFinish(who, iNo):
    shopInfoData = Game.res_mgr.res_shopData.get(iNo, None)
    buyType = shopInfoData.buyType() # 购买类型 1：没限制，2:有限制, 3:天限制, 4:周限制, 5:时间限制
    PayType = shopInfoData.PayType()
    NeedADTime = shopInfoData.NeedADTime()
    if PayType != 3:
        return False
    sObj = who.shop.GetItemByNo(iNo)
    if buyType == BUY_TYPE.NOT_LIMIT:
        res = playADNoLimit(who, iNo, NeedADTime) # 检测广告播放次数
        if res and checkcanBuy(who, iNo, sObj): # 检测购买次数
            return res
    elif buyType == BUY_TYPE.HAS_LIMIT:
        res = playADHasLimit(who, iNo, NeedADTime)
        if res and checkcanBuy(who, iNo, sObj):
            return res
    elif buyType == BUY_TYPE.DAY_LIMIT:
        res = playADDayLimit(who, iNo, NeedADTime)
        if res and checkcanBuy(who, iNo, sObj):
            return res
    elif buyType == BUY_TYPE.WEEK_LIMIT:
        res = playADWeekLimit(who, iNo, NeedADTime)
        if res and checkcanBuy(who, iNo, sObj):
            return res
    return False

# 无限制
def playADNoLimit(who, iNo, NeedADTime=1):
    key = "shopAD_%s"%(iNo)
    playCount = who.Query(key)
    if not playCount:
        who.Set(key, 1)
    else:
        playCount += 1
    if playCount >= NeedADTime:
        who.Delete(key)
        return True
    return False

# 有总限制
def playADHasLimit(who, iNo, NeedADTime=1):
    key = "shopAD_%s"%(iNo)
    playCount = who.Query(key)
    if not playCount:
        who.Set(key, 1)
    else:
        playCount += 1
    if playCount >= NeedADTime:
        # who.Delete(key)
        return True
    return False
    pass

# 天限制
def playADDayLimit(who, iNo, NeedADTime=1):
    key = "shopAD_%s"%(iNo)
    playCount = who.cycleDay.Query(key)
    if not playCount:
        who.cycleDay.Set(key, 1)
    else:
        playCount += 1
    if playCount >= NeedADTime:
        print "---playADDayLimit:", playCount
        who.cycleDay.Set(key, playCount)
        return True
    return False

# 周限制
def playADWeekLimit(who, iNo, NeedADTime=1):
    key = "shopAD_%s"%(iNo)
    playCount = who.cycleWeek.Query(key)
    if not playCount:
        who.cycleWeek.Set(key, 1)
    else:
        playCount += 1
    if playCount >= NeedADTime:
        who.cycleWeek.Set(key, playCount)
        return True
    return False

# 购买商品检测
def checkcanBuy(who, iNo, shopObj=None):
    shopInfoData = Game.res_mgr.res_shopData.get(iNo, None)
    PayType = shopInfoData.PayType() # 支付类型 1：金币，2：钻石，3：播放广告次数
    if PayType == PAY_TYPE.COIN_PAY: # 金币支付
        own_coin = who.base.getCoin()
        if own_coin < shopInfoData.NeedCoin():
            who.notify("金币不足！")
            return False
        pass
    elif PayType == PAY_TYPE.DIAMOND_PAY: # 钻石支付
        own_diamond = who.base.getDiamond()
        if own_diamond < shopInfoData.NeedDiamond():
            who.notify("钻石不足!")
            return False

    buyType = shopInfoData.buyType() # 购买类型 1：没限制，2:有限制, 3:天限制, 4:周限制, 5:时间限制
    # 检测是否有限制
    LimitCount = shopInfoData.buycount()
    hasbuyCount = 0
    if buyType == BUY_TYPE.NOT_LIMIT:
        return True
    elif buyType == BUY_TYPE.HAS_LIMIT:
        if shopObj:
            hasbuyCount = shopObj.getHasBuyCount()
        if LimitCount > hasbuyCount:
            return True
        else:
            who.notify("不要重复购买哦！")
    elif buyType == BUY_TYPE.DAY_LIMIT:
        if shopObj:
            hasbuyCount = shopObj.getDayHasBuyCount()
        if LimitCount > hasbuyCount:
            return True
        else:
            who.notify("今天的购买次数已用完！")
    elif buyType == BUY_TYPE.WEEK_LIMIT:
        if shopObj:
            hasbuyCount = shopObj.getWeekHasBuyCount()
        if LimitCount > hasbuyCount:
            return True
        else:
            who.notify("这周的购买次数已用完！")
    return False


# 扣除服务器每天可购买次数
def addServerHasBuyCount(iNo):
    num = Game.rpc_server_info.cycDayGet("shop_%s"%(iNo))
    if num > 0:
        pass
    num = num - 1
    Game.rpc_server_info.cycDaySet("shop_%s" % (iNo), num)



import game.core.item.net
from game.core.cycleData import CycleDay, CycleWeek, CycleMonth, CycleHour, CycleCustom
