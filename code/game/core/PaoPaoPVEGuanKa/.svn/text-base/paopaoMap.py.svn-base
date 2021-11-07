#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import random
from gevent import sleep
from corelib import spawn, log, spawn_later
from game.define import errcode
from game import Game
from game.common import utility
import config
import random
import copy
import game.core.PaoPaoPVP.paopaoMap


P1_KEY = 119
P2_KEY = 120
WIDTH = 9
HIGH = 7




class PaopaoMap(object):
    def __init__(self, barrierNo=0, isTrain=0):
        print "------------------PaopaobarrierNo", barrierNo
        self.mapBase = Game.res_mgr.res_mapBase
        # self.mayType = self.mapConfObj.Type

        self.itemSpeed = 0 # 速度道具数量
        self.itemNum = 0 # 泡泡数量道具
        self.itemPower = 0 # 泡泡威力道具
        self.itemLife = 0 # 增加生命道具
        self.itemDestory = 0 # 刺穿泡泡道具
        self.itemDef = 0 # 防护罩道具
        self.barrTime = 0 # 总游戏时常
        self.aiNum = 0 # ai数量
        self.MapInfo = {}
        self.dEffectItem = {} #当前可捡取的{道具类型：num}
        self.barrierNo = barrierNo
        self.bgconf = []
        self.layerconf = []
        self.isTrain = isTrain
        self.lGuanKaDoorIdx = []
        if self.isTrain:
            self.mapConfObj = Game.res_mgr.res_mapConf.get(self.barrierNo, None)
        else:
            self.mapConfObj = Game.res_mgr.res_wujinInstData.get(self.barrierNo, None)
        self.bgconf = self.mapConfObj.bgconf
        self.layerconf = copy.copy(self.mapConfObj.layerconf)
        self.init()
        pass

    def init(self):
        self.itemSpeed = self.mapConfObj.itemSpeed
        self.itemNum = self.mapConfObj.itemNum
        self.itemPower = self.mapConfObj.itemPower
        self.itemLife = self.mapConfObj.itemLife
        self.itemDestory = self.mapConfObj.itemDestory
        self.itemDef = self.mapConfObj.itemDef
        self.barrTime = self.mapConfObj.barrTime
        self.lGuanKaDoorIdx = self.mapConfObj.lGuanKaDoorIdx
        self.aiNum = 1#self.mapConfObj.aiNum
        x = 0
        y = 0
        for i, mid in enumerate(self.layerconf):
            x = i%9
            y = i/7
            self.MapInfo[i] = {"mid":mid, "x":x, "y":y}
        print "self.MapInfo:",self.MapInfo
        pass

    def getWalkArea(self, idx):
        lWalkArea = [3,3]
        try:
            lWalkArea = self.mapConfObj.lMonsterArea[idx]
        except:
            pass
        return lWalkArea


    # 消除障碍物
    def breakMap(self, idx):
        if idx > len(self.layerconf):
            return {"err": errcode.EC_ZHUANIDX_NOT_EXIST}
        mapid = self.layerconf[idx]
        if not mapid:
            return {"err":errcode.EC_ZHUANIDX_NOT_EXIST}
        mapBaseObj = self.mapBase.get(mapid)
        if mapBaseObj.canBreak():
            self.layerconf[idx] = 0
            self.MapInfo[idx]['mid'] = 0
            return self.baoItem(idx)

    # 爆道具
    # 速度 Type : 1
    # 泡泡数量道具 Type : 2
    # 泡泡威力道具 Type : 3
    # 添加生命道具 Type : 4
    # 屎道具 Type : 5
    # 问号道具 Type : 6
    def baoItem(self, idx):
        print "--------------baoItem---<<<<<<<1111<", idx
        if idx in self.lGuanKaDoorIdx: # 通关门
            self.addEffectItem(idx, CFightToolType.DOOR, 1)
            return {'type': CFightToolType.DOOR,
                    'num': 1,
                    'err': errcode.EC_OK}
        if self.itemSpeed > 0: # 速度
            speedPer = self.mapConfObj.itemSpeedPer
            print "--------speedPer--",speedPer
            isSpeed = RandomKey({1:speedPer}, 100)#random.randint(0, 1)
            if isSpeed:
                self.itemSpeed -= 1
                self.addEffectItem(idx, 1, 1)
                return {'type':CFightToolType.SPEED,
                        'num':1,
                        'err':errcode.EC_OK}
        if self.itemNum > 0: # 泡泡数量道具
            itemNumPer = self.mapConfObj.itemNumPer
            print "--------itemNumPer--", itemNumPer
            isitemNum = RandomKey({1:itemNumPer}, 100)#random.randint(0, 1)
            if isitemNum:
                self.itemNum -= 1
                # self.dEffectItem[2] += 1
                self.addEffectItem(idx, 2, 1)
                return {'type':CFightToolType.NUM,
                        'num':1,
                        'err': errcode.EC_OK}
        if self.itemPower > 0: # 泡泡威力道具
            itemPowerPer = self.mapConfObj.itemPowerPer
            print "--------itemPowerPer--", itemPowerPer
            isitemPower = RandomKey({1:itemPowerPer}, 100)#random.randint(0, 1)
            if isitemPower:
                self.itemPower -= 1
                # self.dEffectItem[3] += 1
                self.addEffectItem(idx, 3, 1)
                return {'type':CFightToolType.POWER,
                        'num':1,
                        'err': errcode.EC_OK}
        return {'err': errcode.EC_OK}
    # def baoItem(self, idx):
    #     if self.itemSpeed > 0: # 速度
    #         isSpeed = random.randint(0, 1)
    #         if isSpeed:
    #             self.itemSpeed -= 1
    #             self.addEffectItem(idx, 1, 1)
    #             return {'type':1,
    #                     'num':1,
    #                     'err':errcode.EC_OK}
    #     if self.itemNum > 0: # 泡泡数量道具
    #         isitemNum = random.randint(0, 1)
    #         if isitemNum:
    #             self.itemNum -= 1
    #             # self.dEffectItem[2] += 1
    #             self.addEffectItem(idx, 2, 1)
    #             return {'type':2,
    #                     'num':1,
    #                     'err': errcode.EC_OK}
    #     if self.itemPower > 0: # 泡泡威力道具
    #         isitemPower = random.randint(0, 1)
    #         if isitemPower:
    #             self.itemPower -= 1
    #             # self.dEffectItem[3] += 1
    #             self.addEffectItem(idx, 3, 1)
    #             return {'type':3,
    #                     'num':1,
    #                     'err': errcode.EC_OK}
    #     return {'err': errcode.EC_OK}

    # 添加/删除 地图道具
    def addEffectItem(self, idx, iType, num=1):
        if not self.dEffectItem.has_key(iType):
            self.dEffectItem[iType] = {}
        onum = self.dEffectItem[iType].get('num', 0)
        if num > 0: # 增加
            self.dEffectItem[iType]['num'] = onum + num
            if not self.dEffectItem[iType].get('idx'):
                self.dEffectItem[iType]['idx'] = []
            self.dEffectItem[iType]['idx'].append(idx)
        elif num < 0 and onum > 0: #减少
            self.dEffectItem[iType]['num'] = onum + num
            if self.dEffectItem[iType].get('idx') and idx in self.dEffectItem[iType].get('idx'):
                index = self.dEffectItem[iType]['idx'].index(idx)
                if index:
                    self.dEffectItem[iType]['idx'].pop(index)


    # 获取地图是否有掉落道具
    def isHasEffectItem(self, idx, iType):
        if not self.dEffectItem.has_key(iType):
            return False
        if idx not in self.dEffectItem[iType]['idx']:
            return False
        onum = self.dEffectItem[iType].get('num', 0)
        if onum <= 0:
            return False
        else:
            return True

    # 吃道具
    def eatEffectItem(self, idx, iType):
        isHas = self.isHasEffectItem(idx, iType)
        if not isHas:
            return isHas
        num = -1
        onum = self.dEffectItem[iType].get('num', 0)
        if onum > 0:
            self.addEffectItem(idx, iType, num)
            return True
        return False


    def hasMapidx(self, idx):
        # try:
        if idx > len(self.layerconf):
            return False
        mapid = self.layerconf[idx]
        if not mapid:
            return False
        mapBaseObj = self.mapBase.get(mapid)
        if mapid and mapBaseObj:
            return True
        else:
            return False
        # except:
        #     return False



    def Id(self):
        return self.mapConfObj.id

    def getBGConf(self):
        return self.bgconf

    def getlayerconf(self):
        return self.layerconf

    def getBaseObj(self, id):
        return self.mapBase.get(id)

    def get_p1_idx(self):
        return self.getlayerconf().index(P1_KEY)

    def get_p2_idx(self):
        if P2_KEY not in self.getlayerconf():
            return 0
        return self.getlayerconf().index(P2_KEY)

    def mapType(self):
        return self.mayType


from game.common.utility import *
from game.define.constant import *