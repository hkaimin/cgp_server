#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import time
import traceback
import random
import string
import types

from requests import Session
from functools import partial

gtStandardTime = (2018,6,1,0,0,0,0,0,0) # 2018-06-01 00:00:00
giStandardTime = int(time.mktime(gtStandardTime))

gtSpecTime_Hour_5 = (2018,6,1,5,0,0,0,0,0) # 2018-06-01 05:00:00  凌晨5点
giSpecTime_Hour_5 = int(time.mktime(gtSpecTime_Hour_5))

def GetMinNo(t=0): #时间戳：分钟序号
    if not t:
        t = int(time.time())
    return (t-giStandardTime)/60+1

def GetHourNo(t=0): #时间戳：小时序号
    if not t:
        t = int(time.time())
    return (t-giStandardTime)/3600+1

def GetDayNo(t=0): #时间戳：天序号
    if not t:
        t = int(time.time())
    return (t-giStandardTime)/3600/24+1

def GetWeekNo(t=0): #时间戳：周序号
    if not t:
        t = int(time.time())
    return (t-giStandardTime)/3600/24/7+1

def GetMonthNo(t=0): #时间戳：月序号
    if not t:
        t = int(time.time())
    curTime = time.localtime(t)
    return (curTime[0]-gtStandardTime[0]*12)+(curTime[1]-gtStandardTime[1]) +1

def GetSpecHour5No(t=0): #时间戳：小时序号  凌晨5点
    if not t:
        t = int(time.time())
    return (t-giSpecTime_Hour_5)/3600+1

def Choice(lRand): #[(id, rate), (id, rate)]
    iTotal = 0
    for one in lRand:
        iTotal += one[1]
    if iTotal <= 0:
        return
    iNum = random.randint(1, iTotal)
    tmp = 0
    for one in lRand:
        tmp += one[1]
        if tmp >= iNum:
            return one[0]

def ChoiceReturn(lRand): #[(id, rate), (id, rate)]
    iTotal = 0
    for one in lRand:
        iTotal += one[1]
    iNum = random.randint(1, iTotal)
    tmp = 0
    for one in lRand:
        tmp += one[1]
        if tmp >= iNum:
            return one

# =========== pst 模块迟点应该要独立抽出来的============
class DirtyFlag(object):
    def __init__(self):
        self.dirty = False

    def isDirty(self):
        return self.dirty

    def markDirty(self):
        self.dirty = True


    def cleanDirty(self):
        self.dirty = False

# CPersist的实现类，增加属性dData，对一个类对象的属性封装
# 例:dData = {"id":1,"name"="abc"}
class CEasyPersist(DirtyFlag):
    def __init__(self):
        super(CEasyPersist, self).__init__()
        self.dData = {}

    def Add(self, key, value, default=0):  # 返回成功后的结果值
        self.dData[key] = self.dData.get(key, default) + int(value)
        self.markDirty()
        return self.dData[key]

    # 新增方法
    def AddKey(self, key, default=0):
        self.dData.setdefault(key, default)
        self.markDirty()
        return self.dData[key]

    def Delete(self, key):
        if self.dData.has_key(key):
            del self.dData[key]
            self.markDirty()

    def Set(self, key, value):
        if value == None:
            raise Exception("CEasyPersist.Set的参数value不能是None")
        elif type(value) == types.BooleanType:
            raise Exception("bool类型存成0或1就行,不要存成True或False")
        self.dData[key] = value
        self.markDirty()
        return value

    def Query(self, key, default=None):
        return self.dData.get(key, default)

    def Save(self):
        return self.dData

    def Load(self, dData):
        self.dData = dData

# =========== pst 模块 ============




# 根据玩家id，生成邀请码
def activation_code(id,length=8):
    '''
    id + L + 随机码
    string模块中的3个函数：string.letters，string.printable，string.printable
    '''
    prefix = hex(int(id))[2:]+ 'L'
    length = length - len(prefix)
    chars=string.ascii_letters+string.digits
    return prefix + ''.join([random.choice(chars) for i in range(length)])

# 邀请码 转 玩家id
def get_id(code):
    ''' Hex to Dec '''
    id_hex = code.split('L')[0]
    return str(int(id_hex.upper(), 16))



#获得0~(i-1)之间的随机数，请别传0进去(传0则返回0)
def Random(i):
    return int(random.random()*i)

#获得i到j(包括i和j)之间的随机数
def RandRange(i,j):
    return random.randint(i,j)

#根据几率返回key,such as  dDict={1:25,2:20,3:10,4:30,5:15}
#未命中返回None,传入空字典返回None
#类似NBA抽签选秀的方式，dDict的单元中的value值越高，概率就越高
def RandomKey(dDict,iTotal=0):
    if iTotal==0:
        for v in dDict.itervalues():
            iTotal+=v
    i=Random(iTotal)
    t=0
    for k,v in dDict.iteritems():
        t+=v
        if i<t:
            return k
    return None


