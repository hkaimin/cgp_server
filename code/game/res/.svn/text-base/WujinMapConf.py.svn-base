#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 无尽关卡	第几层关卡	底图配置	障碍物	ai等级	速度道具数量	泡泡数量道具	泡泡威力道具	增加生命道具	刺穿泡泡道具	防护罩道具	总游戏时常
# int&key	int	arrayint1	arrayint1	int	int	int	int	int	int	int	int
# id	diffLevel	bgconf	layerconf	aiLevel	itemSpeed	itemNum	itemPower	itemLife	itemDestory	itemDef	barrTime

class WujinMapConf(object):
    RES_TABLE = "WujinMapConf"

    def __init__(self):
        self.id             = 0 # id
        self.diffLevel      = 0
        self.bgconf         = []
        self.layerconf      = []
        self.aiLevel        = 0 # AI等级
        self.itemSpeed      = 0 # 速度道具数量
        self.itemNum        = 0 # 泡泡数量道具
        self.itemPower      = 0 # 泡泡威力道具
        self.itemLife       = 0 # 增加生命道具
        self.itemDestory    = 0 # 刺穿泡泡道具
        self.itemDef        = 0 # 防护罩道具
        self.barrTime       = 0 # 总游戏时常
        self.itype          = 0 # 通关条件类型 1:时间
        self.condition      = "" # 通关条件
        self.aiLift         = 0 #AI生命值
        self.aiSpeed        = 0 #AI速度
        self.aiPaoNum       = 0 #AI泡泡NUM
        self.aiPower        = 0 #AI泡泡威力
        self.aiClass        = 1 #AI职业
        self.itemSpeedPer   = 0 # 速度道具数量概率
        self.itemNumPer     = 0 # 泡泡数量道具概率
        self.itemPowerPer   = 0 # 泡泡威力道具概率
        self.itemLifePer    = 0 # 增加生命道具概率
        self.lGuanKaDoorIdx = [] # 关卡门IDX
        self.lMonsterArea = [] # 新怪物行走区域

    def load_from_json(self, data):
        self.id             = data.get("id", 0)
        self.diffLevel      = data.get("diffLevel", 0) # 难度等级
        self.bgconf         = data.get("bgconf", [])
        self.layerconf      = data.get("layerconf", [])
        self.aiLevel        = data.get("aiLevel", 0) # AI等级
        self.itemSpeed      = data.get("itemSpeed", 0)
        self.itemNum        = data.get("itemNum", 0)
        self.itemPower      = data.get("itemPower", 0)
        self.itemLife       = data.get("itemLife", 0)
        self.itemDestory    = data.get("itemDestory", 0)
        self.itemDef        = data.get("itemDef", 0)
        self.barrTime       = data.get("barrTime", 0)
        self.itype          = data.get("itype", 0)
        self.condition      = data.get("condition", "")
        self.aiLife         = data.get("aiLife", 1) #AI生命值
        self.aiSpeed        = data.get("aiSpeed", 1) #AI速度
        self.aiPaoNum       = data.get("aiPaoNum", 1) #AI泡泡NUM
        self.aiPower        = data.get("aiPower", 1) #AI泡泡威力
        self.aiClass        = data.get("aiClass", 1) #AI职业
        self.itemSpeedPer   = data.get("itemSpeedPer", 0) # 速度道具数量概率
        self.itemNumPer     = data.get("itemNumPer", 0) # 泡泡数量道具概率
        self.itemPowerPer   = data.get("itemPowerPer", 0) # 泡泡威力道具概率
        self.itemLifePer    = data.get("itemLifePer", 0)# 增加生命道具概率
        self.lGuanKaDoorIdx = data.get("lGuanKaDoorIdx", [])# 关卡门
        self.lMonsterArea = data.get("lMonsterArea", [])# 新怪物行走区域

    # 获取通关条件
    def getPassCondition(self):
        dCondition = {}
        if self.condition:
            dCondition = eval(self.condition)
        # try:
        #     if self.condition:
        #         dCondition = eval(self.condition)
        #         pass
        # except:
        #     pass
        return dCondition


    def getAIAttr(self):
        data = {
            "aiLife":self.aiLife,
            "aiSpeed": self.aiSpeed,
            "aiPaoNum": self.aiPaoNum,
            "aiPower": self.aiPower,
            "aiClass": self.aiClass
        }
        return data