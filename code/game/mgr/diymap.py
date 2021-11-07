#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from game.common import utility

from corelib.frame import Game, MSG_FRAME_STOP
from game.models.diymap import ModelDiyMap
from corelib.gtime import get_days
from game.common.utility import *



class DiyMapInfo(utility.DirtyFlag):
    """diy地图"""
    _rpc_name_ = 'rpc_diymap_info'

    def __init__(self):
        utility.DirtyFlag.__init__(self)
        self.data = None
        self.dMapInfo = {} # pid:mapinfo
        self.mapTranceNo = 1000

        self.save_cache = {}  # 存储缓存

        Game.sub(MSG_FRAME_STOP, self._frame_stop)

    def start(self):
        print ">>>>>>>>>>>>>> DiyMapInfo stat <<<<<<<<<<<<<<<<"
        self.data = ModelDiyMap.load(Game.store, ModelDiyMap.TABLE_KEY)
        # print self.data , self.data.dataDict
        print ">>>>>>>>>>>>>> DiyMapInfo stat <<<<<<<<<<<<<<<< 2"
        if not self.data:
            self.data = ModelRank()
            self.data.set_owner(self)
            self.data.save(Game.store, forced=True)
        else:
            self.data.set_owner(self)
        self.load_from_dict(self.data.dataDict)

    def _frame_stop(self):
        self.data.save(Game.store, forced=True, no_let=True)

    # 存库数据
    def to_save_dict(self, forced=False):
        if self.isDirty() or forced or not self.save_cache:
            self.save_cache = {}
            self.save_cache["dMapInfo"] = self.dMapInfo
            self.save_cache["mapTranceNo"] = self.mapTranceNo
        return self.save_cache

    # 读库数据初始化
    def load_from_dict(self, data):
        # print "-55555555555555-------load mapinfo data", data
        self.dMapInfo = data.get("dMapInfo", {})
        self.mapTranceNo = data.get("mapTranceNo", 1000)
        self.markDirty()

    def SaveMapInfo(self):
        self.data.save(Game.store, forced=True)

    def GeneraDiyMapTranceNo(self):
        self.mapTranceNo += 1
        self.data.modify()
        return self.mapTranceNo

    # 制作地图
    # roleId 角色ID
    # Type 地图类型
    # bgConf 背景配置
    # layerConf 装饰层配置
    # 'bgConf': [1, 24, 24, 1, 2, 2, 2, 1, 1, 1, 26, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 25, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 3, 3, 1, 1, 2, 2, 2],
    # 'layerConf': [119, 0, 7, 7, 16, 21, 16, 7, 7, 0, 0, 0, 4, 4, 20, 21, 4, 21, 20, 4, 4, 0, 0, 0, 9, 9, 16, 4, 16, 9, 9, 0, 0, 6, 19, 5, 5, 11, 4, 11, 5, 5, 16, 6, 6, 19, 5, 11, 0, 4, 0, 11, 5, 16, 6, 6, 19, 5, 5, 11, 4, 11, 7, 5, 16, 6, 0, 0, 0, 4, 16, 4, 16, 4, 0, 0, 0, 0, 4, 4, 4, 12, 19, 12, 4, 4, 4, 0, 0, 20, 20, 12, 16, 19, 16, 12, 20, 20, 120]}
    def makeDiyMap(self, roleId, Type, bgConf, layerConf):
        if not self.dMapInfo.has_key(roleId):
            self.dMapInfo[roleId] = {}
            mapkey = self.GeneraDiyMapTranceNo()
            makInfo = {
                'id':mapkey,
                'Type':Type,
                'bgconf':bgConf,
                'layerconf':layerConf
            }
            self.dMapInfo[roleId][mapkey] = makInfo
        else:
            mapkey = self.GeneraDiyMapTranceNo()
            makInfo = {
                'id':mapkey,
                'Type':Type,
                'bgconf':bgConf,
                'layerconf':layerConf
            }
            self.dMapInfo[roleId][mapkey] = makInfo
        self.markDirty()
        pass



