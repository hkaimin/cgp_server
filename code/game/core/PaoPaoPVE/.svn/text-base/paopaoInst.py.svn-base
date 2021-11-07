#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import random
from gevent import sleep
from corelib import spawn, log, spawn_later
from game.define import errcode,msg_define
from game import Game
from game.common import utility
import config
from corelib.frame import Game
import weakref
import game.core.PaoPaoPVP.paopaoInst
from game.define.constant import *

# ============== 战斗模式
# APP_MODE_PVP = 1
# APP_MODE_PVE = 2
# APP_MODE_PVE_GUANKA = 3

PAOPAO_EXIST_TIME = 0

PAOPAO_MAX_TOUCHTIME = 8 # 泡泡最大碰撞次数

class PaopaoPVEInst(game.core.PaoPaoPVP.paopaoInst.PaopaoInst):
    """ 房间类 """
    def __init__(self, mgr, rid, mode=1, max=2):
        super(PaopaoPVEInst, self).__init__(mgr, rid, mode, max, True)
        self.id = rid #房间id
        # self.roomType = mode #房间类型（1:PVP,）
        # self.mgr = mgr1
        self.mgr = weakref.proxy(mgr)
        self.name = "" #名称
        self.fight_mode = APP_MODE_PVE # PVE模式
        self.map_mode = 2 # 9*11
        self.max = max #最大人数
        self.state = 0 # 0:匹配，1，准备, 2:已开始
        # self.isGoReady = False
        self._st = 0 #当前局开始时间
        # self.players = {} #房间玩家列表 id：roomPlayer
        self.lplayers= [] # 匹配队列
        self.readys = {} #EC_VALUE
        self.Map = Game.res_mgr.dPvpMapData
        self.isOver = False
        self._loop_task = None
        self.task_timmer = None # 任务计时器
        self.canJoin = True
        self.mapObj = None # 地图对象
        self.dPaoPao = {}
        self.iPaopaoTranceNo = 0
        self.random_name_data = Game.res_mgr.res_name  # 随机名字表

        # Game.sub(msg_define.MSG_ROLE_LEVEL_UPGRADE, self.event_lv_uprade)

    # 获取AI随机名字
    def getRandAIName(self):
        namekeys = self.random_name_data.keys()
        namekey = random.choice(namekeys)
        randomNameObj = self.random_name_data.get(namekey)
        if randomNameObj:
            return randomNameObj.name
        else:
            return "随机名字"

    def InitPVE(self):
        self.NameRes = Game.res_mgr.res_name

    # def check(self):
    #     # while 1:
    #     #     sleep(60)
    #     #     if len(self.players) == 0:
    #     #         self.end()
    #     pass

    def broadcast(self, fname, data, exclude=()):
        """ 广播 """
        # print "-------------PaopaoPVEInst", fname, self.id
        from game.mgr.player import get_rpc_player
        for pid, player in self.players.iteritems():
            if pid in exclude:
                continue
            if pid <= 10000 and pid > 1:
                continue
            # data1 = self.packRoomPlayer(player
            # data["roleInfo"] = data1
            rpc_player = get_rpc_player(pid)
            rpc_player.broadcast(fname, data, _no_result=True)

    def getPaopaoTranceNo(self):
        self.iPaopaoTranceNo += 1
        return self.iPaopaoTranceNo


    # 房间是否满员
    def IsFull(self):
        if len(self.players) >= self.max and self.canJoin:
            return True
        if self.state > 0:
            return True
        return False
    # 是否空房间
    def InEmpty(self):
        if len(self.players) == 0:
            return True
        return False

    def canJoin(self):
        if self.fight_mode == APP_MODE_PVE:
            if len(self.players) >= 1:
                return False
        return True

    # 获取房间详细信息
    # def get_info(self):
    #     return dict(rid=self.id, name=self.name, money=self.money, count=len(self.players),
    #                 max=self.max, isEncrypted=self.isEncrypted)


    #=========================匹配等待=======================
    # AI进入
    def makeAI(self):
        pid = random.randint(1,10000)
        name =  self.getRandAIName()
        icon = ""
        iClass = random.randint(1,4)
        ppskil = random.randint(1,6)
        dAttr = {"fightClass":iClass, "PPSkin":ppskil}
        player = game.core.PaoPaoPVP.paopaoPlayer.PaopaoRoomPlayer(self, pid, name, icon, dAttr)
        player.setIsAI()
        return player


    def enter_wait(self, pid, name, icon, dAttr, dEffect={}):
        # self.players[pid]
        print "------PVE WAIT-----pid",pid,self.id
        # 玩家 坐下
        if not self.players.has_key(pid):
            player = game.core.PaoPaoPVP.paopaoPlayer.PaopaoRoomPlayer(self, pid, name, icon, dAttr, dEffect)
            self.players[pid] = player
            player.setPlayerSide(len(self.players))

        # ai 坐下
        aiPlayer = self.makeAI()
        aiPid = aiPlayer.pid
        if not self.players.has_key(aiPid):
            self.players[aiPid] = aiPlayer
            aiPlayer.setPlayerSide(len(self.players))

        print "AI PID: ",aiPid
        print "AI Name:",aiPlayer.name

        if len(self.players) >=2:
            print "match success!!!", self.players.keys()
            self.state = 1
            self.MatchSuccessPVP()
            self.syncWaitingInfo()
            return 1, {}
        else:
            self.syncWaitingInfo()
            return 1, {}






import random
import types
from datetime import datetime
from game.core.PaoPaoPVP.paopaoMap import *
import game.core.PaoPaoPVP.paopaoPlayer
