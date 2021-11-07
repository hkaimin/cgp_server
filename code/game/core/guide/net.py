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
from game.define.shop_define import *
from game.define.constant import *

class CGuildType(object):
    FIRST_IN_MAIN = 1
    CLICK_TRAIN = 2
    FIGHT_TRAINING = 3
    CLICK_GUANKA = 4
    CLICK_DIYMAP = 6

# 角色系統

# @observable
class netCmd(object):
    # 协议处理模块
    def __init__(self):
        self.GuildData = Game.res_mgr.res_guildData
        self.dGuildForKey = Game.res_mgr.dGuideForKey


    def getGuild(self):
        GuildID = self.Query("GuildID", 1)
        GuildKey = self.Query("GuildKey", 1)
        GuildStep = self.Query("GuildStep", 1)

    # 推送引导
    def sendGuild(self):
        print "1111111111111111111111221 sendGuild"
        GuildID = self.Query("GuildID", 1)
        GuildKey = self.Query("GuildKey", 1)
        GuildStep = self.Query("GuildStep", 1)
        if GuildID > max(self.GuildData.keys()):
            return
        if GuildID  == 0:
            GuildID = 1
            self.Set("GuildID", 1)
        if GuildKey == 0:
            GuildKey = 1
            self.Set("GuildKey", 1)
        if GuildStep == 0:
            GuildStep = 1
            self.Set("GuildStep", 1)
        GuildObj = self.GuildData.get(GuildID)
        if not GuildObj:
            return
        #print "----------------GuildObj.isFight",GuildObj.isFight,self.isFighting(),self.isFightingTrain()
        if GuildObj.isFight:
            if self.isFighting() and self.isFightingTrain():
                self.packGuild(GuildObj)
            else:
                return
        else:
            if not self.isFighting():
                self.packGuild(GuildObj)
        # isFighting
        # isFightingTrain
        pass

    def finishGuild(self):
        GuildID = self.Query("GuildID", 1)
        GuildKey = self.Query("GuildKey", 1)
        GuildStep = self.Query("GuildStep", 1)
        GuildObj = self.GuildData.get(GuildID)
        if not GuildObj:
            return

    def getNowGuild(self):
        GuildID = self.Query("GuildID", 1)
        # 引导已经全部完毕
        if GuildID > max(self.GuildData.keys()):
            return {}

        if GuildID >= 1:
            self.sendGuild()
        return {}
        pass

    # 获取下一个引导
    def getNextGuild(self):
        GuildID = self.Query("GuildID", 1)
        # 引导已经全部完毕
        if GuildID > max(self.GuildData.keys()):
            return

        GuildKey = self.Query("GuildKey", 1)
        GuildStep = self.Query("GuildStep", 1)
        GuildObj = self.GuildData.get(GuildID)
        GuildID += 1

        NextGuildObj = self.GuildData.get(GuildID)
        if NextGuildObj:
            if NextGuildObj.ikey == GuildObj.ikey:
                GuildStep += 1
            else:
                GuildStep = 1
            GuildKey = GuildObj.ikey

        self.Set("GuildID", GuildID)
        self.Set("GuildKey", GuildKey)
        self.Set("GuildStep", GuildStep)
        if GuildID > 1:
            self.sendGuild()
        return {}

    def packGuild(self, GuildObj):
        id             = GuildObj.id         # id
        ikey           = GuildObj.ikey       #引导KEY
        istep          = GuildObj.istep     #步骤
        itype          = GuildObj.itype     #类型
        btnkey         = GuildObj.btnkey    #界面引导按钮编号
        innerIndex     = GuildObj.innerIndex#子界面引导编号
        desc           = GuildObj.desc      #备注
        isFight        = GuildObj.isFight   #触发
        data = {
            "id": id,
            "ikey": ikey,
            "istep": istep,
            "itype": itype,
            "btnkey": btnkey,
            "innerIndex": innerIndex,
            "desc": desc,
            "isFight": isFight,}
        self.broadcast("GuildInfo", data)


