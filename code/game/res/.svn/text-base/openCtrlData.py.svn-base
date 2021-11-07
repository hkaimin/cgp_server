#!/usr/bin/env python
# -*- coding:utf-8 -*-


# 按钮配置	名字	位置（1为右边，2为下面）	是否开启
# string&key	string	int	int
# id	name	pos	isOpen




class OpenCtrlData(object):
    RES_TABLE = "openCtrl"
    def __init__(self):
        self.id        = 0 # id
        self.name      = "" #名字
        self.isOpen    = 0 #是否开启
        self.openLv    = 0 #排序权重

    def load_from_json(self, data):
        self.id         = data.get("id", 0)
        self.name       = data.get("name", "")      #名字
        self.isOpen     = data.get("isOpen", 0)    #是否开启
        self.openLv     = data.get("openLv", 0)    #开放等级

    def Save(self):
        dData = {
            "id": self.id,
            "name":self.name,
            "isOpen":self.isOpen,
            "openLv":self.openLv,
        }
        return dData
