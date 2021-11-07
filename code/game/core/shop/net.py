#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from game.common.ctn import CPstContainerBase
from game.common.utility import *
import game.mgr.player
import time
from game import Game

from corelib.message import observable
from corelib import spawn_later, log, spawn
from corelib.gtime import current_time
from game import Game
from game.define.shop_define import *
from game.define.errcode import *


ALL_TYPE = 0 # 全部道具
NORMAL_TYPE = 1 # 普通道具
PAOPAOSHOW_TYPE = 2 # 泡泡外观道具
PAOPAOEFFECT_TYPE = 3 # 泡泡爆炸效果道具




# 购买商品
def BuyItem(who, iNo, num=1):
    print "------------------iNo:",iNo
    shopobj = game.core.shop.BuyItem(iNo, who, num)
    print "------------------BuyItem:",shopobj
    return shopobj



# @observable
class netCmd(object):
    # 协议处理模块
    def __init__(self):
        self.shopDataRes = Game.res_mgr.res_shopData  # 商品表
        self.res_lShopDataByType = Game.res_mgr.res_lShopDataByType
        pass


    # 获取商城信息
    # ALL_TYPE = 0  # 全部商品
    # NORMAL_TYPE = 1  # 普通商品
    # PAOPAOSHOW_TYPE = 2  # 泡泡外观商品
    # PAOPAOEFFECT_TYPE = 3  # 泡泡爆炸效果商品
    def rc_openShopUI(self, who, iType):
        if not who:who = self
        shopType = iType
        lShopList = self.shopDataRes.values()
        # print "res_lShopDataByType:",self.shopDataRes,lShopList, self.res_lShopDataByType.keys()
        if shopType > 0:
            lShopList = self.res_lShopDataByType.get(shopType,[])
        lShopInfo = []
        for shopObj in lShopList:
            iNo = shopObj.No()
            sObj =  who.shop.GetItemByNo(iNo)
            if sObj:
                shopObj = sObj # 已经购买过的物品
            # print shopObj.No(), shopObj.Name()
            # print "shopObj.Type()",shopObj.Type(),shopObj.canBuyCount()
            shopItemInfo = {
                "iNo": shopObj.No(),                    # 商品ID
                # "sName": shopObj.Name(),                # 名字
                "iType": shopObj.Type(),                # 类型 0：全部商品， 1：普通商品， 2：泡泡外观商品， 3：泡泡爆炸效果商品
                "buyType": shopObj.buyType(),           # 购买类型 1：没限制，2:有限制, 3:天限制, 4:周限制, 5:时间限制，6:日每天限制
                "payType": shopObj.PayType(),           # 支付类型 1：金币，2：钻石，3：播放广告次数
                "NeedCoin": shopObj.NeedCoin(),         # 需要金币数
                "NeedDiamond": shopObj.NeedDiamond(),   # 需要钻石
                "NeedADTime": shopObj.NeedADTime(),     # 需要播放广告数量
                "canBuyCount": shopObj.canBuyCount(),   # 可购买次数, 可购买次数为0时，道具要有灰色蒙版盖着(购买类型为1的时候，这个字段不用显示)
                # "sRes": shopObj.Res(),                  # 资源
                # "sDes": shopObj.sDesc(),                # 物品描述
                "iEndTime": shopObj.getEndTime()        # 剩余多少时间
            }
            lShopInfo.append(shopItemInfo)
        dData = {
                "lShopInfo": lShopInfo, # 商品列表
                "oepnType": iType # 打开类型
            }
        return dData


    # 购买物品
    # iNo 物品表ID
    # iType 标签类型
    # num 购买数量
    def rc_Buy(self, who, iNo, iType, num=1):
        # BuyItem
        # print "----------------1111111111111111111111",iNo
        if not who:who = self
        iNo = int(iNo)
        iType = int(iType)
        num = int(num)
        shopInfoData = self.shopDataRes.get(iNo)    # 产品数据
        sObj = who.shop.GetItemByNo(iNo)            # 已购买对象
        # print "-----------sObj",sObj.No(), sObj.Name()
        if not shopInfoData:
            who.notify("购买物品ID不对")
            try:
                Game.glog.log2File("rc_Buy_ERR",
                                   "%s|%s|%s|%s|%s" % (
                                       self.id, self.Name(), self.data.account, iNo, iType))
            except:
                pass
            return {"iNo": iNo,"err": EC_BUY_ERROR}
        iPayType = shopInfoData.PayType() # 支付类型
        canBuy = False
        if iPayType == PAY_TYPE.VIDIO_PAY: # 播放视频
            canBuy = self.rc_playerVidio(who, iNo)
        else:
            canBuy = game.core.shop.checkcanBuy(who,iNo,sObj)
        # print "--------------canBuy------",canBuy
        if canBuy:
            shopobj = BuyItem(who, int(iNo), int(num))
            if not shopobj:
                return {"iNo": iNo,"err": EC_BUY_ERROR}
            else:
                shopName=shopobj.Name()
                print shopobj
                who.notify("获得:%s"%shopName)

        dData = self.rc_openShopUI(who, iType) # 主动推刷新商城UI
        who.broadcast("openShopUI", dData)
        after_buy_data =  who.base.to_after_buy() # 金币，钻石数量
        try:
            Game.glog.log2File("rc_Buy_SUCC",
                               "%s|%s|%s|%s|%s" % (
                                   self.id, self.Name(), self.data.account, iNo, iType))
        except:
            pass
        return {"iNo": iNo, "after_buy_data": after_buy_data,"err": EC_OK}


    # 播放广告购买
    def rc_playerVidio(self, who, iNo):
        if not who:who = self
        shopInfoData = self.shopDataRes.get(iNo)
        if not shopInfoData:
            return {"iNo": iNo,"err": EC_BUY_ERROR}
        # canBuy = game.core.shop.playVidioFinish(who, iNo)
        canBuy = True
        if not canBuy:
            who.notify("请观看视频购买")
        return canBuy



    # 播放广告购买回调
    def rc_playerVidioCallBack(self, who, iNo, iType):
        if not who:who = self
        shopInfoData = self.shopDataRes.get(iNo)
        if not shopInfoData:
            return {"iNo": iNo,"err": EC_BUY_ERROR}
        canBuy = game.core.shop.playVidioFinish(who, iNo)
        dData = {}
        if canBuy:
            # 播放完毕，可以购买
            dData = self.rc_Buy(who, iNo, 1)
        else:
            # 还有播放条件没达到，刷新UI
            dData = self.rc_openShopUI(who, iType)
        return dData # 刷新商城UI








import game.core.shop