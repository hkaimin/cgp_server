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
import game.core.PaoPaoPVP.paopaoPlayer


class PaopaoRoomPlayer(game.core.PaoPaoPVP.paopaoPlayer.PaopaoRoomPlayer):

    def __init__(self, fatherInst, pid, name, icon, dAttr, dPlayerEffect={}):
        super(PaopaoRoomPlayer, self).__init__(fatherInst, pid, name, icon, dAttr, dPlayerEffect)
        # print "00000000000000>>>>1111111111111", dAttr
        self.pid = pid
        self.name = name
        self.icon = icon
        self.base = dAttr
        self.dPlayerEffect = dPlayerEffect # 主服传过来的战斗属性
        self.dFightEffectBuff = {} # 主服传过来的战斗属性 buff
        self.win = 0
        self.duringtime = 0
        # 战斗属性
        self.life = 1        # 多少条命
        self.speed = 1       # 速率
        self.power = 1       # 威力
        self.paopaocountMax = 1 # 最大可恢复泡泡数量
        self.paopaocount = 1 # 当前泡泡数量
        self.dTask_timmer = {}  # 任务计时器
        self.player_side = 1 # 玩家持方， 1 = 1p，2 = 2
        self.timmer_id = 0
        self.addcoin = 0 # 捡到的金币
        self.addExpprecent = 0
        self.canMove = 1 # 是否可移动
        self.isAI = 0
        self.aiLevel = self.base.get("aiLevel", 0)
        self.mapInfo = {}
        self.iStart = int(time.time())
        self.iKillCnt = 0
        self.lWalkArea = []  # [x,y] (单位：格)
        # # self.setStartTime()
        # # self.setRoleBuff()
        # # self.init_own_map()
        # self.init_class()
        # # self.init_player()
        self.buff = {} # 当前身上的buff
        self.skillUseTime = {} # 技能使用时间{技能ID：下次技能使用时间}
        self.setStartTime()
        self.setRoleBuff() # 设置角色BUFF, 战斗外带进来的属性
        self.init_class()
        self.init_player()
        self.init_own_map()


    def setAiLevel(self, iLv):
        self.aiLevel = iLv
        pass

    # 设置角色BUFF, 战斗外带进来的属性
    # def setRoleBuff(self):
    #     # # {key1:info1,...}
    #     # info {effectkey, num, times, cycle}
    #     # dKEYS = {1:"LIFE", 2:"SPEED", 3:"COUNT", 4:"POWER"}
    #     for key, dinfo in self.dPlayerEffect.iteritems():
    #         num = dinfo.get("num")
    #         self.dFightEffectBuff[key] = num

    def init_player(self):
        # if not self.base:
        #     return
        if not self.isAI: # 如果是玩家
            RoleInfoObj = Game.res_mgr.res_roleData.get(self.iClass)
            pve_life = RoleInfoObj.pve_life
            pve_speed = RoleInfoObj.pve_speed
            pve_power = RoleInfoObj.pve_power
            pve_cnt = RoleInfoObj.pve_cnt
            self.life = pve_life + self.dFightEffectBuff.get("LIFE", 0)
            self.speed = pve_speed + self.dFightEffectBuff.get("SPEED", 0)
            self.power = pve_power + self.dFightEffectBuff.get("POWER", 0)
            self.paopaocount = pve_cnt
            self.paopaocountMax = pve_cnt
        else:
            pve_life = self.base.get("aiLift", 1)
            pve_speed = self.base.get("aiSpeed", 1)
            pve_cnt = self.base.get("aiPaoNum", 1)
            pve_power = self.base.get("aiPower", 1)
            self.iClass = self.base.get("aiClass", 1)
            self.life = pve_life
            self.speed = pve_speed
            self.power = pve_power
            self.paopaocount = pve_cnt
            self.paopaocountMax = pve_cnt
        self.lv = self.base.get("lv", 1)
        self.exp = self.base.get("exp", 0)
        self.curexp = self.base.get("curexp", 1)
        self.coin = self.base.get("coin", 1)
        self.addExp = 0
        self.addcoin = 0
        if self.name == "":
            self.name = '玩家'
        addPPcount = self.dFightEffectBuff.get("COUNT",0)
        if addPPcount:
            self.addPaopaocount(int(addPPcount))



    def setStartTime(self):
        self.start_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.starttime = int(time.time())

    def setEndTime(self):
        self.endtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.duringtime = int(time.time()) - self.starttime



    # def packRoleBase(self):
    #     data = {
    #         "uid": self.pid,
    #         "name": self.name,
    #         "icon": self.icon,
    #         "Lv": 1,
    #         "life":self.life, # 多少条命
    #         "speed":self.speed, # 速率
    #         "power":self.power, # 威力
    #         "paopaocount":self.paopaocountMax, # 个数
    #         "player_side":self.player_side, # 玩家持方， 1 = 1p，2 = 2
    #         "isAI":self.isAI, # 0：正常玩家，1：AI
    #         "aiLevel":self.aiLevel,
    #         "PPSkinID":self.getPPSkinID(), # 泡泡皮肤ID
    #         "PPEffectID": self.getPPEffectID(),  # 泡泡特效ID
    #         "iClass": self.iClass,
    #         "dSkill": self.getPPSkillData()
    #     }
    #     return data

    def packRoleBaseBT(self):
        # self.addPaopaocount(10)
        # self.speed = 10
        # self.power = 10

        data = {
            "uid": self.pid,
            "name": self.name,
            "icon": self.icon,
            "Lv": 1,
            "life":self.life, # 多少条命
            "speed":self.speed, # 速率
            "power":self.power, # 威力
            "paopaocount":self.paopaocountMax, # 个数
            "player_side":self.player_side, # 玩家持方， 1 = 1p，2 = 2
            "isAI":self.isAI, # 0：正常玩家，1：AI
            "aiLevel":self.aiLevel,
            "PPSkinID":self.getPPSkinID(), # 泡泡皮肤ID
            "PPEffectID": self.getPPEffectID(),  # 泡泡特效ID
            "iClass": self.iClass
        }
        return data

    def packRoleBase(self):
        data = {
            "uid": self.pid,
            "name": self.name,
            "icon": self.icon,
            "Lv": 1,
            "life":self.getLife(), # 多少条命
            "speed":self.getSpeed(), # 速率
            "power":self.getPower(), # 威力
            "paopaocount":self.getPaopaoCountMax(), # 个数
            "player_side":self.player_side, # 玩家持方， 1 = 1p，2 = 2
            "isAI":self.isAI, # 0：正常玩家，1：AI
            "aiLevel": self.aiLevel,
            "PPSkinID":self.getPPSkinID(), # 泡泡皮肤ID
            "PPEffectID": self.getPPEffectID(),  # 泡泡特效ID
            "iClass":self.iClass,
            "dSkill":self.getPPSkillData(),
            "lWalkArea":self.lWalkArea
        }
        return data

    def packBackToMain(self):
        data = {
            "addcoin":self.addcoin, # 增加的金币
        }
        return data

    def getTimmerId(self):
        self.timmer_id += 1
        return self.timmer_id

    # 结算完之后要做的事
    # 升级
    # 同步排行榜
    # 触发事件等
    def afterResult(self, star = 0):
        if self.isAI:
            return
        from game.mgr.player import get_rpc_player
        if self.win:
            timePoint = (500 - (int(time.time() - self.iStart)))
            if timePoint < 0:
                timePoint = 0
            addExp = timePoint + star*100 + self.iKillCnt*(star*50)
        else:
            addExp = 30
        self.addExp = addExp*(1+self.addExpprecent)
        rpc_player = get_rpc_player(self.pid)
        rpc_player.Upgrade(self.addExp, _no_result=True)
        self.Upgrade(self.addExp)
        addcoin = 20*star
        self.addCoin(addcoin)
        pass

    def addKill(self):
        self.iKillCnt += 1

    # 被打中
    def beHurt(self):
        self.life -= 1
        return self.life

    # 死亡
    def isDie(self):
        return not bool(self.life)

    # 新一轮
    def newRound(self):
        pass

    def setWin(self):
        self.win = 1

    def isWin(self):
        return self.win == 1

    def setLose(self):
        pass

    # 获得分数（金币）
    def Score(self, score):
        pass

    # 增加命
    def addLife(self):
        self.life += 1
        return self.life

    # 增加速度
    def addSpeed(self, iAdd=1):
        self.speed += iAdd
        return self.speed

    # 增加威力
    def addPower(self, iAdd=1):
        self.power += iAdd
        return self.power

    # 增加当前泡泡数量
    def addPaopaocount(self, addcount=1):
        self.paopaocountMax += addcount
        self.paopaocount += addcount
        return self.paopaocountMax

    def packRoleResult(self):
        data = {
            "uid": self.pid,
            "name": self.name,
            "icon": self.icon,
            "Lv": self.lv,
            "life":self.life, # 多少条命
            "speed":self.speed, # 速率
            "power":self.power, # 威力
            "paopaocount":self.paopaocountMax, # 个数
            "player_side":self.player_side, # 玩家持方， 1 = 1p，2 = 2
            "win":self.win, # 是否获胜
            "coin":self.coin, # 总金币数
            "addcoin":self.addcoin, # 当局增加金币
            "MaxExp":self.exp, # 当前最大经验
            "curExp":self.curexp, # 当前经验值
            "addExp":self.addExp, # 当局获得经验
            "star":0,             # 获得星星数
            "GuanKaDesc":""       #
        }

        return data

import random
import types
from datetime import datetime
from game.core.PaoPaoPVP.paopaoMap import *
