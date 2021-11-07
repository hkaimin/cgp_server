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



class PaopaoRoomPlayer(object):

    def __init__(self, pid, name, icon, dAttr):
        print "-----------PaopaoRoomPlayer", dAttr
        self.pid = pid
        self.name = name
        self.icon = icon
        self.base = dAttr
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
        self.canMove = 1 # 是否可移动
        self.mapInfo = {}

        self.setStartTime()
        self.setRoleBuff()
        self.init_player()
        self.init_diy_map()

    def init_player(self):
        if not self.base:
            return
        self.life = self.base.get("life", 1)
        self.speed = self.base.get("speed", 1)
        self.power = self.base.get("power", 1)
        self.paopaocount = self.base.get("paopaocount", 1)
        self.lv = self.base.get("lv", 1)
        self.exp = self.base.get("exp", 0)
        self.curexp = self.base.get("curexp", 1)
        self.coin = self.base.get("coin", 1)
        self.addExp = 0
        self.addcoin = 0



    # 设置角色BUFF, 战斗外带进来的属性
    def setRoleBuff(self):
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
            "life":self.life, # 多少条命
            "speed":self.speed, # 速率
            "power":self.power, # 威力
            "paopaocount":self.paopaocountMax, # 个数
            "player_side":self.player_side # 玩家持方， 1 = 1p，2 = 2
        }
        return data

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
        }
        print "----------------------------------"
        print data
        print "----------------------------------"
        return data

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
        if self.paopaocount <= 0: return
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
        if self.paopaocount > 0:
            return True
        else:
            return False

    # # 结算完之后要做的事
    # # 升级
    # # 同步排行榜
    # # 触发事件等
    # def afterResult(self):
    #     from game.mgr.player import get_rpc_player
    #     if self.win:
    #         addExp = 1000
    #     else:
    #         addExp = 100
    #     self.addExp = addExp
    #     rpc_player = get_rpc_player(self.pid)
    #     rpc_player.Upgrade(addExp, _no_result=True)
    #     self.Upgrade(self.addExp)
    #     pass

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
    def addSpeed(self):
        self.speed += 1
        return self.speed

    # 增加威力
    def addPower(self):
        self.power += 1
        return self.power

    # 增加当前泡泡数量
    def addPaopaocount(self):
        self.paopaocountMax += 1
        self.paopaocount += 1
        return self.paopaocountMax




    def ExitRoom(self):
        for id, ttimmer in self.dTask_timmer.iteritems():
            if ttimmer:
                ttimmer.kill(block=False)
        pass


import random
import types
from datetime import datetime
from game.core.PaoPaoPVP.paopaoMap import *
