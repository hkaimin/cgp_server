#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from game.common import utility

from corelib.frame import Game, MSG_FRAME_STOP
from game.models.diymap import ModelDiyMap
from corelib.gtime import get_days
from game.common.utility import *
import cPickle
from game.define import horse_define , msg_define
import random

MAP_RANK_MAX = 50
MAP_SHOW_RANK = 20


class DiyMapInfo(utility.DirtyFlag):
    """diy地图"""
    _rpc_name_ = 'rpc_diymap_info'

    def __init__(self):
        utility.DirtyFlag.__init__(self)
        self.data = None
        self.dMapInfo = {} # pid:mapinfo
        self.dMapInfoMapKey = {} # mapkey:mapinfo
        self.lmapLikeRank = [] # 点赞排行榜
        self.lmapNewRank = [] # 最新排行榜
        self.dmapLikeData = {}

        self.mapTranceNo = 1000
        self.nftPool = {} #horse nft info
        self.nftMarket = [] #拍卖场
        self.exbihitionDirty = True #牧场是否被修改 
        self.exbihitionCache = {} #牧场总奖励池

        self.save_cache = {}  # 存储缓存

        Game.sub(MSG_FRAME_STOP, self._frame_stop)
        Game.sub(msg_define.MSG_ONE_MINUTE, self.event_one_minute)

    def start(self):
        print ">>>>>>>>>>>>>> DiyMapInfo stat 1<<<<<<<<<<<<<<<"
        self.data = ModelDiyMap.load(Game.store, ModelDiyMap.TABLE_KEY)
        # print self.data
        print ">>>>>>>>>>>>>> DiyMapInfo stat 1<<<<<<<<<<<<<<<< 2"
        if not self.data:
            self.data = ModelDiyMap()
            self.data.set_owner(self)
            self.data.save(Game.store, forced=True)
        else:
            self.data.set_owner(self)
        self.load_from_dict(self.data.dataDict)

    def _frame_stop(self):
        self.data.save(Game.store, forced=True, no_let=True)

    # 每分钟事件
    def event_one_minute(self):
        iCurTotalRewards = self.exbihitionCache.get("iCurTotalRewards",0)
        iCurTotalRewards += horse_define.EXHIBITION_EVERY_MINUTE
        self.exbihitionCache["iCurTotalRewards"] = iCurTotalRewards
        self.markDirty()
        print '--event_one_minute--iCurTotalRewards--' ,iCurTotalRewards

    def markDirty(self):
        super(DiyMapInfo, self).markDirty()
        self.data.modify()

    # 存库数据
    def to_save_dict(self, forced=False):
        if self.isDirty() or forced or not self.save_cache:
            save_cache = {}
            save_cache["dMapInfo"] = cPickle.dumps(self.dMapInfo)
            save_cache["dMapInfoMapKey"] = cPickle.dumps(self.dMapInfoMapKey)
            save_cache["lmapLikeRank"] = self.lmapLikeRank
            save_cache["mapTranceNo"] = self.mapTranceNo
            save_cache["lmapNewRank"] = self.lmapNewRank
            save_cache["dmapLikeData"] = self.dmapLikeData

            save_cache["nftPool"]   = self.nftPool
            save_cache["nftMarket"] = self.nftMarket
            save_cache["exbihitionCache"] = self.exbihitionCache

            self.save_cache = save_cache
        else:
            save_cache = self.save_cache

        return save_cache

    # 读库数据初始化
    def load_from_dict(self, data):
        # print "-55555555555555-------load mapinfo data", data
        if data.get("dMapInfo", {}):
            self.dMapInfo = cPickle.loads(str(data.get("dMapInfo", {})))
        if data.get("dMapInfoMapKey", {}):
            self.dMapInfoMapKey = cPickle.loads(str(data.get("dMapInfoMapKey", {})))
        self.lmapLikeRank = data.get("lmapLikeRank",[])
        self.lmapNewRank = data.get("lmapNewRank",[])
        self.mapTranceNo = data.get("mapTranceNo", 1000)
        self.dmapLikeData = data.get("dmapLikeData",{})

        self.nftPool = data.get("nftPool",{})
        self.nftMarket = data.get("nftMarket",[])
        self.exbihitionCache = data.get("exbihitionCache",{})
        # print "------------->>>>self.dMapInfo:", self.dMapInfo
        self.markDirty()

    def SaveMapInfo(self):
        self.data.save(Game.store, forced=True)

    def GeneraDiyMapTranceNo(self):
        self.mapTranceNo += 1
        self.data.modify()
        self.data.save(Game.store, forced=True, no_let=True)
        return self.mapTranceNo

    def GetNftInfo(self,iIndex):
        return self.nftPool.get(iIndex,{})

    def SaveNftInfo(self,iIndex,dNftData):
        self.nftPool[str(iIndex)] = dNftData
        dLoad = self.nftPool.get(str(iIndex),{})
        #fix
        if not dLoad.get("breedMax",0):
            self.fixData(dLoad)
        self.data.modify()
        self.data.save(Game.store, forced=True, no_let=True)

    def rc_getNftMarket(self):
        lMarketData = []
        bFix = False
        for iIndex in self.nftMarket:
            dLoad = self.nftPool.get(str(iIndex),{})

            #fix
            if not dLoad.get("breedMax",0):
                bFix = True
                self.fixData(dLoad)
            
            dHorse = {
                "name":dLoad["sRanName"],
                "iType": horse_define.HORSE_INFO[dLoad["iRandomHorseType"]]["iType"] ,
                "res_key": horse_define.HORSE_INFO[dLoad["iRandomHorseType"]]["res_key"] ,
                "id": iIndex ,
                "sellStatus": dLoad["sellStatus"],
                "score": dLoad["strength"] + dLoad["speed"] + dLoad["dexterity"] + dLoad["burse"],
                "money": dLoad.get("money",11) ,
                "star": random.randint(1,5),#星星数
                "iSex": dLoad.get("iSex",1),#默认公的
                "strength": dLoad["strength"],#体力
                "MaxStrength": dLoad["MaxStrength"],
                "speed": dLoad["speed"],#速度
                "MaxSpeed": dLoad["MaxSpeed"],
                "dexterity": dLoad["dexterity"],#灵巧
                "MaxDexterity": dLoad["MaxDexterity"],
                "burse": dLoad["burse"],#爆发
                "MaxBurse": dLoad["MaxBurse"],
                "stamina": dLoad["stamina"],#耐力
                "start": dLoad["start"],#启动
                "wisdom": dLoad["wisdom"],#智慧
                "constitution": dLoad["constitution"],#体质
                "landMax":horse_define.LAND_MAX_NUM,#地形适应最大值
                "grassland": dLoad["grassland"],#草地
                "sand": dLoad["sand"],#沙地
                "mud": dLoad["mud"],#泥地
                "breedMax": dLoad["breedMax"],#繁殖次数上限
                "breed": dLoad.get("breed",0),#当前繁殖次数
                "energyMax": horse_define.ENERGY_CONFIG,#最大energy
                "energy": dLoad.get("energy",horse_define.ENERGY_CONFIG),#当前energy
                "days": (GetDayNo() - GetDayNo(dLoad["createTime"]))+1,#马匹年龄
            }
            lMarketData.append(dHorse)

        if bFix:
            self.markDirty()
            self.data.save(Game.store, forced=True, no_let=True)

        return {"lMarketData":lMarketData}

    def rc_SellNft(self,nftIndex,money):
        if int(nftIndex) not in self.nftMarket:
            self.nftMarket.append(nftIndex)
        dLoad = self.nftPool.get(str(nftIndex),{})
        dLoad["sellStatus"] = 1
        dLoad["money"] = money
        self.markDirty()
        self.data.save(Game.store, forced=True, no_let=True)
        return self.rc_getNftMarket()

    def rc_BuyNft(self,nftIndex,sAddress):
        lNftMarket = []
        for index in self.nftMarket:
            if int(nftIndex) == index:
                dLoad = self.nftPool.get(str(nftIndex),{})
                dLoad["sellStatus"] = 0
                dLoad["owner"] = sAddress
            else:
                lNftMarket.append(index)
        self.nftMarket = lNftMarket
        self.markDirty()
        self.data.save(Game.store, forced=True, no_let=True)
        return self.rc_getNftMarket()

    def getRandomMax(self,maxNum,tRandomSub):
        return int(random.randint(tRandomSub[0],tRandomSub[1])/100.0 * maxNum)

    def fixData(self,dLoad):
        tRandom = horse_define.HORSE_INFO[dLoad["iRandomHorseType"]]["tRandom"] #主属性
        tRandomSub = horse_define.HORSE_INFO[dLoad["iRandomHorseType"]]["tRandomSub"]
        iRandomMax = random.randint(tRandom[0],tRandom[1])
        dLoad["MaxStrength"] = self.getRandomMax(iRandomMax,tRandomSub)
        dLoad["strength"] = dLoad["MaxStrength"] / 2
        dLoad["MaxSpeed"] = self.getRandomMax(iRandomMax,tRandomSub)
        dLoad["speed"] = dLoad["MaxSpeed"] / 2
        dLoad["MaxDexterity"] = self.getRandomMax(iRandomMax,tRandomSub)
        dLoad["dexterity"] = dLoad["MaxDexterity"] / 2
        dLoad["MaxBurse"] = self.getRandomMax(iRandomMax,tRandomSub)
        dLoad["burse"] = dLoad["MaxBurse"] / 2

        tRandom2 = horse_define.HORSE_INFO[dLoad["iRandomHorseType"]]["tRandom2"] #副属性
        tRandomSub2 = horse_define.HORSE_INFO[dLoad["iRandomHorseType"]]["tRandomSub2"]
        iRandomMax = random.randint(tRandom2[0],tRandom2[1])
        dLoad["stamina"] = self.getRandomMax(iRandomMax,tRandomSub2)
        dLoad["start"] = self.getRandomMax(iRandomMax,tRandomSub2)
        dLoad["wisdom"] = self.getRandomMax(iRandomMax,tRandomSub2)
        dLoad["constitution"] = self.getRandomMax(iRandomMax,tRandomSub2)

        tRandom3 = horse_define.HORSE_INFO[dLoad["iRandomHorseType"]]["tRandom3"] #地形适应
        tRandomSub3 = horse_define.HORSE_INFO[dLoad["iRandomHorseType"]]["tRandomSub3"]
        iRandomMax = random.randint(tRandom3[0],tRandom3[1])
        dLoad["grassland"] = self.getRandomMax(iRandomMax,tRandomSub3)
        dLoad["sand"] = self.getRandomMax(iRandomMax,tRandomSub3)
        dLoad["mud"] = self.getRandomMax(iRandomMax,tRandomSub3)
        iRanInt = random.randint(1,1000)
        iRandomBreedMax = utility.GetLeftValue(iRanInt,horse_define.HORSE_BREED_RANDOM)
        dLoad["breedMax"] = iRandomBreedMax

    def rc_getTotalExhi(self):
        if self.exbihitionDirty:
            iTotalScore = 0
            iTotalHorse = 0
            for sIndex,dNft in self.nftPool.iteritems():
                if dNft.get("exhibition",0):
                    iTotalScore += dNft.get("score",0)
                    iTotalHorse += 1
            self.exbihitionCache["iTotalScore"] = iTotalScore
            self.exbihitionCache["iTotalHorse"] = iTotalHorse
            self.exbihitionDirty = False
            self.markDirty()
            self.data.save(Game.store, forced=True, no_let=True)
        return {"iTotalScore":self.exbihitionCache.get("iTotalScore",0),"iTotalHorse":self.exbihitionCache.get("iTotalHorse",0),"iCurTotalRewards":self.exbihitionCache.get("iCurTotalRewards",0)*horse_define.EXCHANGE_RATE}

    def packNftinfo(self,lHorse):
        lOwnNftData = []
        bFix = False
        for sIndex in lHorse:
            dLoad = self.nftPool.get(sIndex,{})

            #fix
            if not dLoad.get("breedMax",0):
                bFix = True
                self.fixData(dLoad)

            dHorse = {
                "name":dLoad["sRanName"],
                "iType": horse_define.HORSE_INFO[dLoad["iRandomHorseType"]]["iType"] ,
                "res_key": horse_define.HORSE_INFO[dLoad["iRandomHorseType"]]["res_key"] ,
                "id": int(sIndex) ,
                "sellStatus": dLoad["sellStatus"],
                "score": dLoad["strength"] + dLoad["speed"] + dLoad["dexterity"] + dLoad["burse"],
                "money": dLoad.get("money",11) ,
                "star": random.randint(1,5),#星星数
                "iSex": dLoad.get("iSex",1),#默认公的
                "strength": dLoad["strength"],#体力
                "MaxStrength": dLoad["MaxStrength"],
                "speed": dLoad["speed"],#速度
                "MaxSpeed": dLoad["MaxSpeed"],
                "dexterity": dLoad["dexterity"],#灵巧
                "MaxDexterity": dLoad["MaxDexterity"],
                "burse": dLoad["burse"],#爆发
                "MaxBurse": dLoad["MaxBurse"],
                "stamina": dLoad["stamina"],#耐力
                "start": dLoad["start"],#启动
                "wisdom": dLoad["wisdom"],#智慧
                "constitution": dLoad["constitution"],#体质
                "landMax":horse_define.LAND_MAX_NUM,#地形适应最大值
                "grassland": dLoad["grassland"],#草地
                "sand": dLoad["sand"],#沙地
                "mud": dLoad["mud"],#泥地
                "breedMax": dLoad["breedMax"],#繁殖次数上限
                "breed": dLoad.get("breed",0),#当前繁殖次数
                "energyMax": horse_define.ENERGY_CONFIG,#最大energy
                "energy": dLoad.get("energy",horse_define.ENERGY_CONFIG),#当前energy
                "days": (GetDayNo() - GetDayNo(dLoad["createTime"]))+1,#马匹年龄
            }
            lOwnNftData.append(dHorse)

        if bFix:
            self.markDirty()
            self.data.save(Game.store, forced=True, no_let=True)
        return lOwnNftData

    def rc_getNftInfo(self,lHorse):
        return {"lOwnNftData":self.packNftinfo(lHorse)}

    def rc_joinExhi(self,lSelectNft,lNft):
        for iIndex in lSelectNft:
            dLoad = self.nftPool.get(str(iIndex),{})
            dLoad["exhibition"] = 1

        self.markDirty()
        self.data.save(Game.store, forced=True, no_let=True)
        return {"lOwnNftData":self.packNftinfo(lNft)}

    # 制作地图
    # roleId 角色ID
    # bgConf 背景配置
    # layerConf 装饰层配置
    # 'bgConf': [1, 24, 24, 1, 2, 2, 2, 1, 1, 1, 26, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 25, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 3, 3, 1, 1, 2, 2, 2],
    # 'layerConf': [119, 0, 7, 7, 16, 21, 16, 7, 7, 0, 0, 0, 4, 4, 20, 21, 4, 21, 20, 4, 4, 0, 0, 0, 9, 9, 16, 4, 16, 9, 9, 0, 0, 6, 19, 5, 5, 11, 4, 11, 5, 5, 16, 6, 6, 19, 5, 11, 0, 4, 0, 11, 5, 16, 6, 6, 19, 5, 5, 11, 4, 11, 7, 5, 16, 6, 0, 0, 0, 4, 16, 4, 16, 4, 0, 0, 0, 0, 4, 4, 4, 12, 19, 12, 4, 4, 4, 0, 0, 20, 20, 12, 16, 19, 16, 12, 20, 20, 120]}
    def makeDiyMap(self, roleId, name, headpic, bgConf, layerConf, mapName, mapSign, isFight=0):
        mapkey = self.GeneraDiyMapTranceNo()
        now = int(time.time())
        if not self.dMapInfo.has_key(roleId):
            self.dMapInfo[roleId] = {}
            mapInfo = {
                'id':mapkey,
                'bgconf':bgConf,
                'layerconf':layerConf,
                'roleId':roleId,
                'like':0,
                'mapName':mapName,
                'mapSign': mapSign,
                'isFight':isFight, # 是否出战
                'time': now,
            }
            self.dMapInfo[roleId][mapkey] = mapInfo
            self.dMapInfoMapKey[mapkey] = mapInfo
        else:
            isFightCache = self.dMapInfo[roleId].get('isFight', 0)
            mapInfo = {
                'id':mapkey,
                'bgconf':bgConf,
                'layerconf':layerConf,
                'roleId':roleId,
                'like':0,
                'mapName': mapName,
                'mapSign': mapSign,
                'isFight': isFightCache,
                'time':now,
            }
            self.dMapInfo[roleId][mapkey] = mapInfo
            self.dMapInfoMapKey[mapkey] = mapInfo
        self.addNew(roleId, name, headpic, mapkey)
        self.markDirty()
        self.data.save(Game.store, forced=True, no_let=True)
        return {"roleId":roleId, "mapkey":mapkey}

    # 制作地图
    # roleId 角色ID
    # bgConf 背景配置
    # layerConf 装饰层配置
    # 'bgConf': [1, 24, 24, 1, 2, 2, 2, 1, 1, 1, 26, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 25, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 3, 3, 1, 1, 2, 2, 2],
    # 'layerConf': [119, 0, 7, 7, 16, 21, 16, 7, 7, 0, 0, 0, 4, 4, 20, 21, 4, 21, 20, 4, 4, 0, 0, 0, 9, 9, 16, 4, 16, 9, 9, 0, 0, 6, 19, 5, 5, 11, 4, 11, 5, 5, 16, 6, 6, 19, 5, 11, 0, 4, 0, 11, 5, 16, 6, 6, 19, 5, 5, 11, 4, 11, 7, 5, 16, 6, 0, 0, 0, 4, 16, 4, 16, 4, 0, 0, 0, 0, 4, 4, 4, 12, 19, 12, 4, 4, 4, 0, 0, 20, 20, 12, 16, 19, 16, 12, 20, 20, 120]}
    def updateMakeDiyMap(self, roleId, name, headpic, bgConf, layerConf, mapName, mapSign, mapkey):
        mapInfo = {}
        try:
            mapInfo = self.dMapInfo[roleId][mapkey]
        except:
            return self.makeDiyMap(roleId, name, headpic, bgConf, layerConf, mapName, mapSign)
        mapInfo["bgconf"]       = bgConf
        mapInfo["layerconf"]    = layerConf
        mapInfo["mapName"]      = mapName
        mapInfo["mapSign"]      = mapSign
        self.dMapInfo[roleId][mapkey] = mapInfo
        self.dMapInfoMapKey[mapkey] = mapInfo
        self.markDirty()
        return {"roleId":roleId, "mapkey":mapkey}


    def addLike(self, roleID, mapkey):

        from game.mgr.player import get_rpc_player
        who = get_rpc_player(roleID)
        if self.dMapInfo.has_key(roleID):
            print ".>>>>>>>>>>>>>>>>>>>>..", self.dMapInfo[roleID].keys(), mapkey
            if self.dMapInfo[roleID].has_key(mapkey):
                like = self.dMapInfo[roleID][mapkey].get('like',0)
                now = self.dMapInfo[roleID][mapkey].get('time',0)
                if not now:
                    now = int(time.time())
                    self.dMapInfo[roleID][mapkey]['time'] = now
                like += 1
                print "------------like",like
                self.dMapInfo[roleID][mapkey]['like'] = like
                # 添加到排行榜
                roleID = who.getUID()
                name = who.Name()
                headpic = who.getIcon()
                tInfo = [roleID, name, headpic, mapkey, like, now]
                self.insterNewRank(roleID, tInfo, mapkey)
                # ======================================================
                now = int(time.time())
                tInfo = [roleID, name, headpic, mapkey, like, now]
                self.insterMapRank(roleID, tInfo, mapkey)
                return like

        return 0

    def insterMapRank(self, rid, tUpdateInfo, mapkey, forceUpdate=False):
        for i, tInfo in enumerate(self.lmapLikeRank):
            if tInfo[0] == rid and tInfo[3] == mapkey:
                if forceUpdate:
                    self.lmapLikeRank.pop(i)
                    break
                if tUpdateInfo[4] > tInfo[4]:
                    self.lmapLikeRank.pop(i)
                    break
                return
        BinaryInsertRight(self.lmapLikeRank, tUpdateInfo, self.MapSort)
        while len(self.lmapLikeRank) > MAP_RANK_MAX:
            self.lmapLikeRank.pop()
        self.markDirty()
        pass

    def MapSort(self, a, b):
        # tInfo = [roleID, name, headpic, mapkey, like, now]
        l1 = [a[4],-1*a[5],-1*a[1]]
        l2 = [b[4],-1*b[5],-1*b[1]]
        if l1 > l2:
            return -1
        else:
            return 1

    # 最新排行榜
    def addNew(self, roleID, name, headpic, mapkey):
        print "------------------sdsdsd ::: ",roleID, name, headpic, mapkey
        if self.dMapInfo.has_key(roleID):
            if self.dMapInfo[roleID].has_key(mapkey):
                like = self.dMapInfo[roleID][mapkey].get('like',0)
                like += 1
                self.dMapInfo[roleID][mapkey]['like'] = like
                # 添加到排行榜
                now = time.time()
                tInfo = [roleID, name, headpic, mapkey, like, now]
                self.insterNewRank(roleID, tInfo, mapkey)
        pass

    # 插入最新排行榜
    def insterNewRank(self, rid, tUpdateInfo, mapkey, forceUpdate=False):
        # print "tUpdateInfo===============", tUpdateInfo
        for i, tInfo in enumerate(self.lmapNewRank):
            if tInfo[0] == rid and tInfo[3] == mapkey:
                if forceUpdate:
                    self.lmapNewRank.pop(i)
                    break
                if tUpdateInfo[5] < tInfo[5]:
                    self.lmapNewRank.pop(i)
                    break
                if tUpdateInfo[4] > tInfo[4]:
                    self.lmapNewRank.pop(i)
                    break
        BinaryInsertRight(self.lmapNewRank, tUpdateInfo, self.NewSort)
        while len(self.lmapNewRank) > MAP_RANK_MAX:
            self.lmapNewRank.pop()
        self.markDirty()
        pass

    def NewSort(self, a, b):
        # tInfo = [roleID, name, headpic, mapkey, like, now]
        l1 = [-1*a[5],-1*a[1]]
        l2 = [-1*b[5],-1*b[1]]
        if l1 > l2:
            return 1
        else:
            return -1

    # 点赞榜
    def getMapLikeRank(self):
        lrank = self.lmapLikeRank[:MAP_SHOW_RANK]
        lmapRank = []
        for tRankInfo in lrank:
            print tRankInfo
            dInfo = {} # [roleID, name, headpic, mapkey, like, now]
            # [200010001, '\xe6\x80\x9d\xe5\xbf\xb5\xe6\xb8\x90\xe6\xb5\x93', '', 1003, 1, 1573513942.426]
            rid             = tRankInfo[0]
            name            = tRankInfo[1]
            headpic         = tRankInfo[2]
            mapkey          = tRankInfo[3]
            like            = tRankInfo[4]
            if not rid in self.dMapInfo:
                continue
            if not mapkey in self.dMapInfo[rid]:
                continue
            mapInfo             = self.dMapInfo[rid].get(mapkey,{})
            bgconf              = mapInfo.get("bgconf",[])
            layerconf           = mapInfo.get("layerconf", [])
            mapName             = mapInfo.get("mapName", "")
            mapSign             = mapInfo.get("mapSign", "")
            dInfo["rid"]        = rid
            dInfo["name"]       = name
            dInfo["headpic"]    = headpic
            dInfo["mapkey"]     = mapkey
            dInfo["lBgconf"]    = bgconf
            dInfo["lLayerconf"] = layerconf
            dInfo["like"]       = like
            dInfo["mapName"]    = mapName
            dInfo["mapSign"]    = mapSign
            lmapRank.append(dInfo)
        return lmapRank

    # 最新榜
    def getNewRank(self):
        lrank = self.lmapNewRank[:MAP_SHOW_RANK]
        lmapRank = []
        for tRankInfo in lrank:
            print tRankInfo
            dInfo       = {}
            rid         = tRankInfo[0]
            name        = tRankInfo[1]
            headpic     = tRankInfo[2]
            mapkey      = tRankInfo[3]
            like        = tRankInfo[4]
            if not rid in self.dMapInfo:
                continue
            if not mapkey in self.dMapInfo[rid]:
                continue
            mapInfo             = self.dMapInfo[rid].get(mapkey,{})
            bgconf              = mapInfo.get("bgconf",[])
            layerconf           = mapInfo.get("layerconf", [])
            mapName             = mapInfo.get("mapName", "")
            mapSign             = mapInfo.get("mapSign", "")
            dInfo["rid"]        = rid
            dInfo["name"]       = name
            dInfo["headpic"]    = headpic
            dInfo["mapkey"]     = mapkey
            dInfo["lBgconf"]    = bgconf
            dInfo["lLayerconf"] = layerconf
            dInfo["like"]       = like
            dInfo["mapName"]    = mapName
            dInfo["mapSign"]    = mapSign
            lmapRank.append(dInfo)
        return lmapRank


    # 获取我的地图
    def getMyMaps(self, rid):
        allMapInfo = self.dMapInfo.get(rid, {})
        # print "------self.dMapInfo--",self.dMapInfo
        return allMapInfo

    # 设置出战地图
    def setFightMap(self, rid, mid):
        MyMaps = self.getMyMaps(rid)
        for mapId, mInfo in MyMaps.iteritems():
            if mapId == mid:
                mInfo['isFight'] = 1
            else:
                mInfo['isFight'] = 0
        self.dMapInfo[rid] = MyMaps
        return MyMaps.get(mid, {})