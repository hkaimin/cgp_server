#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 地图	类型	底图配置	障碍物
# int&key	int	arrayint1	arrayint1
# id	Type	bgconf	layerconf
# 1	1	1_1_1_1_1_1_1_1_3_1_2_1_1_1_1_1_1_1_1_1_1_1_3_1_1_1_1_1_2_1_1_3_1_1_1_1_1_1_1_1_1_1_1_1_1_1_1_1_2_1_1_3_1_1_1_1_1_1_1_1_1_1_1	0_10_0_0_0_0_4_8_0_0_10_4_0_7_0_4_8_0_0_10_4_0_0_0_4_8_0_0_10_4_0_0_5_4_17_0_0_4_4_18_5_5_5_17_0_0_0_7_18_18_18_17_17_0_5_0_7_0_0_0_0_0_6

# 速度道具数量	泡泡数量道具	泡泡威力道具	增加生命道具	刺穿泡泡道具	防护罩道具	总游戏时常	ai数量
# int	int	int	int	int	int	int	int
# itemSpeed	itemNum	itemPower	itemLife	itemDestory	itemDef	barrTime	aiNum
# 2	2	2	0	0	0	600	0




class ResMapConf(object):
    RES_TABLE = "MapConf"

    def __init__(self):
        self.id = 0 # id
        self.Type = 0 #名称
        self.bgconf = []
        self.layerconf = []
        self.itemSpeed = 0 # 速度道具数量
        self.itemNum = 0 # 泡泡数量道具
        self.itemPower = 0 # 泡泡威力道具
        self.itemLife = 0 # 增加生命道具
        self.itemDestory = 0 # 刺穿泡泡道具
        self.itemDef = 0 # 防护罩道具
        self.barrTime = 0 # 总游戏时常
        self.aiNum = 0 # ai数量
        self.itemSpeedPer = 0  # 速度道具数量概率
        self.itemNumPer = 0  # 泡泡数量道具概率
        self.itemPowerPer = 0  # 泡泡威力道具概率
        self.itemLifePer = 0  # 增加生命道具概率
        self.lGuanKaDoorIdx = []

    def load_from_json(self, data):
        self.id = data.get("id", 0)
        self.Type = data.get("Type", 0)
        self.bgconf = data.get("bgconf", [])
        self.layerconf = data.get("layerconf", [])
        self.itemSpeed = data.get("itemSpeed", 0)
        self.itemNum = data.get("itemNum", 0)
        self.itemPower = data.get("itemPower", 0)
        self.itemLife = data.get("itemLife", 0)
        self.itemDestory = data.get("itemDestory", 0)
        self.itemDef = data.get("itemDef", 0)
        self.barrTime = data.get("barrTime", 0)
        self.aiNum = data.get("aiNum", 0)
        self.itemSpeedPer   = data.get("itemSpeedPer", 0) # 速度道具数量概率
        self.itemNumPer     = data.get("itemNumPer", 0) # 泡泡数量道具概率
        self.itemPowerPer   = data.get("itemPowerPer", 0) # 泡泡威力道具概率
        self.itemLifePer    = data.get("itemLifePer", 0)# 增加生命道具概率

