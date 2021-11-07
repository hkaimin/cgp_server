#!/usr/bin/env python
# -*- coding:utf-8 -*-

from game.define.store_define import TN_P_MAIL
from store.store import StoreObj

from game import Game

class ModelMail(StoreObj):
    """全局邮件数据"""
    TABLE_NAME = TN_P_MAIL

    def init(self):
        self.id = ''          # self.serverid 设计为不同服，不同的邮件表
        self.mailDict = {}    # 邮件对象{rid:{mid1,{data1}, mid2:{data2}, ...}}
        self.mailTranceNo = 0 #用于生成邮件唯一id的自增值

    def to_save_dict(self, copy=False, forced=False):
        #todo:针对各个模块做cache，避免每次都全量打包，提高性能
        print ">>>>>>>>>>>>>>>mail to_save_dict"
        save = {}
        save['id'] = self.id
        save['mailTranceNo'] = self.mailTranceNo
        save['mailDict'] = self.mailDict
        return save

    def GenerateMailTranceNo(self):
        self.mailTranceNo += 1
        self.modify()
        return self.mailTranceNo

    #overwrite
    def save(self, store, forced=False):
        print ">>>>>>>>>>>>>>>tree mail"
        StoreObj.save(self, store, forced=forced)

    def Set(self, key, value):
        setattr(self, key, value)
        self.modify()

    def Query(self, key, default=None):
        return getattr(self, key, default)
