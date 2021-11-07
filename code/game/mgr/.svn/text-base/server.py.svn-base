#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from game.common import utility

from corelib.frame import Game, MSG_FRAME_STOP
from game.models.server import ModelServer
from corelib.gtime import get_days
from game.core.cycleData import CycleDay, CycleWeek
from game.define.shop_define import *
from game.define import errcode,msg_define

class ServerInfo(utility.DirtyFlag):
    """服务器信息"""
    _rpc_name_ = 'rpc_server_info'

    def __init__(self):
        utility.DirtyFlag.__init__(self)
        self.data = None
        self.opentime = 0
        self.mergetime = 0

        self.save_cache = {}  # 存储缓存
        self.cycleDay = CycleDay(self)  # 天周期数据
        self.cycleWeek = CycleWeek(self)  # 周周期数据
        self.res_lShopDataByType = None
        Game.sub(MSG_FRAME_STOP, self._frame_stop)

    def start(self):
        self.data = ModelServer.load(Game.store, ModelServer.TABLE_KEY)
        if not self.data:
            self.data = ModelServer()
            self.data.set_owner(self)
            self.opentime = int(time.time())
            self.data.save(Game.store, forced=True)
        else:
            self.data.set_owner(self)
        self.load_from_dict(self.data.dataDict)
        self.res_lShopDataByType = Game.res_mgr.res_lShopDataByType
        Game.sub(msg_define.MSG_WEE_HOURS, self.event_wee_hours)
        self.init_serverLimitShopItem()

    # 每日凌晨重置
    def event_wee_hours(self):
        self.init_serverLimitShopItem()


    def _frame_stop(self):
        self.data.save(Game.store, forced=True, no_let=True)

    # 存库数据
    def to_save_dict(self, forced=False):
        if self.isDirty() or forced or not self.save_cache:
            self.save_cache = {}
            self.save_cache["opentime"] = self.opentime
            self.save_cache["mergetime"] = self.mergetime
            self.save_cache["cycleDay"] = self.cycleDay.to_save_bytes()
            self.save_cache["cycleWeek"] = self.cycleWeek.to_save_bytes()
        return self.save_cache

    # 读库数据初始化
    def load_from_dict(self, data):
        self.opentime = data.get("opentime", 0)
        self.mergetime = data.get("mergetime", 0)
        self.cycleDay.load_from_dict(data.get("cycleDay", ""))
        self.cycleWeek.load_from_dict(data.get("cycleWeek", ""))
        if not self.opentime:
            self.opentime = int(time.time())
            self.markDirty()

    # 初始化全服限制道具
    def init_serverLimitShopItem(self):
        if not self.res_lShopDataByType:
            return
        # 天数量限制
        lDayLimitShopList = self.res_lShopDataByType.get(BUY_TYPE.SERVER_DAY_LIMIT, [])
        for shopObj in lDayLimitShopList:
            iNo = shopObj.No()
            canBuyCount = shopObj.canBuyCount()
            if not self.cycDayGet("shop_%s"%iNo):
                self.cycDaySet("shop_%s"%iNo, canBuyCount)
        # 周数量限制
        lWeekLimitShopList = self.res_lShopDataByType.get(BUY_TYPE.SERVER_WEEK_LIMIT, [])
        for shopObj in lWeekLimitShopList:
            iNo = shopObj.No()
            canBuyCount = shopObj.canBuyCount()
            if not self.cycWeekGet("shop_%s"%iNo):
                self.cycWeekSet("shop_%s"%iNo, canBuyCount)
        pass

    def cycDaySet(self, key, value):
        self.cycleDay.Set(key, value)

    def cycDayGet(self, key, default=0):
        return self.cycleDay.Query(key, default)

    def cycWeekSet(self, key, value):
        self.cycleWeek.Set(key, value)

    def cycWeekGet(self, key, default=0):
        return self.cycleWeek.Query(key, default)

    def GetPlayerLoginInitData(self):
        """获取玩家登陆时需要的数据"""
        resp = {}
        resp["opentime"] = self.opentime
        resp["mergetime"] = self.mergetime
        return resp

    def GetServerInfo(self):
        resp = {}
        resp["opentime"] = self.opentime
        resp["mergetime"] = self.mergetime
        return resp

    def SetServerOpenTime(self, iTime):
        self.opentime = iTime
        self.markDirty()

    def SetServerMergeTime(self, iTime):
        self.mergetime = iTime
        self.markDirty()

    def reloadConfig(self, tname):
        Game.res_mgr.loadByNames(tname)

    def printCommonMemory(self):
        import sys
        import gc
        a = {}
        b = {}
        iTotal = 0
        for obj in gc.get_objects():
            if type(obj) in a:
                a[type(obj)] += sys.getsizeof(obj)
                b[type(obj)] += 1
            else:
                a[type(obj)] = sys.getsizeof(obj)
                b[type(obj)] = 1
        rs_a = sorted(a.items(), key=lambda x: x[1], reverse=True)
        rs_b = sorted(b.items(), key=lambda x: x[1], reverse=True)
        for one in rs_a:
            Game.glog.log2File("memLogA", "%s|%s\n" % one)
        for one in rs_b:
            Game.glog.log2File("memLogB", "%s|%s\n" % one)

    def GetOpenTime(self):
        return self.opentime

    def GetOpenDay(self):
        """获取开服天数"""
        day = get_days(self.opentime) + 1
        return day

