#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 地图砖块表	名称	类型	所属地图批次（大类型）	资源名称
# int&key	string	int	int	string
# id	name	Type	mapType	res
# 1	地表01	1	1	res_1




class ResMapBase(object):
    RES_TABLE = "MapBase"

    def __init__(self):
        self.id = 0 # id
        self.name = '' #名称
        self.itype = 0 #砖块类型
        self.itheme = 0 #主题类型
        self.mapType = 0 #所属地图批次（大类型）
        self.res = '' #资源名称
        self.themeName = '' #主题名字

    def load_from_json(self, data):
        self.id = data.get("id", 0)
        self.name = data.get("name", "")
        self.itype = data.get("Type", 0)
        self.itheme = data.get("Theme", 0)
        self.mapType = data.get("mapType", 0)
        self.res = data.get("res", "")
        self.themeName = data.get("ThemeName", "")

    # 是否可以炸掉
    def canBreak(self):
        if self.itype == 3:
            return True
        else:
            return False

