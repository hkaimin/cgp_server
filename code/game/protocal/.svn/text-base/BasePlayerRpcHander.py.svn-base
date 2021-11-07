#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from gevent import sleep

from corelib import log
from game.common.gateway import AbsExport
from game.define import errcode, msg_define, constant, store_define




class BasePlayerRpcHander(AbsExport):
    DEBUG = 0
    MAIN_RPC = 1  # 是否rpc主连接

    if 0:
        from game.core import player as player_md

        player = player_md.Player()
        from game.common.gateway import Processer
        rpc = Processer()

    def __init__(self):
        setattr(self, 'player', None)
        setattr(self, 'rpc', None)

    @property
    def pid(self):
        return self.player.data.id if self.player else None

    @property
    def addr(self):
        return self.rpc.addr

    def uninit(self):
        setattr(self, 'player', None)
        self.set_rpc(None)

    def set_player(self, player):
        setattr(self, 'player', player)

    def set_rpc(self, process):
        log.debug('player(%s) handler(%s) set_rpc(%s)', self.pid, id(self),
                  id(process) if process is not None else process)
        if self.rpc:
            self.rpc.close(client=bool(self.MAIN_RPC))
        setattr(self, 'rpc', process)
        if process:
            self.rpc.set_export(self)

    def on_close(self, process):
        """ 断线处理 """
        print "---------> [handler]player(%s)on_close"%(self.pid)
        log.debug('[handler]player(%s)on_close', self.pid)
        self.set_rpc(None)
        if self.player:
            self.player.on_close()

    def call(self, fname, data, noresult=False, timeout=None):
        if self.rpc is None:
            log.warn('***send(fname=%s, data=%s) error: player(%s).handler(%s) ?? handler(%s) rpc_is_None', fname, data,
                     id(self.player) if self.player else None,
                     id(self.player._handler) if self.player else None,
                     id(self))
            return
        if self.DEBUG and fname not in ["syncPosBroadcase"]:
            log.debug('send-- fname %s, data %s', fname, data)
        self.rpc.call(fname, data, noresult=noresult, timeout=timeout)

    def getProcesserInfo(self):
        if self.rpc is None:
            log.warn('***getProcesserInfo error: player(%s).handler(%s) ?? handler(%s) rpc_is_None',
                     id(self.player) if self.player else None,
                     id(self.player._handler) if self.player else None,
                     id(self))
            return
        return self.rpc.getProcesserInfo()

    def stop(self):
        log.debug('[handler]player(%s)stop', self.pid)
        self.set_rpc(None)

    def force_close(self):
        """ 服务器强制网关断开连接 """
        self.rpc.force_close()

    def router(self, addr_fnams):
        """
        添加gateway router
        addr_fnames为{"addr":["f1","f2"]}格式
        DFW的方法
        """
        print "---------------->>>>>>>>>>>>>> ,,,,,,,,,,,,,,, Z<<<<<< ", addr_fnams
        if self.rpc:
            self.rpc.router(addr_fnams)

    def add_router(self, routerId, addr):
        """
        向网关注册路由， 路由ID，与地址绑定，(原始方法)
        """
        if self.rpc:
            self.rpc.add_router(routerId, addr)


    def remove_router(self, addr):
        self.rpc.remove_router(addr)

    def connect(self,host, port):
        self.rpc.connect(host, port)