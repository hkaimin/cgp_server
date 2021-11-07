#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 名字库	名字
# int&key	string
# id	name


class HelpData(object):
    RES_TABLE = "helpConf"

    def __init__(self):
        self.id         = 0 # id
        self.name       = "" # 名字
        self.content    = "" # 内容

    def load_from_json(self, data):
        self.id = data.get("id", 0)
        self.name = data.get("name", "")
        self.content = data.get("content", "")



