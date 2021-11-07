#!/usr/bin/env python
# -*- coding:utf-8 -*-
from gevent import sleep
from corelib import log, spawn
from corelib.cache import TimeMemCache
from corelib.common import IterId
from grpc import get_proxy_by_addr, wrap_pickle_result, RpcCallError, DictExport, DictItemProxy
from game import Game
from game.define import msg_define
from corelib.frame import MSG_FRAME_APP_ADD, MSG_FRAME_APP_DEL

# from game.core.xiyouroom import XiYouRoom
from game.define import errcode

def get_xiyou_room_proxy(addr, rid):
    proxy = get_proxy_by_addr(addr, SubXiYouRoomMgr._rpc_name_, DictItemProxy)
    if proxy:
        proxy.dict_name = 'rooms'
        proxy.key = rid
    return proxy

class GXiYouRoomMgr(object):
    """西游全局房间管理"""
    _rpc_name_ = 'rpc_xiyou_room_mgr'

    def __init__(self):
        self.iter_id = IterId()
        self._mgrs = {}
        self.rid2mgr = {} #{rid:(app_name, addr)}
        Game.sub(MSG_FRAME_APP_ADD, self._msg_app_add)
        Game.sub(MSG_FRAME_APP_DEL, self._msg_app_del)

    def _msg_app_add(self, app_name, addr, names):
        """子房间进程注册"""
        if SubXiYouRoomMgr._rpc_name_ not in names:
            return
        log.info('[GXiYouRoomMgr] reg sub_room_mgr:%s', app_name)
        sub_mgr = get_proxy_by_addr(addr, SubXiYouRoomMgr._rpc_name_)
        self._mgrs[app_name] = sub_mgr
        sub_mgr.sub_id = app_name
        sub_mgr.rooms = set()
        sub_mgr.addr = tuple(addr)

    def _msg_app_del(self, app_name, addr, names):
        """子房间进程反注册"""
        if SubXiYouRoomMgr._rpc_name_ not in names:
            return
        log.info('[GXiYouRoomMgr]unreg sub_room_mgr:%s', app_name)
        sub_mgr = self._mgrs.pop(app_name, None)
        for rid in sub_mgr.rooms:
            self.rid2mgr.pop(rid)

    def new_room(self, pid, money, max, password):
        """ 新建房间 """
        sub_mgr = self.get_free_sub_mgr()
        rid = 0
        for i in xrange(10):
            rid = self.iter_id.next()
            if rid not in self.rid2mgr:
                break
        if not rid:
            return 0, errcode.EC_CREATE_ERR
        sub_mgr.new_room(pid, rid, money, max, password)

        sub_mgr.rooms.add(rid)
        self.rid2mgr[rid] = (sub_mgr.sub_id, sub_mgr.addr)
        return 1, dict(rid=rid, money=money, max=max)


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

class SubXiYouRoomMgr(DictExport):
    """西游子房间管理器"""
    _rpc_name_ = 'rpc_sub_xiyou_room_mgr'

    def __init__(self):
        self.rooms = {}  # {room_id : room}

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

    def get_free_room(self):
        """ 获取有位置的房间id """
        for rid, room in self.rooms.iteritems():
            if not room.IsFull():
                return rid
        return 0

    def new_room(self, pid, rid, money, max, password):
        """ 新建房间 """
        log.debug('[SubXiYouRoomMgr]new_room:%s', rid)
        room = XiYouRoom(self, rid, money, max, password)
        self.rooms[rid] = room


    def del_room(self, room):
        """ 关闭房间 """
        if room.id not in self.rooms:
            return
        log.debug('[SubXiYouRoomMgr]del_room:%s', room.id)
        # self.rooms.pop(room.id)
        del self.rooms[room.id]
        Game.rpc_xiyou_room_mgr.del_room(room.id)

