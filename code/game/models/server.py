#!/usr/bin/env python
# -*- coding:utf-8 -*-
from game.define.store_define import TN_S_SINGLETON

from store.store import StoreObj

from game import Game
import weakref

class ModelServer(StoreObj):
    """服务器数据"""
    TABLE_NAME = TN_S_SINGLETON
    TABLE_KEY = "serverInfo"

    def set_owner(self, owner):
        self.owner = weakref.proxy(owner)

    def init(self):
        self.id = self.TABLE_KEY #键
        self.dataDict = {} #数据

    def to_save_dict(self, copy=False, forced=False):
        save = {}
        save['id'] = self.id
        save['dataDict'] = self.owner.to_save_dict(forced=forced)
        # print 44444444444444,save
        return save