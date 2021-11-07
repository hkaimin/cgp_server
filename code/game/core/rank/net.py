#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'
# from game.common.ctn import CPstContainerBase
from game.common.utility import *
import game.mgr.player
import time
from game import Game




class netCmd(object):
    # 协议处理模块
    def __init__(self):
        pass

# ============= 排行榜相关 ==============
    def openRnakUI(self, who):
        if game.gm.gmFunc.G_is0210Ver:
            return self.rc_getTotalGuankaRank(who)
        else:
            return self.rc_getTotalPvpRank(who)

    # 总战绩排行榜
    def rc_getTotalPvpRank(self, who):
        rid = who.getUID()
        dRankInfo = Game.rpc_rank_info.getPvpRank(rid)
        lRank = dRankInfo.get("lrank", [])
        myRankInfo = dRankInfo.get("myRankInfo", [])
        myRank = dRankInfo.get("myRank", 0)
        name = who.data.getName()
        lv  = who.base.lv
        tInfo = [rid, name, "", 0, 0.0, ""]
        myRankDesc = "未上榜"
        if myRankInfo:
            tInfo = myRankInfo
            myRankDesc = "  %s"%myRank
        dInfo = {
            "iType": 2,
            "lRank": lRank,
            "myRank": tInfo,
            "myRankDesc": myRankDesc
        }
        return dInfo

    def rc_getPvpRankThree(self, who):
        dRankInfo = Game.rpc_rank_info.getPvpRankThree()
        return dRankInfo

    # 总等级排行榜
    def rc_getTotalLvRank(self, who):
        rid = who.getUID()
        dRankInfo = Game.rpc_rank_info.getLvRank(rid)
        lRank = dRankInfo.get("lrank", [])
        myRankInfo = dRankInfo.get("myRankInfo", [])
        myRank = dRankInfo.get("myRank", 0)
        name = who.data.getName()
        lv  = who.base.lv
        tInfo = [rid, name, "", lv, ""]
        myRankDesc = "未上榜"
        if myRankInfo:
            tInfo = myRankInfo
            myRankDesc = "  %s"%myRank
        dInfo = {
            "iType": 2,
            "lRank": lRank,
            "myRank": tInfo,
            "myRankDesc": myRankDesc
        }
        return dInfo

    # 关卡排行榜
    def rc_getTotalGuankaRank(self, who):
        rid = who.getUID()
        dRankInfo = Game.rpc_rank_info.getGuankaRank(rid)
        lRank = dRankInfo.get("lrank", [])
        myRankInfo = dRankInfo.get("myRankInfo", [])
        myRank = dRankInfo.get("myRank", 0)
        name = who.data.getName()
        # lv  = who.base.lv
        unLockGuanka = self.Query("unLockGuanka", 1)
        mylastGuanka = unLockGuanka - 1
        tInfo = [rid, name, "", mylastGuanka, ""]
        myRankDesc = "未上榜"
        if myRankInfo:
            tInfo = myRankInfo
            myRankDesc = "  %s"%myRank
        dInfo = {
            "iType": 2,
            "lRank": lRank,
            "myRank": tInfo,
            "myRankDesc": myRankDesc
        }
        return dInfo

    # 好友战绩排行榜
    def rc_getFriendPvpRank(self, who):
        lRank = Game.rpc_rank_info.getFriendPvpRank()
        dInfo = {
            "iType": 3,
            "lRank": lRank,
            "myRank": [],
            "myRankDesc": "未上榜"
        }
        return dInfo

    # 好友等级排行榜
    def rc_getFriendLvRank(self, who):
        lRank = Game.rpc_rank_info.getFriendLvRank()
        dInfo = {
            "iType": 4,
            "lRank": lRank,
            "myRank": [],
            "myRankDesc": "未上榜"
        }
        return dInfo

    # 更新最快通关时间
    def updatebarrPasTime(self, iNo, iPasTime, sName):
        res = Game.rpc_rank_info.updatebarrPasTime(iNo, iPasTime, sName)
        return res

    # 获取对应关卡最快通关时间的人
    def getbarrPasTimeInfoByNo(self, iNo):
        dInfo = Game.rpc_rank_info.getbarrPasTimeInfoByNo(iNo)
        return dInfo

    def updateBarrInfo(self, iNo):
        res = Game.rpc_rank_info.updateBarrInfo(iNo)
        return res

    def cleanGuankaRank(self):
        Game.rpc_rank_info.cleanGuankaRank()


import game.core.item
import game.gm.gmFunc