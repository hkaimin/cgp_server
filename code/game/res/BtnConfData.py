#!/usr/bin/env python
# -*- coding:utf-8 -*-


# 按钮配置	名字	位置（1为右边，2为下面）	是否开启
# string&key	string	int	int
# id	name	pos	isOpen




class BtnConfData(object):
    RES_TABLE = "btnConf"

    def __init__(self):
        self.id        = "" # id
        self.name      = "" #名字
        self.pos       = 0 #位置（1为右边，2为下面）
        self.isOpen    = 0 #是否开启
        self.weight    = 0 #排序权重


    def load_from_json(self, data):
        self.id         = data.get("id", 0)
        self.name       = data.get("name", "")      #名字
        self.pos        = data.get("pos", 1)       #位置（1为右边，2为下面）
        self.isOpen     = data.get("isOpen", 0)    #是否开启
        self.weight     = data.get("weight", 0)    #是否开启




