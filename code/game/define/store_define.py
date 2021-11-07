#!/usr/bin/env python
# -*- coding:utf-8 -*-
from store.driver import *

#====================   游戏数据库定义 ===============================
#类名定义
TN_P_PLAYER = 'player'
TN_P_TREE = 'tree'
TN_P_MAIL = 'mail'
TN_S_SINGLETON = 'singleton'
TN_S_ITEM= 'item'

#类与表名关系 (tablename, key, indexs, autoInc)
GAME_MONGO_CLS_INFOS = {
    TN_P_PLAYER: (TN_P_PLAYER, 'id', [('account',{'unique':True})], True),
    TN_P_TREE: (TN_P_TREE, 'id', [('serverid',{'unique':True})], False),
    TN_P_MAIL: (TN_P_MAIL, 'id', [('id', {'unique': True})], False),
    TN_S_SINGLETON: (TN_S_SINGLETON, 'id', [], False),
}

GAME_CLS_INFOS = {
    MONGODB_ID: GAME_MONGO_CLS_INFOS,
}
#====================   游戏数据库定义 end ===============================


#====================   资源数据库定义 ===============================
RES_MONGO_CLS_INFOS = {

}

RES_CLS_INFOS = {
    MONGODB_ID: RES_MONGO_CLS_INFOS,
}
#====================   游戏数据库定义  end===============================

#gconfig key 列表
GF_ACCESS_IP = 'access_ip' #admin access ip re



#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