# 查找>=某区间对应的键,查找小于参数1的最近的key所对应的键
def GetRightKey(i, dRange, default=0):
    if dRange.has_key(i):
        return i
    lKeys = dRange.keys()
    lKeys.sort(None, None, True)  # 从大到小
    for iKey in lKeys:
        if i >= iKey:  # 比最大的还大
            return iKey
    else:
        return default


# 查找<=某区间对应的键,查找大于参数1的最近的key所对应的键
def GetLeftKey(i, dRange, default=0):
    if dRange.has_key(i):
        return i
    lKeys = dRange.keys()
    lKeys.sort()  # 从小到大
    for iKey in lKeys:
        if i <= iKey:  # 比最大的还大
            return iKey
    else:
        return default

#查找>=某区间对应的值,查找小于参数1的最近的key所对应的值
def GetRightValue(i,dRange,default=0):
    if dRange.has_key(i):
        return dRange[i]
    lKeys=dRange.keys()
    lKeys.sort(None,None,True)#从大到小
    for iKey in lKeys:
        if i>=iKey:#比最大的还大
            return dRange[iKey]
    else:
        return default

#查找<=某区间对应的值,查找大于参数1的最近的key所对应的值
def GetLeftValue(i,dRange,default=0):
    if dRange.has_key(i):
        return dRange[i]
    lKeys=dRange.keys()
    lKeys.sort()#从小到大
    for iKey in lKeys:
        if i<=iKey:#比最小的还小
            return dRange[iKey]
    else:
        return default


class AsyncRequest(object):
    """ Asynchronous request.

    Accept same parameters as ``Session.request`` and some additional:

    :param session: Session which will do request
    :param callback: Callback called on response.
                     Same as passing ``hooks={'response': callback}``
    """
    def __init__(self, method, url, **kwargs):
        #: Request method
        self.method = method
        #: URL to request
        self.url = url
        #: Associated ``Session``
        self.session = kwargs.pop('session', None)
        if self.session is None:
            self.session = Session()

        callback = kwargs.pop('callback', None)
        if callback:
            kwargs['hooks'] = {'response': callback}

        #: The rest arguments for ``Session.request``
        self.kwargs = kwargs
        #: Resulting ``Response``
        self.response = None

    def send(self, **kwargs):
        """
        Prepares request based on parameter passed to constructor and optional ``kwargs```.
        Then sends request and saves response to :attr:`response`

        :returns: ``Response``
        """
        merged_kwargs = {}
        merged_kwargs.update(self.kwargs)
        merged_kwargs.update(kwargs)
        try:
            self.response = self.session.request(self.method,
                                                self.url, **merged_kwargs)
        except Exception as e:
            self.exception = e
            self.traceback = traceback.format_exc()
        return self

# Shortcuts for creating AsyncRequest with appropriate HTTP method
get = partial(AsyncRequest, 'GET')
options = partial(AsyncRequest, 'OPTIONS')
head = partial(AsyncRequest, 'HEAD')
post = partial(AsyncRequest, 'POST')
put = partial(AsyncRequest, 'PUT')
patch = partial(AsyncRequest, 'PATCH')
delete = partial(AsyncRequest, 'DELETE')


def detailtrace():
  retStr = ""
  curindex=0
  f = sys._getframe()
  f = f.f_back    # first frame is detailtrace, ignore it
  while hasattr(f, "f_code"):
    co = f.f_code
    retStr = "%s(%s:%s)->"%(os.path.basename(co.co_filename),
         co.co_name,
         f.f_lineno) + retStr
    f = f.f_back
  return retStr


#二分插入法，如果值相同，在所有相等的元素后面插入
#lOrder已经是有序的list,uItem是要插入的元素,
#tCompareFunc,可以不传,不传则以小于号来比较
def BinaryInsertRight(lOrder,uItem,*tCompareFunc):
    iIndex=BinarySearchRight(lOrder,uItem,*tCompareFunc)
    lOrder.insert(iIndex,uItem)


# 二分查找法
# lOrder已经是有序的list,uItem是要查找的元素,返回一个恰当的index供插入
# tCompareFunc,可以不传,不传则以><来比较
def BinarySearchRight(lOrder, uItem, *tCompareFunc):
    iLow, iHigh = 0, len(lOrder)  # iHigh是pass the end的非法索引
    while iLow < iHigh:
        iMid = iLow + (iHigh - iLow) / 2

        if tCompareFunc:
            iResult = MultiCompare(uItem, lOrder[iMid], *tCompareFunc)
        elif uItem < lOrder[iMid]:
            iResult = -1
        else:  # 相等也认为是大于,因为要尽量往后面insert
            iResult = 1

        if iResult < 0:
            iHigh = iMid  # 即将插入的位置可能是iMid
        else:
            iLow = iMid + 1  # 即将插入的位置可能是iMid+1
    return iLow


#多重比较器
#对两个obj依次用多个函数进行比武,直到两obj决出胜负
def MultiCompare(obj1,obj2,*tCompareFunc):
    if not tCompareFunc:
        raise Exception,"必须给出比较函数"
    for func in tCompareFunc:
        iResult=func(obj1,obj2)
        if iResult!=0:#用胜负已经出来了,不用继续比了
            return iResult
    return 0
