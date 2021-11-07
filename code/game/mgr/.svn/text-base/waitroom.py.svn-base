#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from game.common import utility

from corelib.frame import Game, MSG_FRAME_STOP
from game.models.server import ModelServer
from corelib.gtime import get_days
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import weakref


# 房间管理器
class CWaitRoomMng(object):
    _rpc_name_ = "rpc_wait_mgr"
    def __init__(self):
        super(CWaitRoomMng, self).__init__()
        self.RoomTranceNo = 0
        self.dRoom = {}
        print "------------>>>>>>>>> CWaitRoomMng1----    -------"

    def start(self):
        print "------------>>>>>>>>> CWaitRoomMng1-----------"
        print "CWaitRoomMng start"
        pass

    # 获取房间流水号
    def getRoomNo(self):
        self.RoomTranceNo += 1
        return self.RoomTranceNo

    # 加入房间
    def JoinRoom(self, pid):
        print "----JoinRoom 1111111111", pid
        matchRes = 0
        res = None
        print "self.dRoom",self.dRoom
        for id, rommObj in self.dRoom.iteritems():
            if matchRes == 1:continue
            if rommObj.CanJoin():
                res = rommObj.Join(pid)
                if not res:
                    matchRes = 0
                else:
                    matchRes = 1
                    rommObj.checkRemoveRoomPVP()
                    break
        if not matchRes:
            res = self.RegisterRoom(pid)
        return res

    def RegisterRoom(self, pid):
        print "----RegisterRoom",pid
        roomid = pid#self.getRoomNo()
        player = get_rpc_player(pid)
        roomObj = CPaoPaoWaitRoom(self, roomid)
        self.dRoom[roomid] = roomObj
        res = roomObj.Join(pid)
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
        self.lWaitting = []
        self.maxCount = 2
        self.status = 0 # 房间状态 0：没人，1：等待中，2：匹配成功, 3:pve
        self.task_timmer = None
        print "========CPaoPaoWaitRoom",RoomId,mrg
        self.countDownPVE()

    def broadcast(self, fname, data, exclude=()):
        """ 广播 """
        # from game.mgr.player import get_rpc_player
        print "-------broadcast", self.lWaitting
        for pid in self.lWaitting:
            if pid in exclude:
                continue
            rpc_player = get_rpc_player(pid)
            rpc_player.broadcast(fname, data, _no_result=True)

    # def broadcast(self, fname, data):
    #     for pid, player in self.dWaitting.iteritems():
    #         player.broadcast(fname, data)

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
        for pid in self.lWaitting:
            player = get_rpc_player(pid)
            data[pid] = player.get_role_base()
        return data

    def Join(self, pid):
        print "-----------Join", pid
        if len(self.lWaitting) >= self.maxCount:
            return False
        print "===========1 pass"
        # if self.dWaitting.has_key(player.UID()):
        #     return False
        if pid in self.lWaitting:
            return 0
        print "===========2 pass"
        # self.dWaitting[player.UID()] = player
        self.lWaitting.append(pid)
        print "===========3 pass",self.lWaitting,
        player = get_rpc_player(pid)
        player.setWaitingRoomid(self.RoomId)
        self.status = 1
        print "--------len", len(self.lWaitting), self.maxCount
        if len(self.lWaitting) >= self.maxCount:
            print "==========Match Success"
            self.status = 2
            self.syncRoomInfo()
            self.MatchSuccessPVP()
        else:
            print "========== ????"
            self.syncRoomInfo()
        return self.packRoomPlayers()

    # 同步房间信息
    def syncRoomInfo(self):
        data = {}
        data["status"] = self.status
        data['lWaitting'] = self.packRoomPlayers()
        self.broadcast("waitinginfo", data)

    def LeaveRoom(self, pid):
        if pid in self.lWaitting:
            self.lWaitting.pop(pid)
            # del self.dWaitting[player.UID()]
        if len(self.lWaitting) <= 0:
            self.status = 0
            self.RemoveSelf()
        else:
            self.syncRoomInfo()

    def RemoveSelf(self):
        if len(self.lWaitting) <= 0:
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
        self.clearTimmer()
        print "-----------------MatchSuccessPVP", self.lWaitting
        for pid in self.lWaitting:
            # player.roomid = 0
            player = get_rpc_player(pid)
            player.gotoFightServer(self.RoomId, self.lWaitting, 1)
            pass

    def checkRemoveRoomPVP(self):
        # 删除等待房间
        if self.status == 2:
            self.lWaitting = []
            self.RemoveSelf()
        # self.mrg.RemoveRoom(self.RoomId)
        # self.mrg = None



    # 匹配超时 PVE模式
    def MatchSuccessPVE(self):
        print "-----------------MatchSuccessPVE",self.lWaitting
        if len(self.lWaitting) >= self.maxCount:
            self.MatchSuccessPVP()
            return
        self.status = 3
        self.syncRoomInfo()
        self.clearTimmer()
        for pid in self.lWaitting:
            # player.roomid = 0
            player = get_rpc_player(pid)
            player.gotoFightServer(self.RoomId, self.lWaitting, 2, _no_result=True)
        #for pid in self.lWaitting:
            ## player.roomid = 0
            #player = get_rpc_player(pid)
            #player.gotoFightServer(self.RoomId, self.lWaitting, 2)
        self.lWaitting = []
        self.RemoveSelf()
        print "-----------------MatchSuccessPVE Finish", self.lWaitting
        pass

# if not globals().has_key("gCWaitRoomMng"):
#     gCWaitRoomMng = CWaitRoomMng()

from corelib import spawn, log, spawn_later
from game.mgr.player import get_rpc_player
import config
#---------------------
#---------------------
#---------------------


