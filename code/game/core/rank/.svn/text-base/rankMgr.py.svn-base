#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from game.common import utility

from corelib.frame import Game, MSG_FRAME_STOP
from game.models.rank import ModelRank
from corelib.gtime import get_days
from game.common.utility import *

PVP_RANK_MAX = 200


class RankInfo(utility.DirtyFlag):
    """服务器信息"""
    _rpc_name_ = 'rpc_rank_info'

    def __init__(self):
        utility.DirtyFlag.__init__(self)
        self.data = None
        self.lPvpRank = [] # PVP总排行榜
        self.lLvRank = [] # PVP等级排行榜
        self.lGuankaRank = [] # 闯关排行榜

        self.lFriendPvpRank = [] # PVP总排行榜
        self.lFriendLVRank = [] # PVP等级排行榜

        self.pasBarrRecord = {} # 记录最快通关时间
        self.barrInfo = {} # 用来记录关卡胜率等信息


        self.save_cache = {}  # 存储缓存



        Game.sub(MSG_FRAME_STOP, self._frame_stop)

    def getPvpRank(self, rid):
        # print "--lPvpRank:",self.lPvpRank
        # return self.lPvpRank[:20]
        dData = {
            "lrank":self.lPvpRank[:50],
            "myRankInfo":self.getMypvpRankInfo(rid),
            "myRank":self.getMypvpRank(rid)
        }
        return dData

    def getPvpRankThree(self):
        dData = {
            "lrank":self.lPvpRank[:3],
        }
        return dData

    def getLvRank(self, rid):
        # print "--lLvRank:", self.lLvRank
        dData = {
            "lrank":self.lLvRank[:50],
            "myRankInfo":self.getMylvRankInfo(rid),
            "myRank":self.getMylvRank(rid)
        }
        return dData

    def getGuankaRank(self, rid):
        # print "--lLvRank:", self.lLvRank
        dData = {
            "lrank":self.lGuankaRank[:50],
            "myRankInfo":self.getMyGuankaRankInfo(rid),
            "myRank":self.getMyGuankaRank(rid)
        }
        return dData

    def getFriendPvpRank(self):
        return self.lFriendPvpRank[:30]

    def getFriendLvRank(self):
        return self.lFriendLVRank[:30]

    def start(self):
        print ">>>>>>>>>>>>>> Rank stat <<<<<<<<<<<<<<<<"
        self.data = ModelRank.load(Game.store, ModelRank.TABLE_KEY)
        # print self.data , self.data.dataDict
        print ">>>>>>>>>>>>>> Rank stat <<<<<<<<<<<<<<<< 2"
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
            self.save_cache["lPvpRank"] = self.lPvpRank
            self.save_cache["lLvRank"] = self.lLvRank
            self.save_cache["lGuankaRank"] = self.lGuankaRank
            self.save_cache["pasBarrRecord"] = self.pasBarrRecord
            self.save_cache["barrInfo"] = self.barrInfo
        return self.save_cache

    # 读库数据初始化
    def load_from_dict(self, data):
        # print "-44444444444444444-------load rank data", data
        self.lPvpRank = data.get("lPvpRank", [])
        self.lLvRank = data.get("lLvRank", [])
        self.lGuankaRank = data.get("lGuankaRank", [])
        self.pasBarrRecord = data.get("pasBarrRecord", {})
        # print "self.lPvpRank:",self.lPvpRank
        # print "self.lLvRank:",self.lLvRank
        self.markDirty()

    def SaveRank(self):
        self.data.save(Game.store, forced=True)

    # ================ pvp排行榜 ================
    def updatePvpRank(self, rid, sName, sPic, winCount, winRate, wechatId=""):
        # winCount 胜场
        # winRate 胜率
        # wechatId 微信ID
        tInfo = [rid, sName, sPic, winCount, winRate, wechatId]
        self.insterPvpRank(rid, tInfo)
        pass

    def forceUpdatePveRank(self, rid, sName, sPic, winCount, winRate, wechatId=""):
        tInfo = [rid, sName, sPic, winCount, winRate, wechatId]
        self.insterPvpRank(rid, tInfo, forceUpdate=True)

    def insterPvpRank(self, rid, tUpdateInfo, forceUpdate=False):
        # tInfo = [rid, sName, sPic, winCount, winRate, wechatId]
        #print ">>>>>>>>> insterPvpRank", tUpdateInfo
        for i, tInfo in enumerate(self.lPvpRank):
            if tInfo[0] == rid:
                if forceUpdate:
                    self.lPvpRank.pop(i)
                    break
                if tUpdateInfo[3] > tInfo[3]:
                    self.lPvpRank.pop(i)
                    break
                elif tUpdateInfo[4] != tInfo[4]:
                    self.lPvpRank.pop(i)
                    break
                return
        BinaryInsertRight(self.lPvpRank, tUpdateInfo, self.MyPvpSort)
        while len(self.lPvpRank) > PVP_RANK_MAX:
            self.lPvpRank.pop()
        print self.lPvpRank
        self.markDirty()
        pass

    def MyPvpSort(self, a, b):
        l1 = [a[3],a[4],-1*a[1]]
        l2 = [b[3],b[4],-1*b[1]]
        if l1 > l2:
            return -1
        else:
            return 1

    # 获取我的排名
    def getMypvpRank(self, rid):
        i = 0
        for t in self.lPvpRank:
            if t[0] == rid:
                return i + 1
            i = i + 1
        return i

    # 获取我的排名详细
    def getMypvpRankInfo(self, rid):
        for t in self.lPvpRank:
            if t[0] == rid:
                return t
        return None

    # ================ 等级排行榜 ================
    def updateLvRank(self, rid, sName, sPic, lv, wechatId=""):
        tInfo = [rid, sName, sPic, lv, wechatId]
        self.insterLvRank(rid, tInfo)
        pass

    def forceUpdateLvRank(self, rid, sName, sPic, lv, wechatId=""):
        tInfo = [rid, sName, sPic, lv, wechatId]
        self.insterLvRank(rid, tInfo, forceUpdate=True)

    def insterLvRank(self, rid, tUpdateInfo, forceUpdate=False):
        for i, tInfo in enumerate(self.lLvRank):
            if tInfo[0] == rid:
                if forceUpdate:
                    self.lLvRank.pop(i)
                    break
                if tUpdateInfo[3] > tInfo[3]:
                    self.lLvRank.pop(i)
                    break
                return
        BinaryInsertRight(self.lLvRank, tUpdateInfo, self.MyLvSort)
        while len(self.lLvRank) > PVP_RANK_MAX:
            self.lLvRank.pop()
        print self.lLvRank
        self.markDirty()
        pass

    def MyLvSort(self, a, b):
        l1 = [a[3],-1*a[1]]
        l2 = [b[3],-1*b[1]]
        if l1 > l2:
            return -1
        else:
            return 1

    # 获取我的排名
    def getMylvRank(self, rid):
        i = 0
        for t in self.lLvRank:
            if t[0] == rid:
                return i + 1
            i = i + 1
        return i

    # 获取我的排名详细
    def getMylvRankInfo(self, rid):
        for t in self.lLvRank:
            if t[0] == rid:
                return t
        return None

    # 更新最快通关时间
    def updatebarrPasTime(self, iNo, iPasTime, sName):
        print 111111111111111111111111111, iNo, iPasTime
        iPasTime = round(iPasTime, 5)
        lastPasTimeInfo = self.pasBarrRecord.get(str(iNo), {})
        serverBsetTime = lastPasTimeInfo.get("serverBsetTime", 0)
        name = lastPasTimeInfo.get("serverBestname", "")

        if serverBsetTime <= 0 and iPasTime >0:
            lastPasTimeInfo["serverBsetTime"] = iPasTime
            lastPasTimeInfo["serverBestname"] = sName
            self.pasBarrRecord[str(iNo)] = lastPasTimeInfo
        elif serverBsetTime > 0 and iPasTime >0 and iPasTime < serverBsetTime:
            lastPasTimeInfo["serverBsetTime"] = iPasTime
            lastPasTimeInfo["serverBestname"] = sName
            self.pasBarrRecord[str(iNo)] = lastPasTimeInfo
        print 111111111112222,  self.pasBarrRecord
        self.markDirty()
        self.updateBarrInfo(iNo, True)
        return 1

    # 获取对应关卡最快通关时间的人
    def getbarrPasTimeInfoByNo(self, iNo):
        print 1111111111111122221111111111111
        lastPasTimeInfo = self.pasBarrRecord.get(str(iNo), {})
        print 111111111, lastPasTimeInfo
        return lastPasTimeInfo

    # 更新关卡信息
    def updateBarrInfo(self, iNo, isWin=False):
        iNo = str(iNo)
        barrInfo = self.barrInfo.get(iNo, {})
        if not barrInfo:
            barrInfo = {
                "winTimes":1,
                "totalTimes":1,
            }
        if isWin:
            winTimes = barrInfo.get("winTimes", 0)
            winTimes = winTimes + 1
            barrInfo["winTimes"] = winTimes
        totalTimes = barrInfo.get("totalTimes", 0)
        totalTimes = totalTimes + 1
        barrInfo["totalTimes"] = totalTimes
        self.barrInfo[iNo] = barrInfo
        self.markDirty()
        return 1

    # 获取关卡
    def getBarrierInfo(self, iNo):
        iNo = str(iNo)
        dInfo = {}
        barrInfo = self.barrInfo.get(iNo, {})
        if not barrInfo:
            barrInfo = {
                "winTimes":1,
                "totalTimes":1,
            }
        lastPasTimeInfo = self.pasBarrRecord.get(str(iNo), {})
        serverBsetTime = lastPasTimeInfo.get("serverBsetTime", 0)
        name = lastPasTimeInfo.get("serverBestname", "")
        dInfo["barrInfo"] = barrInfo
        winRate = (barrInfo.get("winTimes")/(barrInfo.get("totalTimes")*1.0))*100
        dInfo["winRate"] = round(winRate, 2)
        dInfo["serverBsetTime"] = serverBsetTime # 全服最快通关时间
        dInfo["serverBestname"] = name # 名字
        dInfo["iBarrierNo"] = iNo

        return dInfo

    # ================ 闯关排行榜 ================
    def updateGuankaRank(self, rid, sName, sPic, GuanKaID, wechatId=""):
        # winCount 胜场
        # winRate 胜率
        # wechatId 微信ID
        GuanKaID = int(GuanKaID)
        tInfo = [rid, sName, sPic, GuanKaID, wechatId]
        self.insterGuankaRank(rid, tInfo)
        pass

    def forceUpdateGuankaRank(self, rid, sName, sPic, GuanKaID, wechatId=""):
        GuanKaID = int(GuanKaID)
        tInfo = [rid, sName, sPic, GuanKaID, wechatId]
        self.insterGuankaRank(rid, tInfo, forceUpdate=True)

    def insterGuankaRank(self, rid, tUpdateInfo, forceUpdate=False):
        # tInfo = [rid, sName, sPic, winCount, winRate, wechatId]
        #print ">>>>>>>>> insterPvpRank", tUpdateInfo
        for i, tInfo in enumerate(self.lGuankaRank):
            if tInfo[0] == rid:
                if forceUpdate:
                    self.lGuankaRank.pop(i)
                    break
                if tUpdateInfo[3] > tInfo[3]:
                    self.lGuankaRank.pop(i)
                    break
                elif tUpdateInfo[4] != tInfo[4]:
                    self.lGuankaRank.pop(i)
                    break
                return
        BinaryInsertRight(self.lGuankaRank, tUpdateInfo, self.MyGuankaSort)
        while len(self.lGuankaRank) > PVP_RANK_MAX:
            self.lGuankaRank.pop()
        print self.lGuankaRank
        self.markDirty()
        pass

    def MyGuankaSort(self, a, b):
        l1 = [a[3],-1*a[1]]
        l2 = [b[3],-1*b[1]]
        if l1 > l2:
            return -1
        else:
            return 1

    # 获取我的排名
    def getMyGuankaRank(self, rid):
        i = 0
        for t in self.lGuankaRank:
            if t[0] == rid:
                return i + 1
            i = i + 1
        return i

    # 获取我的排名详细
    def getMyGuankaRankInfo(self, rid):
        for t in self.lGuankaRank:
            if t[0] == rid:
                return t
        return None

    def cleanGuankaRank(self):
        self.lGuankaRank = []
