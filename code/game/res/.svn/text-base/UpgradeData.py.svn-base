#!/usr/bin/env python
# -*- coding:utf-8 -*-



# 道具表	经验	速度	泡泡威力	泡泡数量	生命	幸运值
# int&key	int	int	int	int	int	int
# id	exp	speed	power	count	life	luck


class ResUpgradeData(object):
    RES_TABLE = "UpgradeData"

    def __init__(self):
        self.id     = 0 # id
        self.exp    = 0 #经验
        self.speed  = 0 #速度
        self.power  = 0 #泡泡威力
        self.count  = 0 #泡泡数量
        self.life   = 0 #生命
        self.luck   = 0 #幸运值（随机道具掉好东西的增强概率）
        self.reward = 0 #奖励
        self.rewardNum = 0 #数量

    def load_from_json(self, data):
        self.id = data.get("id", 0)
        self.exp = data.get("exp", 0)
        self.speed = data.get("speed", 0)
        self.power = data.get("power", 0)
        self.count = data.get("count", 0)
        self.life = data.get("life", 0)
        self.luck = data.get("luck", 0)
        self.reward = data.get("reward", 0)
        self.rewardNum = data.get("rewardNum", 0)

    def getRewardItemNo(self):
        return self.reward

    def getRewardNum(self):
        return self.rewardNum





