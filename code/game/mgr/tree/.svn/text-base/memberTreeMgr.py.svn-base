#!/usr/bin/env python
# -*- coding:utf-8 -*-
# import os
import time

import config
# from game.define import log_define
from corelib import spawn
from corelib.gtime import current_time
from gevent import sleep

from game import Game
from game.common import utility
from game.core.membTree import membTree
from game.core.player import Player
from game.mgr.tree.TreemapMgr import TreemapMgr


# NOTE： 进程退出的时候还需要再存一次

class MembTreeServer(object):
    """ 游戏记录类 """
    _rpc_name_ = 'rpc_membtree_svr'
    #定时保存时间 6分钟 # 和角色数据存盘时间错开
    _SAVE_TIME_ = 60
    def __init__(self):
        self.memTree = None  # 关系树
        self.TreeMapMgr = None # {code, fakecode}
        self._loop_task = None
        self.stoping = False

    def start(self):
        # print "------------- tree start"
        self._loop_task = spawn(self._loop)
        self.TreeMapMgr = TreemapMgr()
        self.TreeMapMgr.start()
        pass

    def stop(self):
        """ 进程退出 """
        if self.stoping:
            return
        self.stoping = True
        # 退出前树进行强制保存，以防数据丢失
        self.save_tree()
        if self._loop_task:
            self._loop_task.kill(block=False)
            self._loop_task = None

    def _loop(self):
        """ 定时保存等处理 """
        stime = 10
        while 1:
            sleep(stime)
            # try:
            self.save_tree(True)
            # except:
            #     print "save tree exception2"

    def save_tree(self, isLoopTask=False):
        tree = self.memTree
        if tree:
            if tree.save_time + self._SAVE_TIME_ <= time.time():
                tree.save()
                if isLoopTask:
                    sleep(0.01)
            # try:
            #     if tree.save_time + self._SAVE_TIME_ <= time.time():
            #         tree.save()
            #         if isLoopTask:
            #             sleep(0.01)
            # except:
            #     print "save tree exception1",tree


    # 所有进程都启动后，再从库里初始化树
    def after_all_start(self):
        # 从数据库初始化树 -

        self.check_has_tree()
        self.memTree = membTree.load_tree(config.serverNo)  # 每个区号对应一棵树
        # lRootPlayer = Game.store.query_loads(Player.DATA_CLS.TABLE_NAME, dict(account=config.root_player_account, password=config.root_player_password))
        if self.memTree:
            self.memTree.init()
        print "------------ after_start tree"
        # print self.memTree.treeObj.show()
        pass

    # 检测数据库中是否有树和根玩家（管理员）
    def check_has_tree(self):
        # mongo返回的是[dict,]
        lTreeData = Game.store.query_loads("tree", dict(serverid=config.serverNo))
        print "------------lTreeData",lTreeData
        lRootPlayer = Game.store.query_loads(Player.DATA_CLS.TABLE_NAME, dict(account=config.root_player_account, password=config.root_player_password))
        if len(lTreeData) == 0: # 数据库中没有树对象，则创建根节点，预留
            if len(lRootPlayer) == 0:
                self.make_root_player()  # 创建根玩家
            self.make_tree()
            pass
        pass

    # 创建对应服务器唯一的根管理玩家
    def make_root_player(self):
        data = dict(account=config.root_player_account, password=config.root_player_password, newTime=current_time())
        try:
            Game.store.insert(Player.DATA_CLS.TABLE_NAME, data)
        except:
            return 0, errcode.EC_NAME_REPEAT
        pass

    # 数据库中没有树，创建树
    def make_tree(self):
        lData = Game.store.query_loads(Player.DATA_CLS.TABLE_NAME, dict(account=config.root_player_account))
        dRootPlaye = lData[0]
        rid = dRootPlaye['id']
        RootCode = utility.activation_code(rid)
        Game.store.update(Player.DATA_CLS.TABLE_NAME, rid, dict(code=RootCode))
        membTree = {RootCode: {u'data': {'lnum': 0, 'rid': rid, 'canMail': 1}}} # 根节点数据结构
        Game.store.insert("tree", {"id": config.serverNo, "serverid": config.serverNo, "membTree": membTree})


    def init(self):
        # print "------------ tree init"
        pass

    # 账号创建的时候调用
    def rc_creatTreebyAdd(self, code, rid, pcode):
        self.memTree.creatTreebyAdd(code, rid, pcode)
        fcode = self.setFakecode(code, code)
        return fcode

    def rc_check_mail_uid(self, code):
        return self.memTree.check_mail_uid(code)

    # 获取所有子节点
    def rc_getAllChildren(self, code):
        return self.memTree.getAllChildren(code)

    def rc_getCode(self, rid):
        return self.memTree.getCode(rid)

    # 检测节点合法性
    def rc_IsHasCode(self, code):
        return self.memTree.IsHasCode(code)

    def rc_setCanMail(self, rid, canmail):
        print "--------------rc_setCanMail", rid, canmail
        return self.memTree.setCanMail(rid, canmail)

    def rc_getCanMail(self, rid):
        return self.memTree.getCanMail(rid)

    # 是否有存是否代理
    def checkIsAgent(self, code, isAgent):
        print dir(self.memTree)
        isAgent = self.memTree.QueryDataByCode(code, "isAgent", 0)
        print "tree---------------isAgent", isAgent
        if not isAgent:
            self.memTree.SetDataByCode(code, "isAgent", 1)
            self.memTree.save(forced=True)

    # 获取有代理权限的上家
    def getAgentParents(self, code):
        # 从小到多大，倒序
        lAgent = []
        l = self.memTree.getAllParents(code)
        for pcode in l:
            parent = self.memTree.get_node(pcode)
            if not parent:continue
            if parent.data.get('isAgent'):
                rid = parent.data.get('rid', 0)
                if not rid: continue
                linfo = [rid, pcode]
                lAgent.append(linfo)
        # lAgent = lAgent.reverse()

        return lAgent


    # 根据parent code获取rid
    def getparRidByCode(self, code):
        return self.memTree.getparRidByCode(code)

    # 根据 code获取rid
    def getRidByCode(self, code):
        return self.memTree.getRidByCode(code)


    #=======TreeMapMgr=======
    # 设置邀请码映射
    def setFakecode(self, code, fakecode):
        fcode = self.TreeMapMgr.setFakecode(code, fakecode)
        return fcode

    # 获得映射邀请码
    def getFakecode(self, code):
        fakecode = self.TreeMapMgr.getFakecode(code)
        return fakecode

    # 获取原邀请码
    def getCodeByFakecode(self, fakecode):
        code = self.TreeMapMgr.getCodeByFakecode(fakecode)
        return code

    # 获取所有父节点
    def getAllParents(self, code):
        temp_list = self.TreeMapMgr.getAllParents(code)
        return temp_list
    #=======TreeMapMgr=======



    # # 玩之后的结果
    # def platform_mode_result(self, code):
    #     temp_list = self.TreeMapMgr.getAllParents(code)
    #     
    #     pass

def new_game_tree():
    MembTree = MembTreeServer()
    MembTree.init()
    return MembTree





#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
from game.mgr.player import *