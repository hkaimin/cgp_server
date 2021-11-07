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
from game.define import errcode, msg_define, constant, protocol_define
from game.define.constant import *

# APP_MODE_PVP = 1
# APP_MODE_PVE = 2

PAOPAO_EXIST_TIME = 0

PAOPAO_MAX_TOUCHTIME = 8 # 泡泡最大碰撞次数

class CPaopaoWaitRoom(object):
    """ 房间类 """
    def __init__(self):
        self.players = {}
        self.rooms = {}
        self.room1v1 = {}
        self.timmer_id = 1
        self.roomID1V1 = 600000001 # 好友邀请房间
        self.dTask_timmer = {}  # 任务计时器

    def getRoomID1V1(self):
        self.roomID1V1 += 1
        return self.roomID1V1

    def getTimmerId(self):
        self.timmer_id += 1
        return self.timmer_id

    def check(self):
        while 1:
            sleep(60)
            if len(self.players) == 0:
                self.end()

    def end(self):

        # if self.task_timmer:
        #     self.task_timmer.kill(block=False)
        #     self.task_timmer = None
        self.isOver = True


    def Test(self):
        print "Test ========================== 1:"
        return 1, {}

    def broadcast(self, lplayer, fname, data, exclude=()):
        """ 广播 """
        for pid in lplayer:
            if pid in exclude:
                continue
            # data1 = self.packRoomPlayer(player)
            # data["roleInfo"] = data1
            rpc_player = get_rpc_player(pid)
            rpc_player.broadcast(fname, data, _no_result=True)

    def getPaopaoEmptyRoomId(self):
        # """ 获取pp有位置的房间id """
        rooms = []
        for svrs in Game.app_svrs.itervalues():
            rpc_sub_room_mgr = svrs.get(SubPaopaoRoomMgr._rpc_name_)
            if rpc_sub_room_mgr:
                rid = rpc_sub_room_mgr.get_Empty_room()
                print "-------------rid", rid
                if rid:
                    rooms.append(rid)
        if len(rooms) > 0:
            return rooms[0]
        return 0

    def checkHasRoom(self, playerId):
        pass


    def EnterPaoPaoRoom(self, playerId):
        # self.players[playerId] = [playerId]
        rid = self.getPaopaoEmptyRoomId()
        if rid == 0:
            rs, data = Game.rpc_paopao_room_mgr.new_room(playerId) # 如果没有可用房间就创建新房间
            if not rs:
                return 0, data
            rid = data.get("rid",0)

        self.players[playerId] = rid
        if not self.rooms.has_key(rid):
            self.rooms[rid] = [playerId]
        elif len(self.rooms[rid]) < 2:
            self.rooms[rid].append(playerId)
        else:
            del self.rooms[rid]
            self.EnterPaoPaoRoom(playerId)
            return
        print 'self.rooms:',self.rooms,self.rooms[rid]
        from game.mgr.player import get_rpc_player
        if len(self.rooms[rid]) >= 2:
            lPlayer = self.rooms[rid]
            # data["roleInfo"] = data1
            print 'lPlayer:',lPlayer
            for pid in lPlayer:
                rpc_player = get_rpc_player(pid)
                # rpc_player.getPaoPaoPvpNet().rc_enterPPRoomPVP(rid)
                # print rpc_player.netCmd
                # print rpc_player.base.getCoin()
                # rpc_player.rpc_Opera(protocol_define.PAOPAO_PVP, "rc_enterPPRoomPVP", rid)
                rpc_player.rc_enterPPRoomPVP(rid)
            self.cleanRoomInfo(rid, playerId)
            self.delPVETimmer(rid)
        else:
            rpc_player = get_rpc_player(playerId)
            data = {
                "state":0
            }
            rpc_player.broadcast("WaitingInfo", data)
            self.setPVETimmer(rid)
        pass

    # # 退出匹配
    # def ExitPaopaoRoom(self, who, playerId):
    #     rid =  self.players.get(playerId)
    #     if len(self.rooms[rid]) >= 2:
    #         return {"err":-1}
    #     if self.rooms.get(rid):
    #         if playerId in self.rooms[rid]:
    #             self.cleanRoomInfo(rid, playerId)
    #             self.delPVETimmer(rid)
    #     return {"err":1}

    # 删除PVE定时器
    def delPVETimmer(self, roomID):
        print "------delPVETimmer----",roomID
        task_timmer = self.dTask_timmer.get(roomID)
        if task_timmer:
            task_timmer.kill(block=False)
        if self.dTask_timmer.has_key(roomID):
            del self.dTask_timmer[roomID]

    # 设置PVE房间定时器
    def setPVETimmer(self, roomID):
        t = random.randint(2,5)
        task_timmer = spawn_later(t, self.changeToPVE, roomID)
        self.dTask_timmer[roomID] = task_timmer
        pass

    # 匹配超时，切换到PVE模式
    def changeToPVE(self, roomID):
        print "dsadsadad------"
        if not self.rooms.has_key(roomID):
            return
        # print "dsadsadad------1",self.rooms

        if len(self.rooms[roomID]) < 1:
            return
        from game.mgr.player import get_rpc_player
        lPlayer = self.rooms[roomID]
        if len(lPlayer) >= 2:
            return
        playerId = 0
        for pid in lPlayer:
            rpc_player = get_rpc_player(pid)
            # rpc_player.rpc_Opera(protocol_define.PAOPAO_PVP, "rc_enterPPRoomPVE", roomID) # protocol_define
            rpc_player.rc_enterPPRoomPVE(roomID) # protocol_define
            # print rpc_player.netCmd,rpc_player.netCmd.__name__,dir(rpc_player)
            # print rpc_player.get_owner()
            # print dir(rpc_player.netCmd)
            # print rpc_player.netCmd.PaoPaoPvpNet
            playerId = pid
        self.delPVETimmer(roomID)
        self.cleanRoomInfo(roomID,playerId)
        pass

    # 进入关卡
    def EnterPVEGuanKa(self, playerId, guankaInfo={}):
        from game.mgr.player import get_rpc_player
        rid = self.getPaopaoEmptyRoomId()
        if rid == 0:
            rs, data = Game.rpc_paopao_room_mgr.new_room(playerId) # 如果没有可用房间就创建新房间
            if not rs:
                return 0, data
            rid = data.get("rid",0)
        if not rid:
            return
        rpc_player = get_rpc_player(playerId)
        rpc_player.rc_enterPPRoomPVEGuanKa(rid)

    # 创建1V1
    def creatFriend1v1(self, who, mapInfo={}):
        # 用玩家id做key
        playerId = who.id
        key = self.getRoomID1V1()
        if not self.room1v1.get(key):
            matchRoom = CPlayer1V1Room()
            matchRoom.createRoom(who, key, mapInfo)
            self.room1v1[key] = matchRoom
        return key

    # 检查1V1房间是不是还在，还在的话就拉入
    def checkFriend1V1(self, who, roomKey):
        if not self.room1v1.has_key(int(roomKey)):
            return False
        matchRoom = self.room1v1.get(int(roomKey))
        if not matchRoom:
            return False
        print "-----------------checkFriend1V1",roomKey,who.id
        return self.setIsOnline(who, roomKey)


    # 删除房间key
    def delFriend1V1(self, who, key):
        if self.room1v1.has_key(key):
            roomObj = self.room1v1.get(key)
            if not roomObj:
                return
            lplayer = roomObj.lplayer
            for rid in lplayer:
                if rid == who.id:
                    continue
                from game.mgr.player import get_rpc_player
                rpc_player = get_rpc_player(rid)
                rpc_player.delete1V1RoomRoleInfo()
            roomObj.notifyRoomDismiss(who)
            del self.room1v1[key]

    # 进入1v1
    def getIntoFriend1V1(self, who, roomKey):
        print "--------self.room1v1", self.room1v1, roomKey
        roomKey = int(roomKey)
        if not self.room1v1.has_key(int(roomKey)):
            who.notify("房间已解散！")
            return
        matchRoom = self.room1v1.get(roomKey)
        lplayer = matchRoom.lplayer
        if who.id in lplayer:
            # self.setIsOnline(who, roomKey)
            return
        if who.id == matchRoom.roommer:
            # self.setIsOnline(who, roomKey)
            return
        matchRoom.addPlayer(who)
        who.Set("playRoomKey", roomKey)  # 正在玩的好友对战房间号

    # 设置准备
    def setReady1V1(self, who, roomKey):
        if not self.room1v1.has_key(int(roomKey)):
            who.notify("房间已解散！")
            return
        matchRoom = self.room1v1.get(roomKey)
        lplayer = matchRoom.lplayer
        if who.id not in lplayer:
            matchRoom.addPlayer(who)
        matchRoom.setisReady(who)

    # 刷新是否在线
    def setIsOnline(self, who, roomKey):
        if not self.room1v1.has_key(int(roomKey)):
            who.notify("房间已解散！")
            return False
        matchRoom = self.room1v1.get(roomKey)
        if not matchRoom:
            return False
        lplayer = matchRoom.lplayer
        if who.id not in lplayer:
            return False
        return matchRoom.setisOnine(who)

    # 开始1V1
    def startGame1V1(self, who, roomKey):
        if not self.room1v1.has_key(int(roomKey)):
            who.notify("房间已解散！")
            return
        matchRoom = self.room1v1.get(roomKey)
        lplayer = matchRoom.lplayer
        readyCnt = matchRoom.getAllReady()
        if readyCnt == 2:
            self.EnterPaoPaoRoomBy1V1(lplayer)
            del self.room1v1[roomKey]

    # 退出1v1房间
    def leaveGame1v1(self, who, roomKey):
        print "===========leaveGame1v1==========1",roomKey
        if not self.room1v1.has_key(int(roomKey)):
            who.notify("房间已解散！")
            return
        matchRoom = self.room1v1.get(roomKey)
        lplayer = matchRoom.lplayer
        if who.id not in lplayer:
            return
        print "===========leaveGame1v1==========1",roomKey
        matchRoom.leaveRoom(who)
        # if matchRoom.lplayer == 0: # 房主
        #     self.delFriend1V1(who, roomKey)

    # 进入1v1
    def getIntoFriend1V1Old(self, who, roomKey):
        print "self.room1v1:",self.room1v1,roomKey
        if not self.room1v1.has_key(int(roomKey)):
            who.notify("房间已解散！")
            return
        self.room1v1[roomKey].append(who.id)
        lplayer = self.room1v1[roomKey]
        if len(lplayer) == 2:
            self.EnterPaoPaoRoomBy1V1(lplayer)
            del self.room1v1[roomKey]

    # 进入1V1
    def EnterPaoPaoRoomBy1V1(self, lPlayer):
        rid = self.getPaopaoEmptyRoomId()
        if rid == 0:
            rs, data = Game.rpc_paopao_room_mgr.new_room(lPlayer[0]) # 创建新房间
            if not rs:
                return 0, data
            rid = data.get("rid",0) # 房间id
        from game.mgr.player import get_rpc_player
        print 'lPlayer:',lPlayer
        for pid in lPlayer:
            rpc_player = get_rpc_player(pid)
            if rpc_player:
                rpc_player.rc_enterPPRoomPVP(rid,1)
        self.delPVETimmer(rid)


    def cleanRoomInfo(self, rid, playerId):
        if self.rooms.has_key(rid):
            del self.rooms[rid]
        if self.players.has_key(playerId):
            del self.players[playerId]
        print "del room", rid, self.rooms

    # 离开匹配房间
    def playerLeaveRoom(self, pid):
        if not self.players.has_key(pid):
            return
        rid = self.players[pid]
        if self.rooms.has_key(rid):
            if len(self.rooms[rid]) >= 2:
                self.rooms[rid].remove(pid)
            else:
                del self.rooms[rid]
        if self.players.has_key(pid):
            del self.players[pid]
        self.delPVETimmer(rid)
        pass



