#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 地图砖块表	名称	类型	所属地图批次（大类型）	资源名称
# int&key	string	int	int	string
# id	name	Type	mapType	res
# 1	地表01	1	1	res_1




class ResItemData(object):
    RES_TABLE = "ItemData"

    def __init__(self):
        self.id = 0         # id
        self.name = ''      # 称
        self.itype = 0       # 物品类型
        self.res = ''       # 源名称
        self.maxAmount = 0  # 叠加数量
        self.desc = ""      # 描述
        self.spType = 0     # 功能类型1 = 增加生命, 2 = 增加速度, 3 = 增加泡泡数量, 4 = 增加泡泡威力
        self.param1 = 0     # 功能参数1（物品类型1：增加次数）
        self.param2 = 0     # 功能参数2（物品类型2：持续场数）
        self.param3 = ""     # 功能参数3（礼包）
        self.cycle = 0      # 持续周期 0:没限制，1:持续1一天，2持续一周

    def load_from_json(self, data):
        self.id         = data.get("id", 0)
        self.name       = data.get("name", "")
        self.itype       = data.get("Type", 0)
        self.res        = data.get("res", "")
        self.maxAmount  = data.get("maxAmount", 99)
        self.desc       = data.get("desc", "")
        self.spType     = data.get("spType", 0)
        self.param1     = data.get("param1", 0)
        self.param2     = data.get("param2", 0)
        self.param3     = data.get("param3", "")
        self.cycle      = data.get("cycle", 0)

    # 获取礼包数据
    def getGiftData(self):
        data = eval(self.param3)
        return data

