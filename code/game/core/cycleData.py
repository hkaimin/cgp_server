#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cPickle

from game.common import utility
import weakref

class CycleBase(utility.DirtyFlag):
    def __init__(self, owner, keepCyc=1):
        utility.DirtyFlag.__init__(self)
        # print "------------->>>> owner:", owner
        # self.owner = owner
        self.owner = weakref.ref(owner)  # 拥有者
        # print "--------weakref----", self.owner
        self.keepCyc = keepCyc #保存多少个周期的数据
        self.data = {} #{cycNo:json}

    #存库数据
    def to_save_bytes(self, forced=False):
        return cPickle.dumps(self.data)

    #读库数据初始化
    def load_from_dict(self, data):
        if not data:
            return
        data = cPickle.loads(str(data))
        lCycNo = data.keys()
        lCycNo.sort()
        for iCycNo in lCycNo:
            if self.getCycleNo() >= iCycNo + self.keepCyc:
                del data[iCycNo]
                self.markDirty()
            else:
                break
        self.data = data

    def markDirty(self):
        utility.DirtyFlag.markDirty(self)
        if self.owner:
            print "-----markDirty------<><><>:",self.owner
            self.owner().markDirty()

    def getCycleNo(self):
        raise NotImplementedError

    #iWhichCyc的值范围 0=当前周期 -1=上一个周期 -2=上两个周期 以此类推
    def Query(self, key, default=0, iWhichCyc=0, iCycNo=0):
        if not iCycNo:
            iCycNo = self.getCycleNo() + iWhichCyc
        return self.data.get(iCycNo, {}).get(key, default)

    def Set(self, key, value, iCycNo=0, iWhichCyc=0):
        if not iCycNo:
            iCycNo = self.getCycleNo() + iWhichCyc
        dCyc = self.data.setdefault(iCycNo, {})
        dCyc[key] = value
        self.markDirty()

    def Delete(self, key):
        iCycNo = self.getCycleNo()
        if self.data.has_key(iCycNo) and self.data[iCycNo].has_key(key):
            del self.data[iCycNo][key]
            self.markDirty()

    def Clear(self, iWhichCyc=0):
        self.data = {}
        self.markDirty()

#天周期数据
class CycleCustom(CycleBase):
 
    def __init__(self, owner, callback, keepCyc=1):
        CycleBase.__init__(self, owner, keepCyc=keepCyc)
        self.callback = callback
 
    def getCycleNo(self):
        return self.callback()

#天周期数据
class CycleDay(CycleBase):
    def getCycleNo(self):
        return utility.GetDayNo()

#周周期数据
class CycleWeek(CycleBase):
    def getCycleNo(self):
        return utility.GetWeekNo()

#月周期数据
class CycleMonth(CycleBase):
    def getCycleNo(self):
        return utility.GetMonthNo()

#小时周期数据
class CycleHour(CycleBase):
    def getCycleNo(self):
        return utility.GetHourNo()

#指定当天小时的周期数据  #凌晨5点
class CycleSpecHour5(CycleBase):
    def getCycleNo(self):
        return utility.GetSpecHour5No()