#!/usr/bin/env python
# -*- coding:utf-8 -*-
from corelib import log
from corelib.common import IterId
from corelib.frame import MSG_FRAME_APP_ADD, MSG_FRAME_APP_DEL
from grpc import get_proxy_by_addr, DictExport, DictItemProxy
from game import Game
from game.define import errcode
# from game.core.PaoPaoPVP.paopaoroom import PaopaoInst
import game.core.PaoPaoPVP.paopaoInst as Inst
import game.core.PaoPaoPVE.paopaoInst as InstPVE
import game.core.PaoPaoPVEGuanKa.paopaoInst as InstPVEGuanKa

from corelib.cache import TimeMemCache


def get_paopao_room_proxy(addr, rid):
    proxy = get_proxy_by_addr(addr, SubPaopaoRoomMgr._rpc_name_, DictItemProxy)
    if proxy:
        proxy.dict_name = 'rooms'
        proxy.key = rid
    return proxy

class GPaopaoRoomMgr(object):
    """泡泡全局房间管理"""
    _rpc_name_ = 'rpc_paopao_room_mgr'

    def __init__(self):
        self.iter_id = IterId()
        self._mgrs = {}
        self.rid2mgr = {} #{rid:(app_name, addr)}
        Game.sub(MSG_FRAME_APP_ADD, self._msg_app_add)
        Game.sub(MSG_FRAME_APP_DEL, self._msg_app_del)

    def _msg_app_add(self, app_name, addr, names):
        """子房间进程注册"""
        if SubPaopaoRoomMgr._rpc_name_ not in names:
            return
        log.info('[GPaopaoRoomMgr] reg sub_room_mgr:%s', app_name)
        sub_mgr = get_proxy_by_addr(addr, SubPaopaoRoomMgr._rpc_name_)
        self._mgrs[app_name] = sub_mgr
        sub_mgr.sub_id = app_name
        sub_mgr.rooms = set()
        sub_mgr.addr = tuple(addr)

    def _msg_app_del(self, app_name, addr, names):
        """子房间进程反注册"""
        if SubPaopaoRoomMgr._rpc_name_ not in names:
            return
        log.info('[GPaopaoRoomMgr]unreg sub_room_mgr:%s', app_name)
        sub_mgr = self._mgrs.pop(app_name, None)
        for rid in sub_mgr.rooms:
            self.rid2mgr.pop(rid)

    def new_room(self, pid, isFriend1V1=False):
        """ 新建房间 """
        sub_mgr = self.get_free_sub_mgr()
        rid = 0
        for i in xrange(10):
            rid = self.iter_id.next()
            if rid not in self.rid2mgr:
                break
        if not rid:
            return 0, errcode.EC_CREATE_ERR
        sub_mgr.new_room_old(pid, rid, isFriend1V1)

        sub_mgr.rooms.add(rid)
        self.rid2mgr[rid] = (sub_mgr.sub_id, sub_mgr.addr)
        return 1, dict(rid=rid)

    # mode {1: pvp, 2:pve}
    def new_room_FightServer(self, pid, roomid, mode=1):
        """ 新建房间 """
        sub_mgr = self.get_free_sub_mgr()
        rid = roomid
        if rid in self.rid2mgr:
            return 1, dict(rid=rid)
        if not rid:
            return 0, errcode.EC_CREATE_ERR
        sub_mgr.new_room(pid, rid, mode)
        sub_mgr.rooms.add(rid)
        self.rid2mgr[rid] = (sub_mgr.sub_id, sub_mgr.addr)
        return 1, dict(rid=rid)

    def del_room(self, rid):
        """ 房间关闭 """
        app_name, addr = self.rid2mgr.pop(rid)
        sub_mgr = self._mgrs.get(app_name, None)
        if sub_mgr and rid in sub_mgr.rooms:
            sub_mgr.rooms.remove(rid)

    def get_sub_mgr_by_rid(self, rid):
        return self.rid2mgr.get(rid)

    def get_free_sub_mgr(self):
        """ 获取一个最空闲的子房间管理器"""
        _min = None
        for sub_mgr in self._mgrs.itervalues():
            if _min is None:
                _min = sub_mgr
            else:
                _min = sub_mgr if _min.get_count() > sub_mgr.get_count() else _min
        return _min

    def get_player_count(self):
        """ 获取当前房间总人数 """
        count = 0
        for sub_mgr in self._mgrs.itervalues():
            count += sub_mgr.get_count()
        return count

