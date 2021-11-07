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
from game.define.errcode import *


# @observable
class netCmd(object):
    # 协议处理模块
    def __init__(self):
        self.GameConfData = Game.res_mgr.res_gameConfData
        self.res_wujinInstLevelData = Game.res_mgr.res_wujinInstLevelData
        self.res_wujinInstData = Game.res_mgr.res_wujinInstData
        self.dTrainData = Game.res_mgr.dTrainData
        pass

    def getWujinData(self):
        wujinData = self.Query("wujinData", {})
        if not wujinData:
            wujinData = {
                "nowdiffLevel": 1,
                "passBarr": {}
            }
            self.Set("wujinData", wujinData)
        return wujinData

    def getwujinDiffLevel(self):
        wujinDiffLevel = self.Query("wujinDiffLevel", 1)
        return wujinDiffLevel

    # 获取关卡列表
    # nowdiffLevel 第几层
    def rc_C2GOpenWujinUI(self, diffLevel):
        print "-------diffLevel:", diffLevel
        wujinData = self.getWujinData()
        nowdiffLevel = wujinData.get("nowdiffLevel", 1)
        passBarr = wujinData.get("passBarr", {})
        GuanKaInfo = self.Query("GuanKaInfo", {})
        # if diffLevel > nowdiffLevel:
        #     diffLevel = nowdiffLevel
        barrierList = self.res_wujinInstLevelData.get(diffLevel, [])
        if not barrierList:
            return
        tili = self.getTiliCnt()
        dData = {}
        nowstar = 0
        totallayer = len(self.res_wujinInstLevelData.keys())
        for barrObj in barrierList:
            # barrierData = self.res_wujinInstData.get(barrierNo)
            isPass = 0
            barrierNo = barrObj.id
            if barrierNo in passBarr:
                isPass = 1
            star = GuanKaInfo.get(str(barrierNo), 0)
            if star > 3:
                star = 3
            if not dData.has_key("barrierList"):
                dData["barrierList"] = []
            unLockGuanka = self.Query("unLockGuanka", 1)
            isUnLock = 1
            if barrierNo <= unLockGuanka:
                isUnLock = 0
            dInfo = {
                "barrierNo": barrierNo,
                "isPass": isPass,
                "star": star,
                "isSp": 0,  # 是否特殊关卡
                "isLock":isUnLock # 是否上锁
            }
            dData["barrierList"].append(dInfo)
            nowstar += star
            if totallayer < barrObj.diffLevel:
                totallayer = barrObj.diffLevel
        dData["totalstar"] = len(barrierList) * 3  # 总星星数
        dData["nowstar"] = nowstar  # 现在的星星数
        dData["bgetReward"] = 0  # 是否领了奖励
        dData["rewardId"] = 0  # 奖励ID
        dData["status"] = 0 # 0:未解锁， 1：已解锁
        dData["totallayer"] = totallayer  # 总层数
        dData["tili"] = tili # 当前体力
        return dData

    def setPassGuanka(self, iPassNo):
        myPassGuanka = self.Query("myPassGuanka", [])
        maxPassGuanka = max(myPassGuanka)
        if iPassNo >= maxPassGuanka and iPassNo not in myPassGuanka:
            myPassGuanka.append(myPassGuanka)

    def setunLock(self, iPassNo):
        unLockGuanka = self.Query("unLockGuanka", 1)
        if int(iPassNo) >= unLockGuanka:
            unLockGuanka += 1
        self.Set("unLockGuanka", unLockGuanka)

    # 进入关卡
    def rc_C2GGotoBarrier(self, barrierNo, isGm=False):
        unLockGuanka = self.Query("unLockGuanka", 1)
        if barrierNo > unLockGuanka and not isGm:
            self.notify("该关卡未解锁")
            return
        barrierData = self.res_wujinInstData.get(barrierNo)
        print "=================>>>>>> rc_C2GGotoBarrier", barrierNo
        layerconf = barrierData.layerconf
        bgconf = barrierData.bgconf
        info = {
            "layerconf": layerconf,
            "bgconf": bgconf,
            "barrierNo": barrierNo,
        }
        setattr(self, "mapInfo", info)
        setattr(self, "isTrain", 0)
        import game.core.NewWaitRoom
        game.core.NewWaitRoom.gCNewWaitRoomMng.EnterPVEGuanKa(self.id)
        self.doUseTili(5)
        return {"err": "ok"}

    def rc_openBarrierDetail(self, barrierNo):

        pass

    # 进入训练关卡
    def rc_C2GEnterTrain(self):
        barrierKeys= self.dTrainData.keys()
        key = barrierKeys[0]
        #print "----------------rc_C2GEnterTrain", key
        barrierData = self.dTrainData.get(key)
        if not barrierData:
            print "--------not train data"
            return
        layerconf = barrierData.layerconf
        bgconf = barrierData.bgconf
        info = {
            "layerconf": layerconf,
            "bgconf": bgconf,
            "barrierNo": key,
        }
        setattr(self, "mapInfo", info)
        setattr(self, "isTrain", 1)
        import game.core.NewWaitRoom
        game.core.NewWaitRoom.gCNewWaitRoomMng.EnterPVEGuanKa(self.id)
        return {"err": "ok"}

    # 更新关卡信息
    def updateStar(self, iNo, iStar, usetime):
        GuanKaInfo = self.Query("GuanKaInfo", {})
        key_iNo = str(iNo)
        if GuanKaInfo.get(key_iNo, 0) < iStar:
            GuanKaInfo[key_iNo] = iStar
        self.Set("GuanKaInfo", GuanKaInfo)
        GuanKaTimeInfo = self.Query("GuanKaTimeInfo", {}) # 关卡最短用时
        key_iNo = str(iNo)
        if GuanKaTimeInfo.get(key_iNo, 0) > usetime:
            GuanKaTimeInfo[key_iNo] = round(usetime, 3)
        if GuanKaTimeInfo.get(key_iNo, 0) == 0:
            GuanKaTimeInfo[key_iNo] = round(usetime, 3)
        self.Set("GuanKaTimeInfo", GuanKaTimeInfo)
        self.updatebarrPasTime(key_iNo, usetime, self.Name())
        if iStar and usetime:
            self.setunLock(iNo)
            sStr = "恭喜%s在第%s关闯关成功！"%(self.Name(), key_iNo)
            self.rf_scrollNotice(sStr)
            self.updateGuankaRank(iNo)
        try:
            Game.glog.log2File("GuankaFinish",
                               "%s|%s|%s|%s|%s|%s" % (self.id, self.Name(), self.data.account, key_iNo, usetime, iStar))
        except:

            pass


    # 输了攻打次数
    def updateBarrInfo(self, iNo):
        key_iNo = str(iNo)
        self.updateBarrInfo(key_iNo)

    # 再来一次
    def rc_againGuanka(self):
        mapInfo = getattr(self, "mapInfo", {})
        barrierNo = mapInfo.get("barrierNo", 1)
        self.rc_C2GGotoBarrier(barrierNo)
        pass

    # 下一关
    def rc_nextGuanka(self):
        mapInfo = getattr(self, "mapInfo", {})
        barrierNo = mapInfo.get("barrierNo", 1)
        allGuanKa = self.res_wujinInstData.keys()
        maxGuanka = max(allGuanKa)
        if maxGuanka <= barrierNo:
            barrierNo = maxGuanka
        self.rc_C2GGotoBarrier(barrierNo)

    # 获取关卡信息
    def getBarrierInfo(self, barrierNo):
        GuanKaTimeInfo = self.Query("GuanKaTimeInfo", {}) # 关卡最短用时
        key_iNo = str(barrierNo)
        myTime = GuanKaTimeInfo.get(key_iNo, 0)
        dInfo = Game.rpc_rank_info.getBarrierInfo(barrierNo)
        GuanKaInfo = self.Query("GuanKaInfo", {})
        iStar = GuanKaInfo.get(key_iNo, 0)
        if iStar > 3:
            iStar = 3
        dInfo["iStar"] = iStar
        dInfo["myTime"] = myTime
        print dInfo
        return dInfo

import game.core.shop