MAX_1V1_PLAYER = 2

# 1V1房间类
class CPlayer1V1Room(object):
    def __init__(self):
        self.roomID  = 0    # 房间ID
        self.roommer = 0    # 房主
        self.lplayer = []   # 等待玩家
        self.dplayer = {}
        self.useMap = {}    # 使用的地图
        self.room1V1Type = 1 # 邀请好友类型 1：随机地图， 2：DIY地图

    def bCanAdd(self):
        if len(self.lplayer) >= MAX_1V1_PLAYER:
            return False
        return True

    def createRoom(self, who, key, mapInfo={}):
        self.roomID = key
        self.roommer = who.id
        self.useMap = mapInfo
        self.addPlayer(who)
        self.setisReady(who)
        if mapInfo:
            self.room1V1Type = 2

    def addPlayer(self, who):
        playerID = who.id
        playerInfo = self.makeplayerInfo(who)
        if playerID in self.lplayer:
            return
        self.lplayer.append(playerID)
        self.dplayer[playerID] = playerInfo
        self.showMatch1v1RoomUI()

    # 刷新是否在线
    def setisOnine(self, who):
        dInfo = self.dplayer.get(who.id, {})
        if not dInfo:
            return False
        dInfo["isOnline"] = int(who.logined)
        print  "--------setisOnine---", dInfo, self.dplayer, self.lplayer
        self.showMatch1v1RoomUI()
        return True

    def getAllReady(self):
        readyCnt = 0
        for pid, dInfo in self.dplayer.iteritems():
            isReady = dInfo.get("isReady", 0)
            if isReady:
                readyCnt += 1
        return readyCnt

    # 准备
    def setisReady(self, who):
        dInfo = self.dplayer.get(who.id, {})
        if not dInfo:
            return
        dInfo["isReady"] = 1
        self.showMatch1v1RoomUI()

    # 角色数据
    def makeplayerInfo(self, who):
        dInfo = {
            "rid":who.id,
            "name":who.name,
            "head":who.base.getIcon(),
            "iLv":who.base.lv,
            "isOnline":int(who.logined),
            "isReady":0
        }
        return dInfo

    def broadcast(self, fname, data, exclude=()):
        """ 广播 """
        from game.mgr.player import get_rpc_player
        for rid in self.lplayer:
            if rid in exclude:
                continue
            # data1 = self.packRoomPlayer(player)
            # data["roleInfo"] = data1
            rpc_player = get_rpc_player(rid)
            rpc_player.broadcast(fname, data, _no_result=True)

    #
    def changeMap(self, who, dMapData):
        if who.id != self.roommer:
            return
        self.useMap = dMapData


    # 显示1v1匹配UI
    def showMatch1v1RoomUI(self):
        lShowInfo = []
        for rid in self.lplayer:
            WaitplayerInfo = self.dplayer.get(rid, {})
            lShowInfo.append(WaitplayerInfo)
        dData = {
            "lWaitInfo":lShowInfo,
            "MapInfo":self.useMap,
            "room1V1Type":self.room1V1Type,# 邀请好友类型 1：随机地图， 2：DIY地图
            "roomID":self.roomID
        }
        print "-showMatch1v1RoomUI--", dData
        self.broadcast("showMatch1v1RoomUI", dData)

    # 离开房间
    def leaveRoom(self, who):
        if who.id not in self.lplayer:
            return
        self.lplayer.remove(who.id)
        if self.dplayer.get(who.id):
            del self.dplayer[who.id]
        self.showMatch1v1RoomUI()

    # 房间解散
    def notifyRoomDismiss(self, who):
        if who.id not in self.lplayer:
            return
        # if who.id != self.roommer:
        #     return
        dInfo = {
            "roomKey": self.roomID,
            "isDismiss" : 1
        }
        self.broadcast("Room1v1Dismiss", dInfo)
        self.roomID  = 0    # 房间ID
        self.roommer = 0    # 房主
        self.dplayer = {}
        self.useMap = {}    # 使用的地图
        self.lplayer = []


if not globals().has_key("gCNewWaitRoomMng"):
    gCNewWaitRoomMng = CPaopaoWaitRoom()

from corelib import spawn, log, spawn_later
from game.mgr.paopao.paopaoroom import SubPaopaoRoomMgr, get_paopao_room_proxy