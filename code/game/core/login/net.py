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

# @observable
class netCmd(object):
    # 协议处理模块
    def __init__(self):
        self.GameConfData = Game.res_mgr.res_gameConfData
        self.sevenDayCycleData = Game.res_mgr.res_sevenDayCycleData
        self.itemData = Game.res_mgr.res_itemData
        self.btnData = Game.res_mgr.res_btnData
        self.upgradeData = Game.res_mgr.res_upgrade
        pass

    # 每日奖励
    def show_OneDayReward(self):
        bShowOneDay = self.cycleDay.Query("bShowOneDay",0)
        bGetOneDay = self.cycleDay.Query("bGetOneDay",0)
        data ={}
        if not bShowOneDay and not bGetOneDay:
            data = self.OneDayReward()
            self.cycleDay.Set("bShowOneDay", 1)
        return data

    # 每天奖励
    def OneDayReward(self):
        DayLoginRewardSmallObj = self.GameConfData.get("DayLoginRewardSmall")
        DayLoginRewardVedioObj = self.GameConfData.get("DayLoginRewardVedio")
        SmallReward = DayLoginRewardSmallObj.GetValue()
        VedioReward = DayLoginRewardVedioObj.GetValue()
        data = {"SmallReward":SmallReward, "VedioReward":VedioReward}
        self.broadcast("OneDayReward", data)

    # 七日奖励
    def show_sevenDayReward(self):
        bSevenDay = self.cycleDay.Query("bSevenDay",0)
        bGetSevenDay = self.cycleDay.Query("bGetSevenDay",0)
        print "-----show_sevenDayReward----1", bSevenDay, bGetSevenDay
        if bSevenDay or bGetSevenDay:
            return
        sevenCycle = self.Query("sevenCycle", 1)
        sevenDayGet = self.Query("sevenDayGet", 0)
        sevenDayGet, sevenCycle = self.reflashSevenDayGet(sevenDayGet, sevenCycle)

        res_sevenDayCycleData = Game.res_mgr.res_sevenDayCycleData
        cycleData = res_sevenDayCycleData.get(sevenCycle, {})
        if not cycleData:
            # 重置
            sevenCycle = 1
            cycleData = res_sevenDayCycleData.get(sevenCycle, {})
            if not cycleData:
                print "-----show_sevenDayReward----2"
                return
            self.Set("sevenDayGet", 1)
        info = {}
        for day, sevenDayObj in cycleData.iteritems():
            showData = sevenDayObj.getShow()
            itemNo = showData.keys()[0]
            itemInfo = self.itemData.get(itemNo)
            sRes = itemInfo.res
            bGet = 0
            info[day] = {}
            info[day]["itemNo"] = itemNo
            info[day]["sRes"] = sRes
            info[day]["Exps"] = sevenDayObj.Exps
            if sevenDayGet >= day:
                bGet = 1
            info[day]["bGet"] = bGet # 是否已领取
        # self.cycleDay.Set("bSevenDay",sevenCycle)
        self.broadcast("SeventDayReward", info)

    # 领奖后刷新7日奖励界面
    def reflashsevenDayReward(self):
        sevenCycle = self.Query("sevenCycle", 1)
        sevenDayGet = self.Query("sevenDayGet", 0)
        res_sevenDayCycleData = Game.res_mgr.res_sevenDayCycleData
        cycleData = res_sevenDayCycleData.get(sevenCycle, {})
        if not cycleData:
            return
        print "reflah_sevenDayGet:",sevenDayGet
        info = {}
        for day, sevenDayObj in cycleData.iteritems():
            showData = sevenDayObj.getShow()
            itemNo = showData.keys()[0]
            itemInfo = self.itemData.get(itemNo)
            sRes = itemInfo.res
            bGet = 0
            info[day] = {}
            info[day]["itemNo"] = itemNo
            info[day]["sRes"] = sRes
            info[day]["Exps"] = sevenDayObj.Exps
            if sevenDayGet >= day:
                bGet = 1
            info[day]["bGet"] = bGet # 是否已领取
        # self.cycleDay.Set("bSevenDay",sevenCycle)
        self.broadcast("SeventDayReward", info)

    # 领取每天奖励
    def rc_getOneDayReward(self, type=0):
        if self.cycleDay.Query("bGetOneDay"):
            return {}
        DayLoginRewardSmallObj = self.GameConfData.get("DayLoginRewardSmall")
        DayLoginRewardVedioObj = self.GameConfData.get("DayLoginRewardVedio")
        print DayLoginRewardSmallObj, DayLoginRewardVedioObj
        SmallReward = DayLoginRewardSmallObj.GetValue()
        VedioReward = DayLoginRewardVedioObj.GetValue()
        print SmallReward, VedioReward
        if type == 1:
            SmallReward.update(VedioReward)
        for iNo, num in SmallReward.iteritems():
            self.AddItem(self,iNo, num)
        self.cycleDay.Set("bGetOneDay", 1)
        return SmallReward

    # 领取七天奖励
    def rc_getSeventDayReward(self):
        sevenCycle = self.Query("sevenCycle", 1)
        sevenDayGet = self.Query("sevenDayGet", 0)
        if self.cycleDay.Query("bGetOneDay"):
            return {}
        if self.cycleDay.Query("bGetSevenDay"):
            return
        res_sevenDayCycleData = Game.res_mgr.res_sevenDayCycleData
        cycleData = res_sevenDayCycleData.get(sevenCycle, {})
        if not cycleData:
            return {}
        sevenDayObj = cycleData.get(sevenDayGet+1)
        reward = sevenDayObj.getReward()
        for iNo, num in reward.iteritems():
            self.AddItem(self, iNo, num)
        sevenDayGet = sevenDayGet + 1
        print "sevenDayGet:",sevenDayGet
        self.Set("sevenDayGet", sevenDayGet)
        self.Set("sevenCycle", sevenCycle)
        self.cycleDay.Set("bGetSevenDay", 1)
        self.reflashsevenDayReward()
        self.reflashSevenDayGet(sevenDayGet, sevenCycle)
        return reward

    def reflashSevenDayGet(self, sevenDayGet, sevenCycle):
        if sevenDayGet >= 7:
            sevenDayGet = 0
            sevenCycle = sevenCycle + 1
            if sevenCycle > 2:
                sevenCycle = 1
        print "sevenDayGet:",sevenDayGet
        self.Set("sevenDayGet", sevenDayGet)
        self.Set("sevenCycle", sevenCycle)
        return sevenDayGet, sevenCycle

    # 登陆推送按钮数据    、
    def pushBtnData(self):
        dBtnData = {}
        for id, dData in self.btnData.iteritems():
            if not dBtnData.has_key(id):
                dBtnData[id] = {}
            name = dData.name  # 名字
            pos = dData.pos  # 位置（1为右边，2为下面）
            isOpen = dData.isOpen  # 是否开启
            weight = dData.weight  #
            dBtnData[id]["id"] = id
            dBtnData[id]["name"] = name
            dBtnData[id]["pos"] = pos
            dBtnData[id]["isOpen"] = isOpen
            dBtnData[id]["weight"] = weight
        self.broadcast("pushBtnData", dBtnData)

    # 升级奖励
    def showUpgradeReward(self):
        LVKeys = self.upgradeData.keys()
        LVKeys.sort()
        # maxExp = self.getExp()
        curExp = self.getCurExp()
        curLv =  self.Lv()
        LvInfo = {}
        iTotalExp = 0
        lUpgradeReward = self.Query("lUpgradeReward", [])
        bHasReward = 0
        for iLv in LVKeys:
            LvObj = self.upgradeData.get(iLv)
            rewardNo = LvObj.getRewardItemNo()
            if not rewardNo:
                continue
            rewardNun = LvObj.getRewardNum()
            itemObj = self.itemData.get(rewardNo)
            iLvNeedExp = LvObj.exp
            iTotalExp += iLvNeedExp
            iStatus = 0 # 0:不可领取， 1：可领取， 2：已领取
            if curLv >= iLv:
                iStatus = 1
                pass
            if iLv in lUpgradeReward:
                iStatus = 2
            # print iLv, rewardNo, rewardNun, itemObj
            if iStatus == 1 and not bHasReward:
                bHasReward = 1
            info = {
                "iLv":iLv, # 等级
                "id":itemObj.id,
                "icon":itemObj.res, # 图片
                "name":itemObj.name, # 名字
                "itype":itemObj.itype, # 类型
                "rewardNun":rewardNun, # 数量
                "iLvNeedExp":iLvNeedExp, #每级升级所需
                "iStatus": iStatus,  # 0:不可领取， 1：可领取， 2：已领取
            }
            LvInfo[iLv] = info
        dUpgradeReward = {
            "iTotalExp":iTotalExp, #
            "curExp": curExp,
            "LvInfo": LvInfo,
            "bHasReward":bHasReward,
        }
        self.broadcast("showUpgradeReward", dUpgradeReward)
        return {}

    # 获得升级奖励
    def getUpgradeReward(self, iLv):
        curExp = self.getCurExp()
        LVKeys = self.upgradeData.keys()
        curLv = self.Lv()
        MaxLv = max(LVKeys)
        lUpgradeReward = self.Query("lUpgradeReward", [])
        if iLv in lUpgradeReward:
            self.notify("等级%s奖励，已领取！"%iLv)
            return {}
        if iLv > curLv:
            self.notify("未达到等级%s"%iLv)
            return {}
        if iLv > MaxLv:
            self.notify("不能超过最大等级")
            return {}
        LvObj = self.upgradeData.get(iLv)
        rewardNo = LvObj.getRewardItemNo()
        rewardNun = LvObj.getRewardNum()
        itemObj = self.itemData.get(rewardNo)
        Obj = self.AddItem(self, rewardNo, rewardNun)
        if itemObj.itype == 4: # 解锁人物
            Obj.useItem(self)
        if itemObj.itype == 5: # 解锁功能
            Obj.useItem(self)
        lUpgradeReward.append(iLv)
        self.Set("lUpgradeReward", lUpgradeReward)
        self.notify("领取成功")
        self.showUpgradeReward()
        return {}

    # 观看视频后领取等级奖励
    def getUpgradeRewardAuto(self):
        LVKeys = self.upgradeData.keys()
        LVKeys.sort()
        curExp = self.getCurExp()
        curLv =  self.Lv()
        LvInfo = {}
        iTotalExp = 0
        lUpgradeReward = self.Query("lUpgradeReward", [])
        iRewardLv = 0
        for iLv in LVKeys:
            LvObj = self.upgradeData.get(iLv)
            rewardNo = LvObj.getRewardItemNo()
            if not rewardNo:
                continue
            iLvNeedExp = LvObj.exp
            iTotalExp += iLvNeedExp
            iStatus = 0 # 0:不可领取， 1：可领取， 2：已领取
            if curLv >= iLv:
                iStatus = 1
            if iLv in lUpgradeReward:
                iStatus = 2
            if iStatus == 1:
                iRewardLv = iLv
                break
        if not iRewardLv:
            return
        self.getUpgradeReward(iRewardLv)
        try:
            Game.glog.log2File("getUpgradeReward",
                               "%s|%s|%s|%s" % (
                                   self.id, self.Name(), self.data.account, iRewardLv))
        except:
            pass
        return {}

    def getGonggao(self):
        tips = '''新春豪礼活动：2月11日~2月26日，点击【红包】按钮，会获得【珍稀角色】、【泡泡皮肤】或者大量【钻石】，快快来领取吧！！
-----------------------------------------------
参与【DIY地图】制作，优秀的作品有机被会收录到匹配对战地图中哦！
本期收录名单：良的地图1069, 🍀 lixinrui🍀的地图，良的地图0，鹏宝的地图
本周优秀设计师：良，🍀 lixinrui🍀，幸福家人，萧峰，濯爷爷，鹏宝
闯关达人：刘小缘 127关 
!-----------------------------------------------!
关注微信公众号【天曜工作室】，可以关注游戏最新动态。如果在游戏中遇到任何问题，也可以在公众号留言哦，我们会尽快处理哒。
                                                                      ----天曜工作室
'''
        # 【新春豪礼活动】：点击【红包】按钮，有机会获得各种资源，还有机会获得珍稀角色和泡泡皮肤哦，快快来领取吧！！
        # ----天曜工作室
        data = {}
        data["name"] = "活动公告"
        data["content"] = tips
        return data



import game.core.shop