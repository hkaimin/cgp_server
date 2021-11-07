#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# 游戏配置	批次	名字	展示奖励	奖励	描述
# int&key	int	int	string	string	string
# id	cycle	day	show	reward	Exps




class SevenDayRewardData(object):
    RES_TABLE = "sevenDayReward"

    def __init__(self):
        self.id         = "" # id
        self.cycle      = 1 #批次
        self.day        = 1 #名字
        self.show       = "" #展示奖励
        self.reward     = "" #奖励
        self.Exps       = "" #描述

    def load_from_json(self, data):
        self.id = data.get("id", "")
        self.cycle = data.get("cycle", 1)
        self.day = data.get("day", 1)
        self.show = data.get("show", "")
        self.reward = data.get("reward", "")
        self.Exps = data.get("Exps", "")

    def getShow(self):
        return eval(self.show)

    def getReward(self):
        return eval(self.reward)




