#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import random
import string
import game.mgr.player
from game.common import utility
from game.core.cycleData import CycleDay, CycleWeek, CycleMonth, CycleHour


#全部容器基类，抽象类
class CContainerBase(object):
    def __init__(self,iOwner):
        self.iOwner=iOwner
        self.dKeyMapItem={}

    def ClearContainer(self):#从场景服回传到主服务器上才会调用
        self.dKeyMapItem={}

    #所有者id
    def OwnerId(self):
        return self.iOwner

    def SendId(self):
        return self.iOwner

    def SetOwnerId(self,iOwner):
        self.iOwner=iOwner

    #子项总数
    def ItemCount(self):
        return len(self.dKeyMapItem)

    #根据键值获取子项
    def GetItem(self,iKey):
        # print "----self.dKeyMapItem:",self.dKeyMapItem
        return self.dKeyMapItem.get(iKey,None)

    #返回所有子项
    def GetAllItemList(self):
        return self.dKeyMapItem.values()

    #返回所有键值
    def GetAllKeys(self):
        return self.dKeyMapItem.keys()

    #新增子项
    def AddItem(self,obj):
        # print "AddItem self.dKeyMapItem.has_key(obj.ContainerKey())",self.dKeyMapItem.has_key(obj.ContainerKey())
        self.dKeyMapItem[obj.ContainerKey()]=obj
        # print "self.dKeyMapItem:",self.dKeyMapItem
        obj.SetOwnerID(self.OwnerId())
        return True

    #移除子项
    def RemoveItem(self,obj,bSend=True,bRefresh=True): #bRefresh 装备删除的时候要不要重新刷新战斗力
        iKey=obj.ContainerKey()
        if not self.dKeyMapItem.has_key(iKey):
            return False
        del(self.dKeyMapItem[iKey])
        # 对象删除时的调用
        if bRefresh:
            obj.OnRemove()
        else:
            obj.OnRemove(bRefresh)
        return True


#有持久化功能的容器(抽象类)
class CPstContainerBase(CContainerBase,utility.CEasyPersist):
    def __init__(self,iOwner,saveKey='', OwnerObj=None):
        CContainerBase.__init__(self,iOwner)
        utility.CEasyPersist.__init__(self)
        self.cycleDay = CycleDay(self)  # 天周期数据
        self.cycleWeek = CycleWeek(self)  # 周周期数据
        self.cycleMonth = CycleMonth(self)  # 月周期数据
        self.saveKey = saveKey
        self.OwnerObj = OwnerObj

    #根据数据生成子项，需要子类实现
    def LoadItem(self,iIndex,data):
        raise NotImplementedError

    #生成子项的保存数据
    def SaveItem(self,iIndex,obj):
        dData=obj.Save()
        if dData:
            return (obj.ContainerKey(),dData)
        else:
            return obj.ContainerKey()

    def ClearDirtyFlag(self):#override
        super(CPstContainerBase,self).cleanDirty()
        for v in self.dKeyMapItem.itervalues():
            v.ClearDirtyFlag()

    #目的是为了打个脏标志
    #override
    def AddItem(self,obj,isMarkDirty=True):
#       print "============= CPstContainerBase AddItem bLoginCall:",bLoginCall
#         if not bCall:
#             who=self.OwnerObj
#             obj.Setup(False,who)
        super(CPstContainerBase,self).AddItem(obj)
        if isMarkDirty:
            self.MarkDirty()

    #override
    def RemoveItem(self,obj,bSend=True,bRefresh=True):
        if super(CPstContainerBase,self).RemoveItem(obj,bSend,bRefresh):
            self.MarkDirty()
            return True
        else:
            return False

    #override
    #load的时候不markdirty
    def Load(self,dData):
        super(CPstContainerBase,self).Load(dData.get("Sp",{}))
        for iIndex, data in enumerate(dData.get("Item",[])):
            print "iIndex:", iIndex
            obj=self.LoadItem(iIndex,data)
            if obj:
                self.AddItem(obj,False)
        self.cycleDay.load_from_dict(dData.get("D", {}))
        self.cycleWeek.load_from_dict(dData.get("W", {}))
        self.cycleMonth.load_from_dict(dData.get("M", {}))

    #override
    def Save(self,forced=False):
        dData={}
        dSuper=super(CPstContainerBase,self).Save()
        if dSuper:
            dData["Sp"]=dSuper
        list=[]
        for iIndex,obj in enumerate(self.dKeyMapItem.itervalues()):
            data=self.SaveItem(iIndex,obj)
            if data:
                list.append(data)
        if list:
            dData["Item"]=list
        dDay = self.cycleDay.to_save_bytes()
        if dDay:
            dData["D"] = dDay
        dWeek = self.cycleWeek.to_save_bytes()
        if dWeek:
            dData["W"] = dWeek
        dMonth = self.cycleMonth.to_save_bytes()
        if dMonth:
            dData["M"] = dMonth
        return dData

    #override
    def Setup(self):
        # who=C_FindObject(self.OwnerId())
        # if not who:
        #     return
        who = self.OwnerObj
        for obj in self.dKeyMapItem.values():
            obj.Setup(True,who)

    def MarkDirty(self):
        super(CPstContainerBase, self).markDirty()
        who = self.OwnerObj
        if who:
            who.base.markDirty()
        pass




