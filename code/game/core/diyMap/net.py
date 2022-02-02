#!/usr/bin/env python
#coding:utf-8
# -*- coding:utf-8 -*-
__author__ = 'Administrator'
# from game.common.ctn import CPstContainerBase
from game.common.utility import *
import game.mgr.player
import time
from game import Game
from collections import OrderedDict
# from corelib import spawn, log, spawn_later
import corelib
from game.core.item.conf import *
import random


MAP_CNT = 10 # 个人玩家限制的最大上限

class netCmd(object):
    # 协议处理模块
    def __init__(self):
        self.mapBase = Game.res_mgr.res_mapBase
        self.dMapBaseTheme = Game.res_mgr.dMapBaseTheme
        self.mapSignData = Game.res_mgr.res_mapSignData

    # 请求打开UI
    # 默认带参数theme=1
    # dMapBaseTheme= {
    #    theme:{itype:[]}
    # }
    def rc_openDiyMapUI(self, theme = 1):
        # UnluckFunc = self.Query("UnluckFunc", {})
        # if not UnluckFunc.has_key(CItemUnlockFunc.UL_DIYMAP_FUNC):
        #     self.notify("该功能未解锁")
            # return {"isUnLock":0}
        dmapTheme = self.dMapBaseTheme
        dCanSelectTheme = OrderedDict()
        lUnLockTheme = []
        for itheme, themeInfo in dmapTheme.iteritems():
            if itheme in UnluckFunc.get(CItemUnlockFunc.UL_DIYMAP_FUNC):
                lUnLockTheme.append(itheme)
            name = themeInfo.get("name", "")
            dCanSelectTheme[itheme] = name
        isFirstOpen = self.Query("isFirstOpen", 0) # 是否第一次打开的引导标识

        DefaultBg = [1, 24, 24, 1, 2, 2, 2, 1, 1, 1, 26, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 3, 1,
                          1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 25, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1,
                          1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1,
                          3, 3, 1, 1, 2, 2, 2]
        if game.gm.gmFunc.G_is0210Ver:
            DefaultBg = [70, 70, 71, 71, 71, 70, 71, 71, 71, 70, 70, 70, 71, 71, 71, 71, 70, 71, 71, 71, 71, 70, 71, 71,
                         70, 70, 70, 70, 70, 70, 70, 71, 71, 71, 71, 71, 71, 71, 70, 71, 71, 71, 71, 71, 71, 71, 71, 70,
                         70, 70, 70, 70, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 70, 70, 70,
                         70, 70, 71, 71, 71, 70, 71, 71, 70, 71, 71, 71, 70, 71, 71, 70, 70, 70, 71, 70, 70, 70, 70, 70,
                         71, 70, 70]
        res = {
            "isFirstOpen":isFirstOpen, # 是否第一次打开
            "isUnLock":1,
            "canSelectTheme":dCanSelectTheme, # 可选择的主题 {themeId: themeName,...}
            "dSelectTheme":dmapTheme.get(theme,{}), # 当前选择主题 {类型1：地图块列表，类型2：地图块列表,...}
            "theme":theme, # 当前选择主题ID
            "DefaultBg": DefaultBg, # 默认填充背景，只有一层背景图，打开时先显示默认背景
            "lUnLockTheme":lUnLockTheme
        }
        if not isFirstOpen:
            isFirstOpen = 1
            self.Set("isFirstOpen", isFirstOpen)
        try:
            Game.glog.log2File("openDiyMapUI",
                               "%s|%s|%s" % (
                                   self.id, self.Name(), self.data.account))
        except:
            pass
        return res

    # 切换主题
    def rc_changeTheme(self, theme=1):
        dmapTheme = self.dMapBaseTheme
        res = {
            "dSelectTheme": dmapTheme.get(theme, {}),  # 当前选择主题 {类型1：地图块，类型2：地图块。。。}
            "theme": theme,  # 当前选择主题ID
        }
        return res

    # 保存地图， 按战斗下发的形式上传
    # lBgConf: 地图层
    # lLayerConf: 障碍层
    # mapName 地图名字
    # mapSign 地图签名
    # mapkey # 地图ID，如果第一次保存，就传0；
    # 如果保存后，再修改，再保存，就要上传第一次保存下发的mapkey，服务端做update操作
    def rc_saveMap(self, lBgConf, lLayerConf, mapName, mapSign, mapkey):
        lmyMap = self.rc_getMyMaps()
        # mapkey = self.Query("my_mapkey", 0)
        # mapkey = mapkey + 1
        roleID = self.getUID()
        name = self.data.getName()
        headpic = self.base.getIcon()
        isFight = 0
        mapName = "%s的地图%s"%(name, mapkey)
        mapSignKey = self.mapSignData.keys()
        signkey = random.choice(mapSignKey)
        signData = self.mapSignData.get(signkey)
        mapSign = signData.name

        # mapName = "%s的地图"%(name)
        # mapSign = "%s的签名"%(mapName)
        modifyMapCnt = self.getDiyMapCnt()
        # if modifyMapCnt <=0:
        #     self.notify("地图设计图不足")
        #     return {}
        # print lBgConf, lLayerConf, mapName, mapSign, mapkey
        # self.converToString(mapkey, lBgConf, lLayerConf)
        # return {"roleId":self.id,"mapkey":1003}
        if not mapkey: # 新增
            # if len(lmyMap) == 0:
            #     isFight = 1
            # print "0---------lmyMap------------",len(lmyMap)
            if len(lmyMap) > MAP_CNT:
                self.notify("地图数量已达到上限！")
                return {}
            data = Game.rpc_diymap_info.makeDiyMap(roleID, name, headpic, lBgConf, lLayerConf, mapName, mapSign, isFight)
        else: # 更新
            data = Game.rpc_diymap_info.updateMakeDiyMap(roleID, name, headpic, lBgConf, lLayerConf, mapName, mapSign, mapkey)
        self.notify("保存成功")
        try:
            lBgConf = str(lBgConf)
            lLayerConf = str(lLayerConf)
            lBgConf = lBgConf.replace(", ", "_").replace("[", "").replace("]", "")
            lLayerConf = lLayerConf.replace(", ", "_").replace("[", "").replace("]", "")
            Game.glog.log2File("saveMap",
                               "%s|%s|%s|%s|%s" % (
                                   self.id, self.Name(), self.data.account,str(lBgConf),str(lLayerConf)))
        except:
            pass

        return data # {"roleId":roleId, "mapkey":mapkey}

    # 调试时候的弹字提醒，显示角色id和地图id
    def converToString(self, mapkey, lBgConf, lLayerConf):
        roleID = self.getUID()
        lBgConf = str(lBgConf)
        lLayerConf = str(lLayerConf)
        print lBgConf, lLayerConf
        lBgConf = lBgConf.replace(", ", "_").replace("[","").replace("]","")
        lLayerConf = lLayerConf.replace(", ", "_").replace("[","").replace("]","")
        print lBgConf
        print lLayerConf
        Game.glog.log2File("diyMap", "make|rid:%s|mapkey:%s\n|lBgConf:\n%s\n|lLayerConf:\n%s\n" % (roleID, mapkey, str(lBgConf), str(lLayerConf)))
        d = {"roleId":self.id, "mapkey":mapkey}
        corelib.spawn_later(1.5, self.notify, str(d))
        pass

    # 点赞
    # iType = 1 # 最新排行榜
    # iType = 2 # 最热排行榜
    def rc_addLike(self, rid, mapKey, iType):
        who=self
        LikeCnt = self.getLikeCnt()
        # if LikeCnt <=0:
        #     self.notify("剩余点赞次数不足")
        # rid = self.getUID()
        isOKAddLike = self.doAddLike()
        if not isOKAddLike:
            # self.notify("点赞数量不足，快去商城购买吧~")
            return
        like = Game.rpc_diymap_info.addLike(rid, mapKey)
        if like:
            if iType == 1:
                self.rc_getNewRank(True)
            elif iType == 2:
                self.rc_getHopRank(True)
        return {
            "rid":who.getUID(),
            "mapKey": mapKey,
            "like":like
        }

    # 获取排行榜(最热)
    def rc_getHopRank(self, isG2C=False):
        # dInfo["rid"] = rid
        # dInfo["name"] = name
        # dInfo["headpic"] = headpic
        # dInfo["mapkey"] = mapkey
        # dInfo["lBgconf"] = bgconf
        # dInfo["lLayerconf"] = layerconf
        # dInfo["like"] = like
        # lmapRank.append(dInfo)
        iLikeCnt = self.getLikeCnt() # 点赞数量
        lmapRank = Game.rpc_diymap_info.getMapLikeRank()
        # if self.data.
        isGM = self.data.IsGm()
        if isGM:
            print lmapRank
        if isG2C:
            self.broadcast("getHopRank", {"lhotRank":lmapRank})
        return {"lhotRank":lmapRank, "iLikeCnt":iLikeCnt}

    # 获取排行榜(最新)
    def rc_getNewRank(self, isG2C=False):
        # dInfo["rid"] = rid
        # dInfo["name"] = name
        # dInfo["headpic"] = headpic
        # dInfo["mapkey"] = mapkey
        # dInfo["lBgconf"] = bgconf
        # dInfo["lLayerconf"] = layerconf
        # dInfo["like"] = like
        # lmapRank.append(dInfo)
        iLikeCnt = self.getLikeCnt() # 点赞数量
        lnewRank = Game.rpc_diymap_info.getNewRank()
        isGM = self.data.IsGm()
        if isGM:
            print lnewRank
        if isG2C:
            self.broadcast("getNewRank", {"lnewRank":lnewRank})
        return {"lnewRank":lnewRank, "iLikeCnt":iLikeCnt}

    # 查看我的地图
    def rc_getMyMaps(self):
        who = self
        rid = who.getUID()
        MyMaps = Game.rpc_diymap_info.getMyMaps(rid)
        # print "--MyMaps-",len(MyMaps)
        for mid, mInfo in MyMaps.iteritems():
            if mInfo.get("isFight") == None:
                mInfo['isFight'] = 0
        return MyMaps

    # 设置出战地图
    def rc_setFightMap(self, mapId):
        who = self
        rid = who.getUID()
        mapInfo = Game.rpc_diymap_info.setFightMap(rid, mapId)
        who.Set("FightMap", mapInfo)
        return mapInfo

    # 获取拍卖场数据
    def rc_getNftMarket(self):
        return Game.rpc_diymap_info.rc_getNftMarket()

    # sell nft
    def rc_SellNft(self,nftIndex,money):
        self.notify("Sales Success!")
        return Game.rpc_diymap_info.rc_SellNft(nftIndex,money)

    # buy nft
    def rc_BuyNft(self,nftIndex,sAddress):
        self.notify("Buys Success!")
        return Game.rpc_diymap_info.rc_BuyNft(nftIndex,sAddress)

import game.core.item
import game.gm.gmFunc