#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'
import game.mgr.player
from game.common.utility import *
import game.core.item
from game import Game
import weakref
from game.common.ctn import CPstContainerBase

# Test
class CItemContainer(CPstContainerBase):
    def __init__(self, iOwner, saveKey="", OwnerObj=None):
        CPstContainerBase.__init__(self, iOwner, saveKey, OwnerObj)
        self.dItemNoByUID = {}  # 通过物品对象No找到对象UID
        self.dItemNoByUIDList = {}
        self.OwnerObj = weakref.proxy(OwnerObj)
        self.size = 10
        self.ItemDataRes = Game.res_mgr.res_itemData # 物品表

    def ClearDirtyFlag(self):  # override
        super(CItemContainer, self).ClearDirtyFlag()

    def OnBorn(self):
        pass

    def GetRefreshItemList(self):
        return []

    def AddItem(self, obj, isMarkDirty=True):
        CPstContainerBase.AddItem(self, obj, isMarkDirty)
        print "-----AddItem--------obj.No():", obj.No()
        self.dItemNoByUID[obj.No()] = obj.UID()
        if not self.dItemNoByUIDList.has_key(obj.No()):
            self.dItemNoByUIDList[obj.No()] = [obj.UID()]
        else:
            self.dItemNoByUIDList[obj.No()].append(obj.UID())

    def RemoveItem(self, obj, bSend=True, bRefresh=True):
        if self.dItemNoByUID.has_key(obj.No()):
            del self.dItemNoByUID[obj.No()]
        if self.dItemNoByUIDList.has_key(obj.No()):
            if obj.UID() in self.dItemNoByUIDList[obj.No()]:
                self.dItemNoByUIDList[obj.No()].remove(obj.UID())
        CPstContainerBase.RemoveItem(self, obj, bSend)

    # override
    def Load(self, dData):
        print '========ITEM======Load====================', dData
        if dData == None:
            dData = {}
        super(CItemContainer, self).Load(dData.get("Sp", {}))
        self.size = dData.get("size", 10)

    # override,加载宠物数据
    def LoadItem(self, iIndex, data):
        if type(data) == types.ListType:
            iNo, dData = data
        else:
            iNo, dData = data, {}
        return game.core.item.Load(iNo, dData, self.OwnerObj) #这里接的是item的load

    # override
    def Save(self, forced=False):
        if self.isDirty() or forced:
            dData = {}
            dSuper = super(CItemContainer, self).Save(forced)
            if dSuper:
                dData["Sp"] = dSuper
            dData["size"] = self.size
            return dData

    def SaveItem(self, iIndex, obj, bTransfer=False):  # override
        if bTransfer:
            dData = obj.SaveEx()
        else:
            dData = obj.Save()
        if dData:
            return (obj.No(), dData)
        return obj.No()

    def CleanAllItems(self):
        self.dData = {}
        self.dKeyMapItem = {}
        self.MarkDirty()
        self.OwnerObj.save(forced=True)

    def GetItemIdByNo(self, iItemNo):
        return self.dItemNoByUID.get(iItemNo, 0)

    def GetItemByNo(self, iItemNo):
        print "self.dItemNoByUID:",self.dItemNoByUID
        iItemUid = self.dItemNoByUID.get(int(iItemNo), 0)
        # print "------------iItemUid-",iItemUid
        if iItemUid:
            return self.GetItem(iItemUid)
        return None

    def MarkDirty(self):
        super(CItemContainer, self).MarkDirty()
        pass

    def getItemNum(self, iNo):
        print "------------self.dKeyMapItem:",self.dKeyMapItem
        num = 0
        for iUID, obj in self.dKeyMapItem.iteritems():
            print obj.No(), obj.iNum
            if iNo == obj.No():
                num += obj.Num()
        return num

    # 检测物品是否可叠加
    def getItemCanAdd(self, iNo, needAdd=0):
        itemUIDList = self.dItemNoByUIDList.get(iNo, [])
        if not itemUIDList:
            return None
        for iUID in itemUIDList:
            itemObj = self.dKeyMapItem.get(iUID, None)
            print itemObj.iNum
            if itemObj and itemObj.canAdd(needAdd):
                return itemObj
        return None

    # 获取全部道具列表
    def getAllItem(self):
        allItem = self.dKeyMapItem.values()
        return allItem

    # 按物品类型获取物品列表, 其实可以做成缓存，看CPU情况
    def getItemListByType(self, iType):
        lAllItem = self.getAllItem()
        l = []
        for itemObj in lAllItem:
            if itemObj.Type() == iType:
                l.append(itemObj)
        return l


# addItem 1 9999
# getItemNum 1
# ud game.core.item.itemctn
