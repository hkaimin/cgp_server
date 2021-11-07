#!/usr/bin/env python
# -*- coding:utf-8 -*-
import game.mgr.player
from game.common.ctn import CPstContainerBase
from game.common.utility import *

# Test
class CTestContainer(CPstContainerBase):
    def __init__(self, iOwner, saveKey="", OwnerObj=None):
        CPstContainerBase.__init__(self, iOwner, saveKey, OwnerObj)
        self.iCurUsePet = 0  # 当前使用的宠物
        self.dPetNoByUID = {}  # 通过宠物对象No找到宠物对象UID
        self.OwnerObj = OwnerObj
        self.Init()

    def Init(self):
        self.OwnerObj.AddKey(self.saveKey, {})
        pass


    def ClearDirtyFlag(self):  # override
        super(CTestContainer, self).ClearDirtyFlag()

    def OnBorn(self):
        pass


    def GetRefreshItemList(self):
        return []

    def AddItem(self, obj, bSend=True, bLoginCall=False,isMarkDirty=True):
        CPstContainerBase.AddItem(self, obj, bSend, bLoginCall, isMarkDirty)
        self.dPetNoByUID[obj.No()] = obj.UID()


    def RemoveItem(self, obj, bSend=True, bRefresh=True):
        if self.dPetNoByUID.has_key(obj.No()):
            del self.dPetNoByUID[obj.No()]
        CPstContainerBase.RemoveItem(self, obj, bSend)

    # override
    def Load(self, dData):
        # print '==============Load====================', dData
        super(CTestContainer, self).Load(dData.get("Sp", {}))

    # override,加载宠物数据
    def LoadItem(self, iIndex, data):
        if type(data) == types.ListType:
            iNo, dData = data
        else:
            iNo, dData = data, {}
        return Load(iNo, dData) #这里接的是item的load

    # override
    def Save(self, bTransfer=False):
        dData = {}
        dSuper = super(CTestContainer, self).Save(bTransfer)
        if dSuper:
            dData["Sp"] = dSuper
        return dData

    def SaveItem(self, iIndex, obj, bTransfer=False):  # override
        if bTransfer:
            dData = obj.SaveEx()
        else:
            dData = obj.Save()
        if dData:
            return (obj.No(), dData)
        return obj.No()


    def GetPetIdByNo(self, iPetNo):
        return self.dPetNoByUID.get(iPetNo, 0)

    def GetItemByNo(self, iPetNo):
        iPetUid = self.dPetNoByUID.get(iPetNo, 0)
        if iPetUid:
            return self.GetItem(iPetUid)
        return None

    def MarkDirty(self):
        if self.OwnerObj:
            who = self.OwnerObj
        else:
            who = game.mgr.player.get_rpc_player(int(self.iOwner))
        if who:
            dData = self.Save()
            who.Set(self.saveKey, dData)
        pass






ONE_DAY_SEC = 60 * 60 * 24  # 一天的秒数

if not globals().has_key("giTestLastId"):
    giTestLastId = 0

# 神兽基类定义
class CTest(CEasyPersist):
    def __init__(self, iNo):
        super(CTest, self).__init__()
        global giTestLastId
        giTestLastId += 1
        self.iUID = giTestLastId
        self.iNo = iNo
        self.iOwner = 0
        self.OwnerObj = None

    def MarkDirty(self):
        who = self.getOwnerObj()
        if who:
            who.testctn.markDirty()
        pass

    def UID(self):
        return self.iUID

    def OnBorn(self, who, *tArgs):
        self.iBirthday = GetDayNo()  # 生产日期
        if who:
            self.OwnerObj = who
        self.MarkDirty()

    # override
    def Save(self):
        dData = {}
        dSuper = super(CTest, self).Save()
        if dSuper:
            dData["Sp"] = dSuper
        if self.iBirthday:
            dData["Bd"] = self.iBirthday
        return dData

    def SaveEx(self):
        dData = self.Save()
        dData["UID"] = self.iUID
        return dData

    def OnRemove(self):
        pass

    # override
    def Load(self, dData):
        super(CTest, self).Load(dData.get("Sp", {}))
        self.iBirthday = dData.get("Bd", 0)
        uid = dData.get("UID", 0)
        if uid:
            self.iUID = uid

    def Setup(self, bIsLoad, who):
        print "----------------Setups----"
        pass

    def No(self):
        return self.iNo

    def SetNo(self, iNo):
        self.iNo = iNo

    # 被放入容器时的唯一标识
    def ContainerKey(self):
        return self.iUID

    def OwnerId(self):
        return self.iOwner

    def SetOwnerID(self, iOwner):
        self.iOwner = iOwner

    def getOwnerObj(self):
        if self.OwnerObj:
            return self.OwnerObj
        return game.mgr.player.get_rpc_player(int(self.iOwner))

    def RoleId(self):
        return self.iOwner

    def Birthday(self):
        return self.iBirthday


if not globals().has_key("gdTestModule"):
    gdTestModule = {}

def Create(iNo):
    # if not gdTestModule.has_key(iNo):
    #     obj = CTest(iNo)
    # else:
    #     obj = gdTestModule.CTest(iNo)
    obj = CTest(iNo)
    return obj

def New(iNo, who=None, *tArgs):
    obj = Create(iNo)
    obj.OnBorn(who, *tArgs)
    return obj

def Load(iNo, dData):
    obj = Create(iNo)
    obj.Load(dData)
    return obj