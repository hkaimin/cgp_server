#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 地图砖块表	名称	类型	所属地图批次（大类型）	资源名称
# int&key	string	int	int	string
# id	name	Type	mapType	res
# 1	地表01	1	1	res_1




class ResRoleData(object):
    RES_TABLE = "role"

    def __init__(self):
        self.id = 0         # 角色id
        self.name = ''      # 名称
        self.desc = ""      # 角色描述
        self.pvp_life = 1   # PVP_生命
        self.pvp_speed = 1  # PVP速度
        self.pvp_power = 1  # PVP威力
        self.pvp_cnt = 1    # PVP数量
        #
        self.pve_cnt = 1    # PVE_生命
        self.pve_cnt = 1    # PVE速度
        self.pve_cnt = 1    # PVE威力
        self.pve_cnt = 1    # PVE数量
        self.ex_property = "" # 额外属性
        self.isonline = 0   # 是否上线
        self.price = 0      # 售价
        self.payType = 0    # 支付类型 0,自动赠送 1，金币购买 2，钻石购买
        self.smallHead = "" # 小头像
        self.bgHead = ""    # 角色背景
        self.aminRes = ""   # 角色展示动画


    def load_from_json(self, data):
        self.id             = data.get("id", 0)
        self.name           = data.get("name", "")
        self.desc           = data.get("desc", "")
        self.pvp_life       = data.get("pvp_life", 1)
        self.pvp_speed      = data.get("pvp_speed", 1)
        self.pvp_power      = data.get("pvp_power", 1)
        self.pvp_cnt        = data.get("pvp_cnt", 1)
        self.pve_life       = data.get("pve_life", 1)
        self.pve_speed      = data.get("pve_speed", 1)
        self.pve_power      = data.get("pve_power", 1)
        self.pve_cnt        = data.get("pve_cnt", 1)
        self.isonline       = data.get("isonline", 0)
        self.price          = data.get("price", 0)
        self.payType        = data.get("payType", 0)
        self.smallHead      = data.get("smallHead", "")
        self.bgHead         = data.get("bgHead", "")
        self.aminRes        = data.get("aminRes", "")

    # 获取额外属性
    def getExProperty(self):
        try:
            data = eval(self.ex_property)
            return data
        except:
            print "getExProperty Error"

    # 获取PVP属性
    def getPvpProperty(self):
        init_dict = {}
        init_dict["iClass"] = self.id  # 多少条命
        init_dict["life"] = self.pvp_life  # 多少条命
        init_dict["speed"] = self.pvp_speed  # 速率
        init_dict["power"] = self.pvp_power  # 威力
        init_dict["paopaocount"] = self.pvp_cnt  # 范围
        return init_dict

    # 获取PVE属性
    def getPveProperty(self):
        init_dict = {}
        init_dict["iClass"] = self.id
        init_dict["life"] = self.pve_life  # 多少条命
        init_dict["speed"] = self.pve_speed  # 速率
        init_dict["power"] = self.pve_power  # 威力
        init_dict["paopaocount"] = self.pve_cnt  # 范围
        return init_dict
