#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from game.common import utility

from corelib.frame import Game, MSG_FRAME_STOP
from game.models.rank import ModelRank
from corelib.gtime import get_days
from game.common.utility import *
#
# PVP_RANK_MAX = 200
#
#
# class RankInfo(utility.DirtyFlag):
#     """服务器信息"""
#     _rpc_name_ = 'rpc_rank_info'
#
#     def __init__(self):
#         utility.DirtyFlag.__init__(self)
#         self.data = None
#         self.lPvpRank = [] # PVP总排行榜
#         self.lLvRank = [] # PVP等级排行榜
#
#         self.lFriendPvpRank = [] # PVP总排行榜
#         self.lFriendLVRank = [] # PVP等级排行榜
#
#         self.save_cache = {}  # 存储缓存
#
#         Game.sub(MSG_FRAME_STOP, self._frame_stop)
#
#     def getPvpRank(self):
#         # print "--lPvpRank:",self.lPvpRank
#         return self.lPvpRank
#
#     def getLvRank(self):
#         # print "--lLvRank:", self.lLvRank
#         return self.lLvRank
#
#     def getFriendPvpRank(self):
#         return self.lFriendPvpRank
#
#     def getFriendLvRank(self):
#         return self.lFriendLVRank
#
#     def start(self):
#         print ">>>>>>>>>>>>>> Rank stat <<<<<<<<<<<<<<<<"
#         self.data = ModelRank.load(Game.store, ModelRank.TABLE_KEY)
#         # print self.data , self.data.dataDict
#         print ">>>>>>>>>>>>>> Rank stat <<<<<<<<<<<<<<<< 2"
#         if not self.data:
#             self.data = ModelRank()
#             self.data.set_owner(self)
#             self.data.save(Game.store, forced=True)
#         else:
#             self.data.set_owner(self)
#         self.load_from_dict(self.data.dataDict)
#
#     def _frame_stop(self):
#         self.data.save(Game.store, forced=True, no_let=True)
#
#     # 存库数据
#     def to_save_dict(self, forced=False):
#         if self.isDirty() or forced or not self.save_cache:
#             self.save_cache = {}
#             self.save_cache["lPvpRank"] = self.lPvpRank
#             self.save_cache["lLvRank"] = self.lLvRank
#         return self.save_cache
#
#     # 读库数据初始化
#     def load_from_dict(self, data):
#         print "-44444444444444444-------load rank data", data
#         self.lPvpRank = data.get("lPvpRank", [])
#         self.lLvRank = data.get("lLvRank", [])
#         print "self.lPvpRank:",self.lPvpRank
#         print "self.lLvRank:",self.lLvRank
#         self.markDirty()
#
#     def SaveRank(self):
#         self.data.save(Game.store, forced=True)
#
#     # ================ pvp排行榜 ================
#     def updatePvpRank(self, rid, sName, sPic, winCount, winRate, wechatId=""):
#         # winCount 胜场
#         # winRate 胜率
#         # wechatId 微信ID
#         tInfo = [rid, sName, sPic, winCount, winRate, wechatId]
#         self.insterPvpRank(rid, tInfo)
#         pass
#
#     def forceUpdatePveRank(self, rid, sName, sPic, winCount, winRate, wechatId=""):
#         tInfo = [rid, sName, sPic, winCount, winRate, wechatId]
#         self.insterPvpRank(rid, tInfo, forceUpdate=True)
#
#     def insterPvpRank(self, rid, tUpdateInfo, forceUpdate=False):
#         # tInfo = [rid, sName, sPic, winCount, winRate, wechatId]
#         print ">>>>>>>>> insterPvpRank", tUpdateInfo
#         for i, tInfo in enumerate(self.lPvpRank):
#             if tInfo[0] == rid:
#                 if forceUpdate:
#                     self.lPvpRank.pop(i)
#                     break
#                 if tUpdateInfo[3] > tInfo[3]:
#                     self.lPvpRank.pop(i)
#                     break
#                 elif tUpdateInfo[4] != tInfo[4]:
#                     self.lPvpRank.pop(i)
#                     break
#                 return
#         BinaryInsertRight(self.lPvpRank, tUpdateInfo, self.MyPvpSort)
#         while len(self.lPvpRank) > PVP_RANK_MAX:
#             self.lPvpRank.pop()
#         print self.lPvpRank
#         self.markDirty()
#         pass
#
#     def MyPvpSort(self, a, b):
#         l1 = [a[3],a[4],-1*a[1]]
#         l2 = [b[3],b[4],-1*b[1]]
#         if l1 > l2:
#             return 1
#         else:
#             return -1
#
#     # 获取我的排名
#     def getMypvpRank(self, who):
#         i = 0
#         for t in self.lPvpRank:
#             if t[0] == who.UID:
#                 return i + 1
#             i = i + 1
#         return i
#
#     # 获取我的排名详细
#     def getMypvpRankInfo(self, who):
#         for t in self.lPvpRank:
#             if t[0] == who.UID:
#                 return t
#         return None
#
#     # ================ 等级排行榜 ================
#     def updateLvRank(self, rid, sName, sPic, lv, wechatId=""):
#         tInfo = [rid, sName, sPic, lv, wechatId]
#         self.insterLvRank(rid, tInfo)
#         pass
#
#     def forceUpdateLvRank(self, rid, sName, sPic, lv, wechatId=""):
#         tInfo = [rid, sName, sPic, lv, wechatId]
#         self.insterLvRank(rid, tInfo, forceUpdate=True)
#
#     def insterLvRank(self, rid, tUpdateInfo, forceUpdate=False):
#         for i, tInfo in enumerate(self.lLvRank):
#             if tInfo[0] == rid:
#                 if forceUpdate:
#                     self.lLvRank.pop(i)
#                     break
#                 if tUpdateInfo[3] > tInfo[3]:
#                     self.lLvRank.pop(i)
#                     break
#                 return
#         BinaryInsertRight(self.lLvRank, tUpdateInfo, self.MyLvSort)
#         while len(self.lLvRank) > PVP_RANK_MAX:
#             self.lLvRank.pop()
#         print self.lLvRank
#         self.markDirty()
#         pass
#
#     def MyLvSort(self, a, b):
#         l1 = [a[3],-1*a[1]]
#         l2 = [b[3],-1*b[1]]
#         if l1 > l2:
#             return 1
#         else:
#             return -1
#
#     # 获取我的排名
#     def getMylvRank(self, who):
#         i = 0
#         for t in self.lLvRank:
#             if t[0] == who.UID:
#                 return i + 1
#             i = i + 1
#         return i
#
#     # 获取我的排名详细
#     def getMylvRankInfo(self, who):
#         for t in self.lLvRank:
#             if t[0] == who.UID:
#                 return t
#         return None
#
#
