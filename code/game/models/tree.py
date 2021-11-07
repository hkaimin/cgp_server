#!/usr/bin/env python
# -*- coding:utf-8 -*-

from game.define.store_define import TN_P_TREE
from store.store import StoreObj

from game import Game

class ModelTree(StoreObj):
    """全局树数据"""
    TABLE_NAME = TN_P_TREE

    def init(self):
        self.id = ''          # self.serverid
        self.serverid = ''    # 树的id，每一个服对应一棵
        self.membTree = {}    # 成员树
        self.deep = 0         # 树深度
        self.root = ""        # 根节点


    def to_save_dict(self, copy=False, forced=False):
        #todo:针对各个模块做cache，避免每次都全量打包，提高性能
        print ">>>>>>>>>>>>>>>tree to_save_dict"
        save = {}
        save['id']       = self.id
        save['serverid'] = self.serverid
        save['membTree'] = self.membTree
        save['deep'] = self.deep
        save['root'] = self.root
        return save

    #overwrite
    def save(self, store, forced=False):
        # print ">>>>>>>>>>>>>>>tree save"
        StoreObj.save(self,store, forced=forced)


    def Set(self, key, value):
        setattr(self, key, value)
        self.modify()

    def Query(self, key, default=None):
        return getattr(self, key, default)
