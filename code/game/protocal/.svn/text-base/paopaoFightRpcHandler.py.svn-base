#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import game.protocal.BasePlayerRpcHander
import weakref

class paopaoFightRpcHandler(game.protocal.BasePlayerRpcHander.BasePlayerRpcHander, ):
    """ 玩家rpc处理类 """
    DEBUG = 1

    def __init__(self):
        game.protocal.BasePlayerRpcHander.BasePlayerRpcHander.__init__(self)
        self.active = True
        self.room = None
        self.playerId = None

    def setRoomAndPlayerId(self, room, playerId):
        self.room = weakref.proxy(room)
        self.playerId = playerId

    def removeRoom(self):
        self.room = None

    def rc_heartbeat(self):
        return 1, None


    # 战斗服测试接口
    def rc_test(self,v):
        print "-------------rc_test-------", v, self.room, self.playerId
        # self.rc_syncPut(206,185,11)
        return 1, {"v":v}


    def rc_syncPos(self, x, y, direction, speed, idx,playerID=0):
        # print "--------------------222----"
        err, rs = self.room.syncPos(self.playerId, x, y, direction, speed, idx, playerID=playerID)
        return err, rs

    def rc_syncPut(self, x, y, idx,playerID=0):
        # print "------->>>>x, y, idx,playerID:",x, y, idx,playerID
        err, rs = self.room.syncPut(int(self.playerId), int(x), int(y), int(idx), int(playerID))
        return err, rs

    def rc_syncBoomPlayer(self, paopaoID, x, y, idx, killrid, killidx,playerID=0):
        self.room.syncBoomPlayer(self.playerId, int(paopaoID), int(x), int(y), int(idx), int(killrid), int(killidx), int(playerID))
        return 1, {}

    def rc_syncBoomZhuan(self, paopaoID, x, y, idx,  breakidx,playerID=0):
        self.room.syncBoomZhuan(self.playerId, int(paopaoID), int(x), int(y), int(idx), int(breakidx), int(playerID))
        return 1, {}

    def rc_pickItem(self, itype, idx,playerID=0):
        # print "-=---------rc_pickItem", itype, idx
        self.room.pickItem(self.playerId, itype, idx, int(playerID))
        return 1, {}

    # 上行 普通点击
    def rc_normalClick(self):
        self.room.normalClick(self.playerId)
        return 1, {}

    # 上行 特殊点击（购买额外点击次数）
    def rc_spCilck(self):
        self.room.spCilck(self.playerId)
        return 1, {}

    # 小游戏弃权，认输，直接用对手的地图
    def rc_giveup(self):
        self.room.miniGameGiveup(self.playerId)
        return 1, {}

    # 关卡碰门通关
    def rc_guangkaFinish(self, idx):
        self.room.guangkaFinish(self.playerId, idx)
        return 1, {}

    def rc_useSkill(self, skillID):
        self.room.useSkill(self.playerId, skillID)
        return 1, {}

    def rc_kill_player_by_monster(self, attacker_pid, beattacker_pid):
        self.room.kill_player_by_monster(attacker_pid, beattacker_pid)
        return 1, {}
