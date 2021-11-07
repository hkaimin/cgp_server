#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import weakref

from corelib import log, spawn
from corelib.gtime import current_time
from corelib.message import observable
from gevent import sleep
from gevent.lock import RLock

from PlayerMail import PlayerMail
from cycleData import CycleDay, CycleWeek, CycleMonth, CycleHour
from game import Game
from game.core.playerBase import PlayerBase
from game.define import errcode, msg_define, constant
from game.models.player import ModelPlayer


# 房间管理器
class CWaitRoomMng(object):
    def __init__(self):
        super(CWaitRoomMng, self).__init__()
        self.RoomTranceNo = 0
        self.dRoom = {}
        print "------------>>>>>>>>> CWaitRoomMng"

    # 获取房间流水号
    def getRoomNo(self):
        self.RoomTranceNo += 1
        return self.RoomTranceNo

    # 加入房间
    def JoinRoom(self, player):
        matchRes = 0
        res = None
        for id, rommObj in self.dRoom.iteritems():
            if matchRes == 1:continue
            if rommObj.CanJoin():
                res = rommObj.Join(player)
                if not res:
                    matchRes = 0
                else:
                    matchRes = 1
        if not matchRes:
            res = self.RegisterRoom(player)
        return res

    def RegisterRoom(self, player):
        roomid = self.getRoomNo()
        roomObj = CPaoPaoWaitRoom(self, roomid)
        self.dRoom[roomid] = roomObj
        res = roomObj.Join(player)
        return res

    def FindRoom(self, iSeq):
        return self.dRoom.get(iSeq, None)

    def RemoveRoom(self, iSeq):
        if self.dRoom.has_key(iSeq):
            del self.dRoom[iSeq]


class CPaoPaoWaitRoom(object):
    def __init__(self, mrg, RoomId):
        super(CPaoPaoWaitRoom, self).__init__()
        self.RoomId = RoomId
        self.mrg = mrg
        self.dWaitting = {}
        self.maxCount = 2
        self.status = 0 # 房间状态 0：没人，1：等待中，2：匹配成功, 3:pve
        self.task_timmer = None

    def broadcast(self, fname, data):
        for pid, player in self.dWaitting.iteritems():
            player.broadcast(fname, data)

    def countDownPVE(self):
        if self.task_timmer:
            self.task_timmer.kill(block=False)
            self.task_timmer = None
        self.task_timmer = spawn_later(10, self.MatchSuccessPVE)

    def clearTimmer(self):
        if self.task_timmer:
            self.task_timmer.kill(block=False)
            self.task_timmer = None


    def packRoomPlayers(self):
        data = {}
        for pid, player in self.dWaitting.iteritems():
            data[pid] = player.get_role_base()
        return data

    def Join(self, player):
        if len(self.dWaitting) >= self.maxCount:
            return False
        if self.dWaitting.has_key(player.UID()):
            return False
        self.dWaitting[player.UID()] = player
        player.WaitingRoomid = self.RoomId
        self.status = 1
        if len(self.dWaitting) >= self.maxCount:
            self.status = 2
            self.syncRoomInfo()
            self.MatchSuccessPVP()
        else:
            self.syncRoomInfo()
        return self.packRoomPlayers()

    # 同步房间信息
    def syncRoomInfo(self):
        data = {}
        data["status"] = self.status
        data['lwaiting'] = self.packRoomPlayers()
        self.broadcast("waitinginfo", data)

    def LeaveRoom(self, player):
        if self.dWaitting.has_key(player.UID()):
            del self.dWaitting[player.UID()]
        if len(self.dWaitting) <= 0:
            self.status = 0
            self.RemoveSelf()
        else:
            self.syncRoomInfo()

    def RemoveSelf(self):
        if len(self.dWaitting) <= 0:
            self.clearTimmer()
            self.mrg.RemoveRoom(self.RoomId)
            self.lWaitting = []
            self.mrg = None

    def CanJoin(self):
        if len(self.lWaitting) >= self.maxCount:
            return False
        else:
            return True

    # 匹配成功
    def MatchSuccessPVP(self):
        # 两个人拉入战斗房间，房间ID为等待房间的ID，即唯一ID号

        for pid, player in self.dWaitting.iteritems():
            # player.roomid = 0
            player.gotoFightServer(self.RoomId, player.keys())
            pass
        # 删除等待房间
        self.lWaitting = []
        self.RemoveSelf()
        # self.mrg.RemoveRoom(self.RoomId)
        # self.mrg = None

    # 匹配超时 PVE模式
    def MatchSuccessPVE(self):
        self.status = 3
        self.syncRoomInfo()
        self.lWaitting = []
        self.RemoveSelf()
        pass

if not globals().has_key("gCWaitRoomMng"):
    gCWaitRoomMng = CWaitRoomMng()

from corelib import spawn, log, spawn_later
import config
import testcontainer
import game.mgr.player
#---------------------
#---------------------
#---------------------


