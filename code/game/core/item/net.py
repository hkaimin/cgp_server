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
from game.define.bag_define import *

# ALL_TYPE = 0 # 全部道具
# NORMAL_TYPE = 1 # 普通道具
# PAOPAOSHOW_TYPE = 2 # 泡泡外观道具
# PAOPAOEFFECT_TYPE = 3 # 泡泡爆炸效果道具




# 增加道具
def AddItem(who, iNo, num=1):
    print "------------------iNo:",iNo
    itemobj = game.core.item.CloneItem(iNo, who, num)
    print "------------------AddItem:",itemobj
    return itemobj



class netCmd(object):
    # 协议处理模块
    def __init__(self):
        pass

    # 增加道具
    def AddItem(self, who, iNo, num=1):
        print "------------------iNo:",iNo
        itemobj = game.core.item.Create(iNo, who, num)
        print "------------------itemobjitemobj:",itemobj
        who.bag.AddItem(itemobj)
        who.save(forced=True)
        return itemobj

    # 显示全部道具
    def getAllItem(self, who, iType=0):
        return who.bag.getAllItem()

    # 获取背包物品
    # ALL_TYPE = 0  # 全部道具
    # NORMAL_TYPE = 1  # 普通道具
    # PAOPAOSHOW_TYPE = 2  # 泡泡外观道具
    # PAOPAOEFFECT_TYPE = 3  # 泡泡爆炸效果道具
    def rc_openBagUI(self, who, iType):
        if not who:who=self
        lallItem = []
        if iType == BAG_TYPE.ALL_TYPE:
            lallItem = who.bag.getAllItem()
        else:
            lallItem = who.bag.getItemListByType(iType)
        lItmeInfo = []
        for itemObj in lallItem:
            itemInfo = {
                "iNo": itemObj.No(),  # 道具ID
                "iItemID": itemObj.UID(),  # 道具内存ID
                "sName": itemObj.Name(),  # 名字
                "iType": itemObj.Type(),  # 类型
                "sRes": itemObj.Res(),  # 资源
                "iNum": itemObj.Num(),  # 道具数量
                "sDes": itemObj.Des(),  # 物品描述
                "iIsTimeLimit": itemObj.IsTimeLimit(),  # 是否限时道具
                "iEndTime": itemObj.getEndTime()  # 剩余多少时间
            }
            lItmeInfo.append(itemInfo)
        #print lItmeInfo,iType
        return {
            "lItmeInfo": lItmeInfo,
            "openType": iType
        }

    # 使用道具
    # iNo 道具表的id
    # iItemID 道具内存ID
    # iType 打开界面类型
        # ALL_TYPE = 0  # 全部道具
        # NORMAL_TYPE = 1  # 普通道具
        # PAOPAOSHOW_TYPE = 2  # 泡泡外观道具
        # PAOPAOEFFECT_TYPE = 3  # 泡泡爆炸效果道具
    def rc_useItem(self, who, iNo, iItemID, iType):
        itemObj = who.bag.GetItem(iItemID)
        if not itemObj:
            return {"err":"iItemID:%s is wrong!"%iItemID}
        if itemObj and iNo != itemObj.No():
            return {"err":"iNo:%s is wrong!"%iNo}
        itemObj.useItem(who)
        # 刷新界面UI
        dReflashData = who.base.to_reflash_simple()
        who.broadcast("reflashsimple", dReflashData)
        data = self.rc_openBagUI(who, iType)
        who.broadcast("openBagUI", data)
        who.notify("使用成功！")

        return {"err":"ok"}

    # 获取随机红包
    def getHongBao(self):
        # itemData = Game.res_mgr.res_itemData
        itemDataKey = [25,22,26,35,36,37,37,37,37,37,37,37,37,38,39,40,41,22,23,24,22,22,22]#itemData.keys()
        DataKey = random.choice(itemDataKey)
        itemObj = self.AddItem(self, DataKey, 1)
        itemName = itemObj.Name()
        self.notify("恭喜获得随机红包:%s" % itemName)
        try:
            Game.glog.log2File("getHongBao",
                               "%s|%s|%s" % (
                                   self.id, self.Name(), self.data.account))
            sStr = "恭喜%s获得随机红包:%s" % (self.Name(), itemName)
            self.rf_scrollNotice(sStr)
        except:
            pass
        return {DataKey:1}

import game.core.item