#!/usr/bin/env python
# -*- coding:utf-8 -*-

from game.common import utility
from game.define import constant
from game import Game
from game.models.treeMap import ModelTreeMap
from corelib import spawn, log
from gevent import sleep
from corelib.frame import MSG_FRAME_STOP

''' 邀请码映射模块 '''
class TreemapMgr(utility.DirtyFlag):
    DATA_CLS = ModelTreeMap

    def __init__(self):
        utility.DirtyFlag.__init__(self)

        self.treeMap = {}  # {code:fakecode}
        self.data = None
        self.save_cache = {}

        self._save_loop_task = None
        Game.sub(MSG_FRAME_STOP, self._frame_stop)



    def markDirty(self):
        utility.DirtyFlag.markDirty(self)
        self.data.modify()

    def start(self):
        self.data = self.DATA_CLS.load(Game.store, self.DATA_CLS.TABLE_KEY)
        if not self.data:
            self.data = self.DATA_CLS()
        else:
            self.load_from_dict(self.data.dataDict)
        print "treemapMgr start ======================"
        self.data.set_owner(self)

        self._save_loop_task = spawn(self._saveLoop)

    def _frame_stop(self):
        if self._save_loop_task:
            self._save_loop_task.kill(block=False)
            self._save_loop_task = None

        self.save(forced=True, no_let=True)

    def _saveLoop(self):
        stime = 10 * 60
        while True:
            sleep(stime)
            try:
                self.save()
            except:
                log.log_except()

    def save(self, forced=False, no_let=False):
        self.data.save(Game.store, forced=forced, no_let=no_let)

    def load_from_dict(self, data):
        self.treeMap = data.get("treeMap", {})

    def to_save_dict(self, forced=False):
        if self.isDirty() or forced or not self.save_cache:
            self.save_cache = {}
            self.save_cache["treeMap"] = self.treeMap
        return self.save_cache


    # 是否已存在
    def isExist(self, fakecode):
        lfakecode = self.treeMap.values()
        if fakecode in lfakecode:
            return True
        else:
            return False

    # 设置提供映射邀请码
    def setFakecode(self, code, fakecode):
        if self.isExist(fakecode):
            return 0 # 已存在
        self.treeMap[code] = fakecode
        self.markDirty()
        return fakecode

    # 获取映射邀请码
    def getFakecode(self, code):
        if not self.treeMap.has_key(code):
            self.setFakecode(code,code)
            return code
        else:
            fakecode = self.treeMap.get(code)
            return fakecode

    # 获取原邀请码
    def getCodeByFakecode(self, fakecode):
        for code, fcode in self.treeMap.iteritems():
            if fcode == fakecode:
                return code
        return 0
