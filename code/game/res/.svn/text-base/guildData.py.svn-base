#!/usr/bin/env python
# -*- coding:utf-8 -*-


# 新手引导	引导KEY	步骤	类型	界面引导按钮编号	子界面引导编号	备注	触发
# int&key	int	int	int	int	int	string	int
# id	ikey	istep	itype	btnkey	innerIndex	desc	isFight
#



class GuildData(object):
    RES_TABLE = "guildData"

    def __init__(self):
        self.id             = "" # id
        self.ikey           = "" #引导KEY
        self.istep          = 0 #步骤
        self.itype          = 0 #类型
        self.btnkey         = 0 #界面引导按钮编号
        self.innerIndex     = 0 #子界面引导编号
        self.desc           = 0 #备注
        self.isFight        = 0 #触发


    def load_from_json(self, data):
        self.id             = data.get("id", "") # id
        self.ikey           = data.get("ikey", 0) #引导KEY
        self.istep          = data.get("istep", 0) #步骤
        self.itype          = data.get("itype", 0) #类型
        self.btnkey         = data.get("btnkey", 0) #界面引导按钮编号
        self.innerIndex     = data.get("innerIndex", 0) #子界面引导编号
        self.desc           = data.get("desc", "") #备注
        self.isFight        = data.get("isFight", 0) #触发