class SubPaopaoRoomMgr(DictExport):
    """西游子房间管理器"""
    _rpc_name_ = 'rpc_sub_paopao_room_mgr'

    def __init__(self):
        self.rooms = {}  # {room_id : room}
        # self.gwidData = {} # {gwpid:playerdata}
        self.rid2gwpid = {} # {rid : [gwpid1,...]}
        self._keys = TimeMemCache(size=200, default_timeout=5 * 60, name='SubPaopaoRoomMgr._keys')
        self.dHanlder = {}

    def gw_open(self, processor):
        """ 新连接 """
        print "=-==============CCCCXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        print "=-==============CCCCXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",processor
        process_id = processor.pid
        hd = game.protocal.paopaoFightRpcHandler.paopaoFightRpcHandler()
        hd.set_rpc(processor)
        # print "------------------->>>> gw_open 3", hd, hd.rpc
        playerData = self._keys.delete(process_id)
        # playerData = self.gwidData.get(process_id)\
        # print "==============================>>11"
        self.set_handler(processor, hd, playerData)

    def set_handler(self, processor, hd, playerData):
        print "==============set_handler================>>11_22",hd,playerData
        print "-=---processor.pid---::::::::::",processor.pid
        if self.dHanlder.get(processor.pid):
            self.dHanlder.get(processor.pid).uninit()
        self.dHanlder[processor.pid] = hd
        if playerData:
            roomObj = playerData.get("room")
            playerId = playerData.get("playerId")
            hd.setRoomAndPlayerId(roomObj, playerId)
            #print "-0-------------//////////", playerId, processor
            roomObj.setProcessor(playerId, processor)
            # print "--------change to pve", self.rooms[rid]
        else:
            if self.rooms.has_key(rid):
                roomObj = self.rooms.get(rid)
                roomObj.setProcessor(playerId, processor)

    def setHandlerReconnect(self, rid, playerData):
        gwid = playerData.get("gwid")
        roomObj = self.rooms.get(rid)
        playerData["room"] = roomObj
        playerData["roomId"] = rid
        self._keys.set(gwid, playerData)
        # self.rid2gwpid.setdefault(rid, [])
        # self.rid2gwpid[rid].append(gwid)

    def stop(self):
        #等待所有房间完成？
        pass

    def get_count(self):
        count = 0
        for room in self.rooms.itervalues():
            count += len(room.players)
        return count

    def get_rooms_info(self):
        """ 获取房间列表信息 """
        data = []
        for room in self.rooms.itervalues():
            info = room.get_info()
            data.append(info)
        return data

    def check_roomid_exist(self, roomid, players):
        room = self.rooms.get(roomid)
        # 如果房间里面已经有其中一位玩家进去了
        if not room:
            return 0
        for pid in players:
            if pid in room.players.keys():
                return roomid
        return 0

    def check_has_room(self, roomid):
        room = self.rooms.get(roomid)
        if room:
            return roomid
        else:
            return 0

    def get_free_room(self):
        """ 获取有位置的房间id """
        for rid, room in self.rooms.iteritems():
            if not room.IsFull():
                return rid
        return 0

    def get_Empty_room(self):
        """ 获取有位置的房间id """
        for rid, room in self.rooms.iteritems():
            if room.InEmpty() and not room.getIs1V1():
                return rid
        return 0

    def new_room_old(self, pid, rid, isFriend1V1=False):
        log.debug('[SubPaopaoRoomMgr]new_room:%s', rid)
        room = Inst.PaopaoInst(self, rid, 1)
        if isFriend1V1:
            room.setIs1V1()
        self.rooms[rid] = room

    def change_room_to_Pve(self, rid, playerData):
        log.debug('[SubPaopaoRoomMgr]change_room_to_Pve:%s', rid)
        # gwid = playerData.get("gwid")
        if self.rooms.has_key(rid):
            self.rooms[rid] = InstPVE.PaopaoPVEInst(self, rid, 1)
        # playerData["room"] = self.rooms[rid]
        # playerData["roomId"] = rid
        # # self.gwidData[gwid] = playerData
        # self._keys.set(gwid, playerData)
        # self.rid2gwpid.setdefault(rid, [])
        # self.rid2gwpid[rid].append(gwid)
        self.setHandler(rid, playerData)

    def check_room_to_Pve_Guanka(self, rid, playerData):
        if self.rooms.has_key(rid):
            self.rooms[rid] = InstPVEGuanKa.PaoPaoPVEGuanKaInst(self, rid, 1)
        self.setHandler(rid, playerData)
        pass


    def setHandler(self, rid, playerData):
        gwid = playerData.get("gwid")
        roomObj = self.rooms.get(rid)
        playerData["room"] = roomObj
        playerData["roomId"] = rid
        self._keys.set(gwid, playerData)
        self.rid2gwpid.setdefault(rid, [])
        self.rid2gwpid[rid].append(gwid)

    # def new_room(self, pid, rid, money, max, password):
    #     """ 新建房间 """
    #     log.debug('[SubPaopaoRoomMgr]new_room:%s', rid)
    #     room = PaopaoRoom(self, rid, money, max, password)
    #     self.rooms[rid] = room

    def new_room(self, pid, rid, mode):
        room = Inst.PaopaoInst(self, rid, mode)
        self.rooms[rid] = room

    def del_room(self, room):
        """ 关闭房间 """
        if room.id not in self.rooms:
            return
        # print "--------------1", self.rid2gwpid
        # print "--------------1", self.dHanlder
        # print "--------------1", self.rooms
        log.debug('[SubPaopaoRoomMgr]del_room:%s', room.id)
        # self.rooms.pop(room.id)
        del self.rooms[room.id]
        if self.rid2gwpid.get(room.id):
            lgwpid = self.rid2gwpid.get(room.id, [])
            self.removeHandler(lgwpid)
            del self.rid2gwpid[room.id]
        Game.rpc_paopao_room_mgr.del_room(room.id)
        # print "--------------2", self.rid2gwpid
        # print "--------------2", self.dHanlder
        # print "--------------2", self.rooms

    def removeHandler(self, lgwpid):
        for gwpid in lgwpid:
            # if self.gwidData.get(gwpid):
            #     del self.gwidData[gwpid]
            if self.dHanlder.get(gwpid):
                del self.dHanlder[gwpid]

import game.protocal.paopaoFightRpcHandler
