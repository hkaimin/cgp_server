#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

from corelib.message import observable
from corelib import spawn_later, log, spawn
from corelib.gtime import current_time
from corelib.treelib import Node, Tree

from game import Game
from game.models.tree import ModelTree

# 全局关系树对象
# {RootCode: {u'data': {'lnum': 0, 'rid': rid, 'canMail': 1}}} # 根节点数据结构
# data = {"parent":parent ,'lnum': 0, 'rid': rid, 'canMail': 0}
@observable
class membTree(object):
    DATA_CLS = ModelTree

    def __init__(self):

        self.loaded = False
        self.data = None #全局树数据模型
        self.save_time = current_time()
        self.treeObj = Tree()
        pass

    def init(self):
        # 还原树对象
        if self.data:
            self.dict_to_tree(self.data.membTree, True)

    def markDirty(self):
        self.data.modify()

    def save(self, forced=False):
        # self.save_time = current_time()
        # log.debug('tree(%s) save', self.save_time)
        # print "----- log save debug"
        if self.data.modified: # 如果数据脏了，树对象重新导出字典
            self.tree_to_dict()
        self.data.save(Game.store, forced=forced)

    def load(self):
        if self.loaded:
            return
        self.loaded = True
        print "----- log load debug", self.data.membTree
        # log.debug('tree(%s) load', self.save_time)

    @classmethod
    def load_tree(cls, serverid):
        """ 根据pid加载Player对象 """
        data = cls.DATA_CLS.load(Game.store, serverid)  # 这里用serverid做ke
        if data is None:
            return
        tree = cls()
        tree.data = data
        tree.load()
        return tree

    # 设置/添加节点data值 Set
    def SetDataByCode(self, code, key, values):
        node = self.get_node(code)
        if not node: return None
        data = node.data
        data[str(key)] = values
        node.data = data
        print "SetDataByCode----:", node.data
        self.markDirty()
        return 1

    # 查询节点data值 Query
    def QueryDataByCode(self, code, key,  default=None):
        node = self.get_node(code)
        if not node: return None
        data = node.data
        print "QueryDataByCode----:",data
        return data.get(key, default)

    # 根据UID设置节点data值
    def SetDataByUID(self, UID, key, values):
        code = self.getCode(UID)
        if not code:return None
        self.SetDataByCode(code, key, values)

    # 根据UID查询节点data值
    def QueryDataByUID(self, UID, key, default=None):
        code = self.getCode(UID)
        if not code:return None
        self.SetDataByCode(code, key, default)
        pass


    # 检测是否存在相同名字的节点
    def check_has_node(self, code):
        return self.treeObj.contains(code)

    # 获取当前code对应节点Object
    def get_node(self, code):
        return self.treeObj.get_node(code)

    # 获取父节点
    def get_parent(self, code):
        pass

    # 获取所有父节点,查找节点所有上级
    def getAllParents(self, code):
        temp_list = []
        print "---------code", code
        def getFunc(code):
            pnode = self.treeObj.parent(code)
            if pnode:
                temp_list.append(pnode.tag)
                getFunc(pnode.tag)
        getFunc(code)
        return temp_list

    # 获取所有子节点，查找所属节点所有下级
    def getAllChildren(self, code):
        temp_list = []
        tree = self.treeObj
        def func(code):
            children = tree.children(code)
            # print "-----", code, tree.level(code)
            lReloop = []
            for node in children:
                temp_list.append(node.tag)
                print node.tag
                if node.data['lnum'] > 0:
                    lReloop.append(node.tag)
            for tag in lReloop:
                func(tag)
        func(code)
        return temp_list

    # 字典转换为树, d = self.data.membTree
    def dict_to_tree(self, d, isInit=False):
        # if isInit: # 如果是初始化
        #     self.treeObj = Tree()
        for k, v in d.items():
            data = v['data']
            children = v.get('children', None)
            if not data.get("parent", None):
                self.creatTreebyMake(self.treeObj, k, data=v['data'])
            else:
                self.creatTreebyMake(self.treeObj, k, data['parent'], v['data'])
            if children:
                for node in children:
                    self.dict_to_tree(node)

    # 树对象转字典
    def tree_to_dict(self):
        print "----tree_to_dict_1"
        dcitTree = None
        if self.treeObj:
            print "--------self.data.root",self.treeObj.root
            dcitTree = self.treeObj.to_dict(self.treeObj.root, with_data=True)
        if dcitTree:
            self.data.membTree = dcitTree
            print "----tree_to_dict"
        self.markDirty()

    # 字典还原树对象时候用
    def creatTreebyMake(self, tre, id, parent=None, data={}):
        # print "tre, id, parent, data",tre, id, parent, data
        tre.create_node(identifier=id, parent=parent, data=data)

    # 动态添加树节点时候用，玩家注册 tre=树对象，id = 玩家自己的code, parent = 父节点code
    def creatTreebyAdd(self, code, rid, parent=None):
        print "Tree --- code, rid, parent", code, rid, parent
        all_nodes = self.treeObj.all_nodes()
        if not parent or parent == '':
            parent = self.treeObj.root
        data = {"parent":parent ,'lnum': 0, 'rid': rid, 'canMail': 0}
        self.treeObj.create_node(identifier=code, parent=parent, data=data)
        pNode = self.get_node(parent)
        pNode.data['lnum'] = pNode.data['lnum'] + 1 # 对应父节点的子节点计数加一 "lnum"+1
        self.markDirty()

    # 冒泡找出有能力发公告的玩家
    def check_mail_uid(self, code):
        print "---------check_mail_uid", code
        parents = self.getAllParents(code)
        rid = 0
        for nid in parents:
            pnode = self.get_node(nid)
            if pnode.data.get('canMail',0) == 1:
                rid = pnode.data.get('rid')
                break
        print "---------check_mail_uid rid:", rid
        return rid

    def getCode(self, rid):
        all_nodes = self.treeObj.all_nodes()
        for node in all_nodes:
            print "---------getCode"
            if node.data.get('rid') == rid:
                print "sssssssssssss node.identifier",node.identifier
                return node.identifier
        return ''

    # 设置邮件权限
    def setCanMail(self, rid, canmail=1):
        code = self.getCode(rid)
        pNode = self.get_node(code)
        pNode.data['canMail'] = canmail
        self.markDirty()
        return pNode.data

    def getCanMail(self, rid):
        code = self.getCode(rid)
        pNode = self.get_node(code)
        return pNode.data['canMail']

    # 检测节点合法性
    def IsHasCode(self,code):
        if self.check_has_node(code):
            return 1
        else:
            return 0

    # 根据code获取parent的rid
    def getparRidByCode(self, code):
        node = self.get_node(code)
        pcode = node.data.get("parent", 0)
        pnode = self.get_node(pcode)
        if pnode:
            rid = pnode.data.get("rid", 0)
            print "-------------------mmmmmmmmmm rid", rid
            return rid
        else:
            return 0

    # 根据code获取rid
    def getRidByCode(self, code):
        node = self.get_node(code)
        if node:
            rid = node.data.get("rid", 0)
            return rid
        else:
            return 0




#---------------------
#---------------------
#---------------------


