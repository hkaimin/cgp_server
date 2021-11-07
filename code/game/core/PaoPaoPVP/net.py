#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

from corelib.message import observable
from corelib import spawn_later, log, spawn
from corelib.gtime import current_time
from game import Game
from game.define import errcode, msg_define, constant

# @observable
# player里面的 netCmd继承
class netCmd(object):
    # 协议处理模块
    def __init__(self):

        pass

    # 开始匹配
    def start_match(self,who):
        print "----start_match"
        res = Game.rpc_wait_mgr.JoinRoom(who.id)
        # game.core.WaitRoom.gCWaitRoomMng.JoinRoom(self)
        return res



    # =========================== 泡泡相关 ===========================
    def getPaopaoFreeRoomId(self):
        # """ 获取西游有位置的房间id """
        rooms = []
        for svrs in Game.app_svrs.itervalues():
            rpc_sub_room_mgr = svrs.get(SubPaopaoRoomMgr._rpc_name_)
            if rpc_sub_room_mgr:
                rid = rpc_sub_room_mgr.get_free_room()
                # print "-------------rid", rid
                if rid:
                    rooms.append(rid)
        if len(rooms) > 0:
            return rooms[0]
        return 0

    def rc_enterPPRoom(self, who):
        """ 进入房间 """
        rid = self.getPaopaoFreeRoomId()
        if rid == 0:
            rs, data = Game.rpc_paopao_room_mgr.new_room(who.id)# 如果没有可用房间就创建新房间
            if not rs:
                return 0, data
            rid = data.get("rid",0)
        if rid == 0:
            return 0, errcode.EC_CREATE_ERR

        app_name, addr = Game.rpc_paopao_room_mgr.get_sub_mgr_by_rid(rid)
        if not app_name:
            return 0, errcode.EC_NOFOUND
        who.rpc_room = get_paopao_room_proxy(addr, rid)
        rs, data = who.rpc_room.enter_wait(self.id,self.data.name, self.base.headPic, self.base.to_base_fight()) # 进入游戏
        # if rs:
        #     spawn(self.rpc_room.enter, self.id, self.name,self.data.icon)
        return rs, data

    def rc_EnterWait(self, who):
        rs, data = who.outToFight()
        if rs:
            game.core.NewWaitRoom.gCNewWaitRoomMng.EnterPaoPaoRoom(who.id)
            try:
                Game.glog.log2File("startPVP",
                                   "%s|%s|%s" % (
                                   who.id, who.Name(), who.data.account))
            except:
                pass
        return 1, {}

    def rc_ExitWait(self, who):
        who.outToFight()
        return 1, {}



    def rc_enterPPRoomPVP(self, rid, is1v1=0):
        who = self
        app_name, addr = Game.rpc_paopao_room_mgr.get_sub_mgr_by_rid(rid)
        if not app_name:
            return 0, errcode.EC_NOFOUND
        room_mgr = self.checkhasroom(rid)
        playerData = who.pack_to_fight_wait()
        if room_mgr:
            self.Set("PPRoomID", rid)
            room_mgr.setHandler(rid,playerData)
            who.router_to_fightserver(addr[0], addr[1])  # 添加战斗服链接
        who.rpc_room = get_paopao_room_proxy(addr, rid)
        # print "-----------------------1",rid,who.id
        rs, data = who.rpc_room.enter_wait(who.id, who.data.name, who.base.headPic, who.pack_to_fight(), who.packFightEffect(),is1v1) # 进入游戏
        who.rpc_room.setloopCheck()
        pass

    def checkhasroom(self, roomID):
        # """ 获取西游有位置的房间id """
        rooms = []
        for svrs in Game.app_svrs.itervalues():
            rpc_sub_room_mgr = svrs.get(SubPaopaoRoomMgr._rpc_name_)
            if rpc_sub_room_mgr:
                res = rpc_sub_room_mgr.check_has_room(roomID)
                if res:
                    return rpc_sub_room_mgr
        return 0

    def rc_enterPPRoomPVE(self, rid):
        who = self
        app_name, addr = Game.rpc_paopao_room_mgr.get_sub_mgr_by_rid(rid)
        # sAddr = "%s:%s"%(addr[0],addr[1])
        # who.getHandler().add_router(1, sAddr)
        if not app_name:
            return 0, errcode.EC_NOFOUND
        playerData = self.pack_to_fight_wait()
        # gwid = playerData.get("gwid")
        room_mgr = self.checkhasroom(rid)
        if not room_mgr:
            return
        else:
            self.Set("PPRoomID", rid)
            room_mgr.change_room_to_Pve(rid, playerData)
        who.rpc_room = get_paopao_room_proxy(addr, rid)
        # print "-----------------------1",rid,who.id,[who.getHandler().rpc.pid]
        # print "-----who.getHandler().rpc.pid-",[who.getHandler().rpc.pid]
        # 等待连接成功后才返回,要不前端在得到返回后马上发送的数据可能会丢失
        # who.handler.connect(*addr)
        # sAddr = "%s:%s"%(addr[0],addr[1])
        # who.getHandler().add_router(1, sAddr)
        # who.getHandler().connect(*addr)
        rs, data = who.rpc_room.enter_wait(who.id,who.data.name, who.base.headPic, who.pack_to_fight(), who.packFightEffect()) # 进入游戏
        who.router_to_fightserver(addr[0],addr[1]) # 添加战斗服链接
        who.rpc_room.setloopCheck()
        pass

    def rc_enterPPRoomPVEGuanKa(self, rid):
        who = self
        app_name, addr = Game.rpc_paopao_room_mgr.get_sub_mgr_by_rid(rid)
        # sAddr = "%s:%s"%(addr[0],addr[1])
        # who.getHandler().add_router(1, sAddr)
        if not app_name:
            return 0, errcode.EC_NOFOUND
        playerData = self.pack_to_fight_wait()
        # gwid = playerData.get("gwid")
        room_mgr = self.checkhasroom(rid)
        if not room_mgr:
            return
        else:
            self.Set("PPRoomID", rid)
            room_mgr.check_room_to_Pve_Guanka(rid, playerData)
            # room_mgr.change_room_to_Pve(rid, playerData)
        who.rpc_room = get_paopao_room_proxy(addr, rid)
        #
        # print "-----------------------1",rid,who.id,[who.getHandler().rpc.pid]
        # print "-----who.getHandler().rpc.pid-",[who.getHandler().rpc.pid]
        # 等待连接成功后才返回,要不前端在得到返回后马上发送的数据可能会丢失
        # who.handler.connect(*addr)
        # sAddr = "%s:%s"%(addr[0],addr[1])
        # who.getHandler().add_router(1, sAddr)
        # who.getHandler().connect(*addr)
        # print "-------}}}",who.id,who.data.name, who.base.headPic, who.pack_to_fight_GuanKa(), who.packFightEffect()
        rs, data = who.rpc_room.enter_wait(who.id,who.data.name, who.base.headPic, who.pack_to_fight_GuanKa(), who.packFightEffect()) # 进入游戏
        who.router_to_fightserver(addr[0],addr[1]) # 添加战斗服链接
        who.rpc_room.setloopCheck()
        pass

    # 开房间
    def open1V1Room(self):
        self.remove1V1Room()
        rs, data = self.outToFight()
        key = 0
        if rs:
            key = game.core.NewWaitRoom.gCNewWaitRoomMng.creatFriend1v1(self)
            self.Set("roomkey1v1", key)
            try:
                Game.glog.log2File("start1V1Room",
                                   "%s|%s|%s" % (
                                   self.id, self.Name(), self.data.account))
            except:
                pass
        return 1, {"roomkey":key}


    def open1V1RoomByMap(self, mapId):
        # 设置出战地图
        self.remove1V1Room()
        rs, data = self.outToFight()
        rid = self.id
        mapInfo = Game.rpc_diymap_info.setFightMap(rid, mapId)
        print "------mapInfo---", mapInfo
        if mapInfo:
            self.Set("select1V1Map", mapInfo)
        key = 0
        if rs:
            key = game.core.NewWaitRoom.gCNewWaitRoomMng.creatFriend1v1(self, mapInfo)
            self.Set("roomkey1v1", key) # 自己开的房间
            self.Set("playRoomKey", key) # 正在玩的好友对战房间号
            try:
                Game.glog.log2File("start1V1RoomByMap",
                                   "%s|%s|%s" % (
                                   self.id, self.Name(), self.data.account))
            except:
                pass
        #print "------------roomkey---",key
        return 1, {"roomkey":key}

        # 移除房间(只有房主能发)

    def remove1V1RoomInLogin(self, isLogin=False):
        roomkey1v1 = self.Query("playRoomKey")
        print "-------remove1V1RoomInLogin-------",roomkey1v1,isLogin
        isInRoom = False
        if roomkey1v1:
            isInRoom = game.core.NewWaitRoom.gCNewWaitRoomMng.checkFriend1V1(self, roomkey1v1)
        if not isInRoom and roomkey1v1:
            self.remove1V1Room()
        return isInRoom

    # 移除房间(只有房主能发)
    def remove1V1Room(self):
        roomkey1v1 = self.Query("roomkey1v1")
        self.Delete("select1V1Map")
        self.Delete("playRoomKey")
        if roomkey1v1:
            self.Delete("roomkey1v1")
            game.core.NewWaitRoom.gCNewWaitRoomMng.delFriend1V1(self, roomkey1v1)
        return 1, {}

    # 删除角色1v1用到的信息
    def delete1V1RoomRoleInfo(self):
        self.Delete("select1V1Map")
        self.Delete("playRoomKey")
        self.Delete("roomkey1v1")

    # 好友邀请进入1V1
    def enter1V1Room(self, roomKey):
        rs, data = self.outToFight()
        if rs:
            roomkey1v1 = self.Query("playRoomKey")
            isInRoom = False
            if roomkey1v1 == int(roomKey):
                print "------enter1V1Room-111"
                isInRoom = self.remove1V1RoomInLogin(True)
            if not isInRoom:
                print "------enter1V1Room-222"
                print self.id
                print "roomKey:", roomKey
                game.core.NewWaitRoom.gCNewWaitRoomMng.getIntoFriend1V1(self, int(roomKey))
                try:
                    Game.glog.log2File("enter1V1Room",
                                       "%s|%s|%s|%s" % (
                                           self.id, self.Name(), self.data.account,roomKey))
                except:
                    pass
            return 1, {"roomkey", int(roomKey)}

    def leaveGame1v1(self, roomKey):
        rs, data = self.outToFight()
        if rs:
            print self.id
            print "roomKey:", roomKey
            game.core.NewWaitRoom.gCNewWaitRoomMng.leaveGame1v1(self, int(roomKey))
            return 1, {"roomkey", int(roomKey)}

    def setReady1V1(self, roomKey):
        game.core.NewWaitRoom.gCNewWaitRoomMng.setReady1V1(self, int(roomKey))
        try:
            Game.glog.log2File("setReady1V1",
                               "%s|%s|%s|%s" % (
                                   self.id, self.Name(), self.data.account, roomKey))
        except:
            pass
        return 1, {"roomkey", int(roomKey)}

    def startGame1V1(self, roomKey):
        game.core.NewWaitRoom.gCNewWaitRoomMng.startGame1V1(self, int(roomKey))
        try:
            Game.glog.log2File("startGame1V1",
                               "%s|%s|%s|%s" % (
                                   self.id, self.Name(), self.data.account, roomKey))
        except:
            pass
        return 1, {"roomkey", int(roomKey)}

    # 刷新在线状态
    def reflashOnline1V1Room(self):
        roomkey = self.Query("playRoomKey", 0) # 正在玩的好友对战房间号
        if not roomkey:
            return
        game.core.NewWaitRoom.gCNewWaitRoomMng.setIsOnline(self, roomkey)
        return 1, {"roomkey", int(roomkey)}

    # 离开泡泡
    def ppGameOver(self, dFightEffect, dFightAdd, mode):
        # import traceback
        # traceback.print_stack()
        print "-----------ppGameOver !!!!!!!!!!!!!!!!!!!!", [mode]
        who = self
        who.useFightEffect(dFightEffect, mode) # 扣除特效使用次数（如果有）
        who.remove_router() # 关闭战斗链接
        who.rpc_room = None
        self.dealFightAdd(dFightAdd)
        who.reflash_role_data()
        who.G2C_getWXInfo()

    # 处理战斗中得到的
    def dealFightAdd(self, dFightAdd):
        addcoin = dFightAdd.get("addcoin")
        self.base.setCoin(addcoin) # 添加金币



    def rc_syncPos(self,who, x, y, direction, speed, idx, playerID=0):
        # print "-------rc_syncPos", x, y, direction, speed, idx
        if who.rpc_room:
            err, data = who.rpc_room.syncPos(who.id, x, y, direction, speed, idx, playerID)
            return err, data
        return 0, errcode.EC_VALUE

    def rc_syncPut(self, who, x, y, idx, playerID):
        print "-------rc_syncPut", x, y, idx, playerID
        if who.rpc_room:
            err, data = who.rpc_room.syncPut(int(who.id), int(x), int(y), int(idx), int(playerID))
            return err, data
        return 0, errcode.EC_NOT_PAOPAO_CAN_PUT

    def rc_syncBoomPlayer(self, who, paopaoID, x, y, idx, killrid=0, killidx=-1, playerID=0):
        print "rc_syncBoomPlayer",paopaoID, x, y, idx, killrid, killidx
        if who.rpc_room:
            who.rpc_room.syncBoomPlayer(who.id, int(paopaoID), int(x), int(y), int(idx), int(killrid), int(killidx), int(playerID))
            return 1, {}
        return 0, errcode.EC_VALUE

    def rc_syncBoomZhuan(self, who, paopaoID, x, y, idx,  breakidx=-1, playerID=0):
        if who.rpc_room:
            who.rpc_room.syncBoomZhuan(who.id, int(paopaoID), int(x), int(y), int(idx),  int(breakidx), int(playerID))
            return 1, {}
        return 0, errcode.EC_VALUE

    def rc_pickItem(self, who, itype, idx, playerID):
        if who.rpc_room:
            who.rpc_room.pickItem(who.id, itype, idx, int(playerID))
            return 1, {}
        return 0, errcode.EC_VALUE

    def rc_exitPPRoom(self, who):
        """ 退出房间 """
        if who.rpc_room:
            print "-----------------rc_exitPPRoom",who.id
            rs, err = who.rpc_room.exit(who.id)
            who.remove_router()
            if rs:
                who.rpc_room = None
            return rs, err
        return 0, errcode.EC_NO_ROOM


    # =========================== 泡泡相关 ===========================


from game.mgr.paopao.paopaoroom import SubPaopaoRoomMgr, get_paopao_room_proxy
import game.core.NewWaitRoom