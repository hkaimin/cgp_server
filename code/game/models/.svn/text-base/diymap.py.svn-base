#!/usr/bin/env python
# -*- coding:utf-8 -*-
from game.define.store_define import TN_S_SINGLETON

from store.store import StoreObj

from game import Game
import weakref

class ModelDiyMap(StoreObj):
    """排行榜数据"""
    TABLE_NAME = TN_S_SINGLETON
    TABLE_KEY = "diymap"

    def set_owner(self, owner):
        self.owner = weakref.proxy(owner)

    def init(self):
        self.id = self.TABLE_KEY #键
        self.dataDict = {} #数据

    def to_save_dict(self, copy=False, forced=False):
        save = {}
        save['id'] = self.id
        save['dataDict'] = self.owner.to_save_dict(forced=forced)
        # print 5555555555,save
        return save