#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 小游戏加成表	点击次数	增加类型	增加参数	描述
# int&key	int	int	int	string
# id	hitcount	type	param	desc



class ResMiniGameData(object):
    RES_TABLE = "MiniGameData"

    def __init__(self):
        self.ID             = 0 # id
        self.finishType     = 1 # 完成类型
        self.hitcount       = 0 # 达成条件的点击次数
        self.itype           = 0 # 类型
        self.param          = 0 # 参数
        self.desc           = "" # 描述

    def load_from_json(self, data):
        self.ID         = data.get("id", 0)
        self.finishType = data.get("finishType", 0)
        self.hitcount   = data.get("hitcount", 0)
        self.itype       = data.get("type", 0)
        self.param      = data.get("param", 0)
        self.desc       = data.get("desc", "")




