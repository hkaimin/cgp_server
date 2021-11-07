#!/usr/bin/env python
# -*- coding:utf-8 -*-


# 游戏配置	名字
# string&key	string	string
# id	Value	Exps



class GameConfData(object):
    RES_TABLE = "gameConf"

    def __init__(self):
        self.id         = "" # id
        self.Value      = None #内容
        self.Exps       = "" #描述


    def load_from_json(self, data):
        self.id = data.get("id", "")
        self.Value = data.get("Value", "")
        self.Exps = data.get("Exps", "")


    def GetValue(self):
        return eval(self.Value)

