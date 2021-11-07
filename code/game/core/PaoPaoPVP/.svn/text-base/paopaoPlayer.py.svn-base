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


class PaopaoRoomPlayer(object):

    def __init__(self, fatherInst, pid, name, icon, dAttr, dPlayerEffect={}):
        # print "-----------PaopaoRoomPlayer", dAttr, name,icon
        self.fatherInst = weakref.proxy(fatherInst)
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
        self.iClass = 1      # 角色ID
        self.paopaocountMax = 1 # 最大可恢复泡泡数量
        self.paopaocount = 1 # 当前泡泡数量
        self.dTask_timmer = {}  # 任务计时器
        self.player_side = 1 # 玩家持方， 1 = 1p，2 = 2
        self.timmer_id = 0
        self.addcoin = 0 # 捡到的金币
        self.addExpprecent = 0
        self.canMove = 1 # 是否可移动
        self.isAI = 0
        self.mapInfo = {}
        self.iStart = int(time.time())
        self.iKillCnt = 0
        self.buff = {} # 当前身上的buff
        self.skillUseTime = {} # 技能使用时间{技能ID：下次技能使用时间}
        self.BUFFCACHE = {}
        self.setStartTime()
        self.setRoleBuff() # 设置角色BUFF, 战斗外带进来的属性
        self.init_class()
        self.init_player()
        self.init_own_map()

    # 设置角色BUFF, 战斗外带进来的属性
    def setRoleBuff(self):
        # # {key1:info1,...}
        # info {effectkey, num, times, cycle}
        # dKEYS = {1:"LIFE", 2:"SPEED", 3:"COUNT", 4:"POWER"}
        for key, dinfo in self.dPlayerEffect.iteritems():
            num = dinfo.get("num")
            fight_mode  = dinfo.get("fight_mode")
            if fight_mode != self.fatherInst.fight_mode:
                continue
            self.dFightEffectBuff[key] = num

    def init_player(self):
        # if not self.base:
        #     return
        # 读取角色属性
        RoleInfoObj = Game.res_mgr.res_roleData.get(self.iClass)
        pvp_life = RoleInfoObj.pvp_life
        pvp_speed = RoleInfoObj.pvp_speed
        pvp_power = RoleInfoObj.pvp_power
        pvp_cnt = RoleInfoObj.pvp_cnt
        # 读取道具增益
        self.life = pvp_life + self.dFightEffectBuff.get("LIFE", 0)
        self.speed = pvp_speed + self.dFightEffectBuff.get("SPEED",0)
        self.power = pvp_power + self.dFightEffectBuff.get("POWER",0)
        self.paopaocount = pvp_cnt
        self.paopaocountMax = self.paopaocount
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

    def getPPSkinID(self):
        return self.base.get("PPSkin", 1)

    def getPPEffectID(self):
        return self.base.get("PPEffectID", 1)

    def getPPSkillData(self):
        return self.base.get("dSkill", {})

    def getSkillInfoBySkillID(self, skillID):
        dSkill = self.getPPSkillData()
        return dSkill.get(skillID, {})

    # 初始化自己的地图
    def init_own_map(self):
        self.mapInfo = self.base.get("fightMap", {})
        if self.base.get("select1V1Map", {}):
            self.mapInfo = self.base.get("select1V1Map", {})

    # 初始化职业
    def init_class(self):
        self.iClass = self.base.get("fightClass", 1)

    def getMyMapBgconf(self):
        return self.mapInfo.get("bgconf", [])

    def getMyMapLayerConf(self):
        return self.mapInfo.get("layerconf", [])

    def getIsTrain(self):
        return self.base.get("isTrain", 0)

    def setIsAI(self):
        self.isAI = 1
        pass

    # 设置玩家持方
    def setPlayerSide(self, idx=1):
        if idx <1:
            idx = 1
        elif idx >2:
            idx = 2
        self.player_side = idx

    def setStartTime(self):
        self.start_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.starttime = int(time.time())

    def setEndTime(self):
        self.endtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.duringtime = int(time.time()) - self.starttime


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
            "PPSkinID":self.getPPSkinID(), # 泡泡皮肤ID
            "PPEffectID": self.getPPEffectID(),  # 泡泡特效ID
            "iClass":self.iClass,
            "dSkill":self.getPPSkillData()
        }
        return data

    def packRoleResult(self):
        data = {
            "uid": self.pid,
            "name": self.name,
            "icon": self.icon,
            "Lv": self.lv,
            "life":self.getLife(), # 多少条命
            "speed":self.getSpeed(), # 速率
            "power":self.getPower(), # 威力
            "paopaocount":self.getPaopaoCountMax(), # 个数
            "player_side":self.player_side, # 玩家持方， 1 = 1p，2 = 2
            "win":self.win, # 是否获胜
            "coin":self.coin, # 总金币数
            "addcoin":self.addcoin, # 当局增加金币
            "MaxExp":self.exp, # 当前最大经验
            "curExp":self.curexp, # 当前经验值
            "addExp":self.addExp, # 当局获得经验
        }
        print "----------------------------------"
        print data
        print "----------------------------------"
        return data

    def packBackToMain(self):
        data = {
            "addcoin":self.addcoin, # 增加的金币
        }
        return data

    def addCoin(self, iadd):
        self.addcoin += iadd

    # 增加经验百分比
    def addExpPrecent(self, iAdd):
        self.addExpprecent = self.addExpprecent + iAdd
        pass

    def Upgrade(self, exp):
        exp = int(exp)
        # self.lv = 0         # 等级
        # self.exp = 0        # 经验
        # self.curexp = 0     # 当前经验
        lv = self.lv
        nextExp = self.getNextLvExp()
        curexp = self.curexp
        if lv >=30:return
        if curexp < nextExp:
            curexp += exp
        if curexp >= nextExp :
            lv += 1
            nexExp = self.getNextLvExp(lv)
            curexp = curexp - nextExp
            self.lv = lv
            self.exp = nexExp
            self.curexp = curexp
            if curexp >= nexExp:
                self.Upgrade(curexp)
        else:
            self.curexp = curexp
        print exp, self.exp,self.curexp ,self.lv
        return lv

    def getNextLvExp(self, lv=0):
        if not lv:
            lv = self.lv
        if lv == 0:
            lv = 1
            self.lv = lv
        curUpGradeObj = Game.res_mgr.res_upgrade.get(lv)
        nextExp = curUpGradeObj.exp
        return nextExp


    # 打包角色数据
    def packRoleBack(self, roomid=1, roomtype=1):
        data = {
            "uid": self.pid,
            "gametype":1,
            "roomid":roomid,
            "roomtype":roomtype,
            "starttime":self.start_dt,
            "endtime":self.endtime,
            "playtime":self.duringtime,
        }
        return data

    def getTimmerId(self):
        self.timmer_id += 1
        return self.timmer_id

    # 装弹
    def reloadPaoPaoTimmer(self):
        timmer_id = self.getTimmerId()
        task_timmer = spawn_later(3, self.reloadPaoPao, timmer_id)
        self.dTask_timmer[timmer_id] = task_timmer

    # 放炸弹
    def putPaoPao(self):
        if self.getPaopaoCount() <= 0: return
        self.paopaocount -= 1
        self.reloadPaoPaoTimmer()

    # 重新上弹
    def reloadPaoPao(self,timmer_id=0):
        # print "---------------------------------------2222222222222", timmer_id
        task_timmer = self.dTask_timmer.get(timmer_id)
        if task_timmer:
            task_timmer.kill(block=False)
            del self.dTask_timmer[timmer_id]
        if self.paopaocount < self.paopaocountMax:
            self.paopaocount+=1

    # 是否可以放炸弹
    def canPutPaoPao(self):
        if self.getPaopaoCount() > 0:
            return True
        else:
            return False

    # 结算完之后要做的事
    # 升级
    # 同步排行榜
    # 触发事件等
    def afterResult(self, isWin=False):
        print "-------afterResult--"
        if self.isAI or self.getIsTrain():
            return
        from game.mgr.player import get_rpc_player
        addcoin = 0
        if self.win:
            timePoint = (600 - (int(time.time() - self.iStart)))
            if timePoint < 0:
                timePoint = 0
            addExp = timePoint + 300 + self.iKillCnt*300
            addcoin = 50
        else:
            addExp = 300
        self.addExp = addExp*(1+self.addExpprecent)
        rpc_player = get_rpc_player(self.pid)
        rpc_player.Upgrade(self.addExp, _no_result=True)
        if not isWin:
            rpc_player.updatePvpRank(0,_no_result=True)
        self.Upgrade(self.addExp)
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
        return self.getLife()

    # 增加速度
    def addSpeed(self, iAdd=1):
        self.speed += iAdd
        return self.getSpeed()

    # 增加威力
    def addPower(self, iAdd=1):
        self.power += iAdd
        return self.getPower()

    # 增加当前泡泡数量
    def addPaopaocount(self, addcount=1):
        self.paopaocountMax += addcount
        self.paopaocount += addcount
        return self.getPaopaoCountMax()

    def getLife(self):
        life = self.life + self.buffLife()
        return life

    def getSpeed(self):
        speed = self.speed + self.buffSpeed()
        if speed < 0:
            speed = 0
        return speed

    def getPower(self):
        power = self.power + self.buffPower()
        if power < 1:
            power = 1
        return power

    def getPaopaoCount(self):
        paopaocount = self.paopaocount + self.buffPaopaoCount()
        if paopaocount < 0:
            paopaocount = 0
        # if paopaocount <= 0 and self.isAI:
        #     paopaocount = 1
        return paopaocount

    def getPaopaoCountMax(self):
        paopaocountMax = self.paopaocountMax + self.buffPaopaoCountMax()
        if paopaocountMax < 0:
            paopaocountMax = 0
        # if paopaocountMax <= 0 and self.isAI:
        #     paopaocountMax = 1
        return paopaocountMax

    def buffLife(self):
        return self.buff.get("life", 0)

    def buffSpeed(self):
        return self.buff.get("speed", 0)

    def buffPower(self):
        return self.buff.get("power", 0)

    def buffPaopaoCount(self):
        return self.buff.get("paopaocnt", 0)

    def buffPaopaoCountMax(self):
        return self.buff.get("paopaocnt", 0)

    def ExitRoom(self):
        for id, ttimmer in self.dTask_timmer.iteritems():
            if ttimmer:
                ttimmer.kill(block=False)
        pass

    # 设置技能下一个可用的时间
    def setSkillNextUseTime(self, skillID, cd):
        skillInfo = self.getSkillInfoBySkillID(skillID)
        if not skillInfo:
            return False
        now = int(time.time())
        self.skillUseTime[skillID] = now + cd

    # 技能是否可以使用
    def getSkillCanUse(self, skillID):
        nextUseTime = self.skillUseTime.get(skillID, 0)
        if not nextUseTime:
            return True
        # skillInfo = self.getSkillInfoBySkillID(skillID)
        # if not skillInfo:
        #     return False
        # cd = skillInfo.get("cd", 0)
        # if not cd:
        #     return False
        now = int(time.time())
        if now >= nextUseTime:
            return True
        return False


    # 处理buff技能
    def dealbuff(self, skillType, dBuff, effectTime, skillID):
        #print "-------11-------",skillType, dBuff, effectTime, skillID
        red_speed = 0
        red_ppcnt = 0
        red_power  = 0
        key = "skillID_%s"%skillID
        if self.dTask_timmer.has_key(key):
            return
        self.BUFFCACHE[key] = dBuff
        self.buff.update(dBuff)
        task_timmer = spawn_later(effectTime, self.deleteBuff, key)
        self.dTask_timmer[key] = task_timmer
        self.fatherInst.reflashProperty()

    # 清除buff
    def deleteBuff(self, key):
        task_timmer = self.dTask_timmer.get(key)
        if task_timmer:
            task_timmer.kill(block=False)
            del self.dTask_timmer[key]
        lastBuff = self.BUFFCACHE.get(key,{})
        # print "88888888888888888888888", key, self.buff, lastBuff
        for buffname, value in lastBuff.iteritems():
            nowValue = self.buff.get(buffname, 0)
            if value:
                nowValue = nowValue - value
                if nowValue < 0:
                    nowValue = 0
                self.buff[buffname] = nowValue
        # print "88888888888888888888888", key, self.buff
        del self.BUFFCACHE[key]
        self.fatherInst.reflashProperty()


import random
import types
from datetime import datetime
from game.core.PaoPaoPVP.paopaoMap import *
# import paopaoSkill
import game.core.skill.conf
import copy