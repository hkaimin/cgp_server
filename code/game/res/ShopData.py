#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 名字库	名字
# int&key	string
# id	name


class ResShopData(object):
    RES_TABLE = "shopData"

    def __init__(self):
        self.id             = 0     # id
        self.iItemId        = 0     # 物品id
        self.iBuyitemNum    = 1     # 购买物品数量
        self.sName          = ""    # 名字
        self.iType          = 0     # 商品类型
        self.iBuyType       = 0     # 购买类型
        self.iBuycount      = 0     # 可购买次数
        self.iPayType       = 1     # 支付类型 1：金币，2：钻石，3：播放广告次数
        self.iNeedCoin      = 100   # 需要金币数
        self.iNeedDiamond   = 0     # 需要钻石
        self.iNeedADTime    = 0     # 需要播放广告数量
        self.sEndTime       = ""    # 结束时间
        self.sRes           = ""    # 资源名称
        self.desc           = ""    # 描述

    def load_from_json(self, data):
        self.id             = data.get("id", 0)
        self.iItemId        = data.get("itemId", 0)
        self.iBuyitemNum    = data.get("buyitemNum", 1)
        self.sName          = data.get("name", "")
        self.iType          = data.get("Type", 0)      # 类型 0：全部商品， 1：普通商品， 2：泡泡外观商品， 3：泡泡爆炸效果商品
        self.iBuyType       = data.get("buyType", 0)    # 购买类型 1：没限制，2:有限制, 3:天限制, 4:周限制, 5:时间限制
        self.iBuycount      = data.get("buycount", 0)
        self.iPayType       = data.get("payType", 0)    # 支付类型 1：金币，2：钻石，3：播放广告次数
        self.iNeedCoin      = data.get("coin", 0)       # 需要金币数
        self.iNeedDiamond   = data.get("diamond", 0)    # 需要钻石
        self.iNeedADTime    = data.get("ad", 0)         # 需要播放广告数量
        self.sEndTime       = data.get("endTime", "")
        self.sRes           = data.get("res", "")
        self.desc           = data.get("desc", "")


    def No(self):
        return self.id

    # 物品ID
    def itemId(self):
        return self.iItemId

    # 购买物品数量
    def buyitemNum(self):
        return self.iBuyitemNum

    # 商品名称
    def Name(self):
        return self.sName

    # 商品类型
    def Type(self):
        return self.iType

    # 购买类型
    def buyType(self):
        return self.iBuyType

    # 购买次数
    def buycount(self):
        return self.iBuycount

    # 支付类型 1：金币，2：钻石，3：播放广告次数
    def PayType(self):
        return self.iPayType

    # 需要金币数
    def NeedCoin(self):
        return self.iNeedCoin

    # 需要钻石
    def NeedDiamond(self):
        return self.iNeedDiamond

    # 需要播放广告数量
    def NeedADTime(self):
        return self.iNeedADTime

    # 结束时间
    def endTime(self):
        return self.sEndTime

    # 商品描述
    def sDesc(self):
        return self.desc

    def Res(self):
        return self.sRes

    def canBuyCount(self):
        return self.buycount()

    def getEndTime(self):
        return 0