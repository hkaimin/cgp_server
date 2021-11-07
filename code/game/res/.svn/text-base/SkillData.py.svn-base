#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 技能	等级	是否能开放	升级付费类型	花费	效果持续时间	类型	数值	数值2	技能CD	名字
# string&key	string	int	int	int	float	int	int	int	int	string
# id	lv	isOpen	costType	cost	effectTime	skillType	param	param2	cd	name



class ResSkillData(object):
    RES_TABLE = "skillConf"

    def __init__(self):
        self.id             = 0     # 表自增id
        self.skillID        = 0     # 技能ID
        self.lv             = 0     # 等级
        self.isOpen         = 0     # 是否能开放
        self.costType       = 0     # 升级付费类型
        self.cost           = 0     # 花费
        self.effectTime     = 0     # 效果持续时间
        self.skillType      = 0     # 类型
        self.param          = 0     # 数值
        self.param2         = 0     # 数值2
        self.cd             = 0     # 技能CD
        self.name           = ""    # 名字

    def load_from_json(self, data):
        self.id             = data.get("id", 0)
        self.skillID        = data.get("skillID", 0)
        self.lv             = data.get("lv", 0)
        self.isOpen         = data.get("isOpen", 0)
        self.costType       = data.get("costType", "")
        self.cost           = data.get("cost", 0)
        self.effectTime     = data.get("effectTime", 0)
        self.skillType      = data.get("skillType", 0)
        self.param          = data.get("param", 0)
        self.param2         = data.get("param2", 0)
        self.cd             = data.get("cd", 0)
        self.name           = data.get("name", "")


