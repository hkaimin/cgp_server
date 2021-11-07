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
import weakref


WIN_TYPE_TARGET = 2

class TaskFuncType():
    ADD_COIN = 1
    ADD_EXP_PRE = 2
    ADD_FIGHT_SPEED = 3
    ADD_FIGHT_PAO_NUM = 4
    ADD_FIGHT_POWER = 5


# 抢地图小游戏
class MiniGame(object):

    def __init__(self):
        self.Inst = None
        self.players = {}
        self.playerInfo = {}
        self.playerClick = {}
        self.minigameData = Game.res_mgr.res_minigameData
        self.minGameHit2Obj = Game.res_mgr.minGameHit2Obj  # 点击次数对应对象
        self.minGameWin2Obj = Game.res_mgr.minGameWin2Obj  # 赢的目标对应对象
        self.minigame_task_timmer = None

    def setInst(self, inst):
        self.Inst = weakref.proxy(inst)
        self.players = self.Inst.players
        inst.showMiniReadyGo()
        if self.minigame_task_timmer:
            self.minigame_task_timmer.kill(block=False)
            self.minigame_task_timmer = None

        for uid, player in self.players.iteritems():
            self.playerInfo[uid] = {}
            self.playerInfo[uid]["click"] = 0
            self.playerInfo[uid]["hasLvClick"] = 0     # 等级赠送点击
            self.playerInfo[uid]["spClickTimes"] = 0   # 特殊购买次数
            self.playerInfo[uid]["finishTask"] = {}    # 已完成的任务
            self.playerInfo[uid]["isGiveUp"] = 0       # 是否认输
            self.showMiniGameUI(uid)
            self.showTaskInfo(uid)

        self.minigame_task_timmer = spawn_later(7, self.setWin)

    # 显示MINIGAME UI 下行
    def showMiniGameUI(self, uid):
        dminiGameInfo = {}
        dTaskInfo     = {}
        packPlayerInfo = {}
        for uid, playerinfo in self.playerInfo.iteritems():
            playerObj   = self.players.get(uid)
            name        = playerObj.name
            lv          = playerObj.lv
            click       = playerinfo.get("click")
            hasLvClick  = playerinfo.get("hasLvClick")
            spRate      = 5
            # hasLvClick  = playerinfo.get("hasLvClick")
            if not hasLvClick:
                spRate  = lv
            cost        = 100
            packPlayerInfo[uid] = {}                            # 角色ID做KEY
            packPlayerInfo[uid]["name"]          = name         # 名字
            packPlayerInfo[uid]["lv"]            = lv           # 等级
            packPlayerInfo[uid]["click"]         = click        # 点击次数
            packPlayerInfo[uid]["hasLvClick"]    = hasLvClick   # 是否已经用了加成
            packPlayerInfo[uid]["spRate"]        = spRate       # 加成次数
            packPlayerInfo[uid]["cost"]          = cost         # 使用付费加成消耗
        dminiGameInfo["playerInfo"] = packPlayerInfo
        spawn(self.Inst.G2CSendPacket, 'miniGameInfo', dminiGameInfo, uid)  # 展示miniGame UI

    # 显示/刷新 左边点击任务 下行
    def showTaskInfo(self,uid):
        dplayerInfo = self.playerInfo.get(uid)
        finishTask = dplayerInfo.get("dplayerInfo", [])
        dTaskInfo = {}
        taskKey = self.minigameData.keys()
        for key in taskKey:
            taskObj = self.minigameData.get(key)
            ID = taskObj.ID
            finishType = taskObj.finishType # 完成类型
            hitcount = taskObj.hitcount # 达成条件的点击次数
            itype = taskObj.itype # 类型
            desc = taskObj.desc # 描述
            isFinish = 0
            if ID in finishTask:
                isFinish = 1
            dTaskInfo["finishType"] = finishType        # 完成类型
            dTaskInfo["hitcount"] = hitcount            # 点击次数
            dTaskInfo["desc"] = desc                    # 文字表述
            dTaskInfo["isFinish"] = isFinish            # 是否完成
        spawn(self.Inst.G2CSendPacket, 'showTaskInfo', dTaskInfo, uid) # 刷新任务列表


    # 检测任务
    def checkTaskInfo(self, uid, click):
        dplayerInfo = self.playerInfo.get(uid)
        finishTask = dplayerInfo.get("dplayerInfo", [])
        if self.minGameHit2Obj.get(click):
            taskObj = self.minGameHit2Obj.get(click)
            if not finishTask.get(taskObj.ID):
                finishTask[taskObj.ID] = 1
                self.showTaskInfo(uid) # 刷新任务列表


    def setWin(self):
        print "0-----------setWin------"
        bestclick = 0
        bestclickUid = 0
        # bRandomWin = 0
        # if not self.playerClick: # 两边都没点击
        #     bRandomWin = 1
        for uid, playerinfo in self.playerInfo.iteritems():
            dplayerInfo = self.playerInfo.get(uid)
            finishTask = dplayerInfo.get("dplayerInfo", [])
            click = playerinfo.get("click",0)
            isGiveUp = playerinfo.get("isGiveUp",0)
            if click > bestclick and not isGiveUp:
                bestclick = click
                bestclickUid = uid
                winTaskObj = self.minGameWin2Obj.get(WIN_TYPE_TARGET)
                if winTaskObj:
                    ID = winTaskObj.ID
                    finishTask.append(ID)
            self.finishClickTask(uid, finishTask)
        if bestclickUid and bestclickUid in self.players:
            self.Inst.minigameWin(bestclickUid)
        else: # 如果两边都没点
            self.Inst.showReadyGo()
        spawn(self.Inst.broadcast, 'minigameEnd', {})
        self.end()
        try:
            Game.glog.log2File("miniGame", "setWin|%s|%s|%s\n" %(str(self.playerInfo.keys()), bestclickUid, str(self.playerClick)))
        except:
            Game.glog.LogPyException()
            pass

    # 完成任务，给加成
    def finishClickTask(self, uid, lfinishTask):
        playerObj = self.players.get(uid)
        if not playerObj:
            print "-------------!!!"
            return
        for taskID in lfinishTask:
            taskObj = self.minigameData.get(taskID)
            if taskObj:
                if taskObj.itype == TaskFuncType.ADD_COIN:
                    addCoin = taskObj.param
                    playerObj.addCoin(addCoin)
                if taskObj.itype == TaskFuncType.ADD_EXP_PRE:
                    addExpPre = taskObj.param/100.0
                    playerObj.addExpPrecent(addExpPre)
                if taskObj.itype == TaskFuncType.ADD_FIGHT_SPEED:
                    addSpeed = taskObj.param
                    playerObj.addSpeed(addSpeed)
                if taskObj.itype == TaskFuncType.ADD_FIGHT_PAO_NUM:
                    addPaopaoNum = taskObj.param
                    playerObj.addPaopaocount(addPaopaoNum)
                if taskObj.itype == TaskFuncType.ADD_FIGHT_POWER:
                    addPower = taskObj.param
                    playerObj.addPower(addPower)

    # 每次点击，服务的广播
    def broadcastClick(self, uid, click):
        dclickInfo = {
            "uid":uid,
            "click":click
        }
        spawn(self.Inst.broadcast, 'UpdateClick', dclickInfo)  # 刷新点击次数
        self.playerClick[uid] = click


    # 普通点击
    def normalClick(self, uid):
        dplayerInfo = self.playerInfo.get(uid)
        if not dplayerInfo:
            return
        click = dplayerInfo["click"]
        click += 1
        dplayerInfo["click"] = click
        self.broadcastClick(uid, click)

    # 特殊点击
    def spClick(self, uid):
        playerObj = self.players.get(uid)
        if not playerObj:
            return
        lv = playerObj.lv
        spRate = 10
        dplayerInfo = self.playerInfo.get(uid)
        if not dplayerInfo:
            return
        hasLvClick = dplayerInfo.get("hasLvClick")
        if not hasLvClick:
            spRate = lv
            dplayerInfo["hasLvClick"] = 1
        click = dplayerInfo["click"]
        lastClick = click
        click += spRate
        dplayerInfo["click"] = click
        dplayerInfo["spClickTimes"] += 1
        for i in xrange(lastClick, click):
            if i != lastClick:
                spawn(self.checkTaskInfo, uid, i)
        self.playerInfo[uid] = dplayerInfo
        self.broadcastClick(uid, click) # 刷新点击次数

    # 玩家弃权（机器人默认弃权）
    def miniGameGiveup(self, uid):
        dplayerInfo = self.playerInfo.get(uid)
        if dplayerInfo:
            dplayerInfo[uid]["isGiveUp"] = 1
            dGiveInfo = {
                "uid":uid
            }
            spawn(self.Inst.broadcast, 'PlayerGiveUp', dGiveInfo)  # 玩家弃权)
            self.end()
            self.setWin()


    def end(self):
        if self.minigame_task_timmer:
            self.minigame_task_timmer.kill(block=False)
            self.minigame_task_timmer = None



