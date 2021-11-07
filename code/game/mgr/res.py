#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import os
import config

from corelib import log
from UserDict import UserDict
# from game.res.ResSkill import ResSkill
# from game.res.ResFishType import ResFishType
# from game.res.ResFishScene import ResFishScene
# from game.res.ResFishMove import ResFishMove
# from game.res.ResFishFormation import ResFishFormation
# from game.res.ResCaishenType import ResCaishenType
# from game.res.ResCaishenLine import ResCaishenLine
# from game.res.ResGunType import ResGunType

from game.res.ResMapBase import ResMapBase
from game.res.ResMapConf import ResMapConf
from game.res.ResItemData import ResItemData
from game.res.UpgradeData import ResUpgradeData
from game.res.ShopData import ResShopData
from game.res.GameConfData import GameConfData
from game.res.NameData import NameData
from game.res.BtnConfData import BtnConfData
import game.res.MiniGameData
import game.res.SevenDayRewardData
import game.res.WujinMapConf
import game.res.RoleData
import game.res.guildData
import game.res.openCtrlData
import game.res.SkillData
import game.res.HelpData
import game.res.MapSignData

class MinGameType():
    HIT_TYPE_TARGET = 1
    WIN_TYPE_TARGET = 2


class ResDict(UserDict):
    def __init__(self, name, *args, **kwargs):
        UserDict.__init__(self, *args, **kwargs)
        self.name = name

    def get(self, key, default=None):
        val = UserDict.get(self, key, failobj=default)
        if not val:
            log.info("%s not find %s", self.name, key)
        return val

class ResMgr(object):
    def __init__(self):
        self.res_mapBase = {} # 地图砖块表
        self.res_mapConf = {} # 地图配置表
        self.res_itemData = {} # 物品表
        self.res_upgrade = {} # 升级表
        self.res_name = {} # 随机名字表
        self.res_name_data = {} # id 对应 名字
        self.dMapBaseTheme = {}
        self.res_shopData = {} # 商品数据
        self.res_lShopDataByType = {}
        self.res_minigameData = {} # 小游戏数据
        self.minGameHit2Obj = {} # 点击次数对应对象
        self.minGameWin2Obj = {} # 赢的目标对应对象
        self.res_gameConfData = {} # 游戏配置
        self.res_sevenDayReward = {} # 七日奖励
        self.res_sevenDayCycleData = {} # 七日奖励期号信息
        self.res_wujinInstData = {} # 无尽模式
        self.res_wujinInstLevelData = {} # 无尽模式等级
        self.res_roleData = {} # 角色系统
        self.res_btnData = {}
        self.dPvpMapData = {}
        self.dTrainData = {}
        self.res_guildData = {}
        self.dGuideForKey = {}
        self.res_openCtrlData = {}
        self.res_skillDataConf = {}
        self.res_skillDataLv = {}
        self.res_helpData = {}
        self.res_mapSignData = {}



    def parse(self, load_dict, cls, res_dict, keyType=int, prepareFunc=None):
        resData = load_dict.get(cls.RES_TABLE, {})
        for key, oneData in resData.iteritems():
            try:
                resobj = cls()
                resobj.load_from_json(oneData)
                if str(key).isdigit():
                    res_dict[keyType(key)] = resobj
                else:
                    res_dict[key] = resobj
            except Exception, resErr:
                log.log_except('res_load_err:%s, %s, %s', resErr, key, oneData)
        if prepareFunc:
            prepareFunc()


    def load(self):
        res_file = "res.json"
        res_path = os.path.join(config.res_path, res_file)
        # print "res_path:", res_path
        with open(res_path, 'r') as load_f:
            load_dict = json.load(load_f)

        self.parse(load_dict, ResMapBase, self.res_mapBase,prepareFunc=self.init_ai_name)  #
        self.parse(load_dict, ResMapConf, self.res_mapConf, prepareFunc=self.inti_pvpMapConf)  #
        self.parse(load_dict, ResItemData, self.res_itemData)  # 物品表
        self.parse(load_dict, ResUpgradeData, self.res_upgrade)  # 升级表
        self.parse(load_dict, NameData, self.res_name)  # 名字表
        self.parse(load_dict, ResShopData, self.res_shopData,prepareFunc=self.inti_shopRes)  # 商品表
        self.parse(load_dict, game.res.MiniGameData.ResMiniGameData, self.res_minigameData,prepareFunc=self.inti_minigameData)  # 小游戏数据
        self.parse(load_dict, GameConfData, self.res_gameConfData)  # 游戏配置
        self.parse(load_dict, game.res.SevenDayRewardData.SevenDayRewardData, self.res_sevenDayReward, prepareFunc=self.inti_sevenDayReward)  # 七日奖励
        self.parse(load_dict, game.res.WujinMapConf.WujinMapConf, self.res_wujinInstData, prepareFunc=self.inti_wujinInstData)  # 无尽模式
        self.parse(load_dict, game.res.RoleData.ResRoleData, self.res_roleData)  # 角色系统
        self.parse(load_dict, game.res.BtnConfData.BtnConfData, self.res_btnData)  # 游戏配置
        self.parse(load_dict, game.res.guildData.GuildData, self.res_guildData, prepareFunc=self.inti_guideData)  # 引导配置
        self.parse(load_dict, game.res.guildData.GuildData, self.res_guildData, prepareFunc=self.inti_guideData)  # 引导配置
        self.parse(load_dict, game.res.openCtrlData.OpenCtrlData, self.res_openCtrlData)  # 引导配置
        self.parse(load_dict, game.res.SkillData.ResSkillData, self.res_skillDataConf, prepareFunc=self.init_skill)  # 引导配置
        self.parse(load_dict, game.res.HelpData.HelpData, self.res_helpData)  # 帮助表
        self.parse(load_dict, game.res.MapSignData.MapSignData, self.res_mapSignData)  # 地图签名

        # print "------------------"
        # print self.res_mapSignData
        # print "------------------"

    # res_helpData
        pass

    def loadByNames(self, names=[]):
        res_file = "res.json"
        res_path = os.path.join(config.res_path, res_file)
        # print "res_path:", res_path
        with open(res_path, 'r') as load_f:
            load_dict = json.load(load_f)
        if not names or ResMapBase.RES_TABLE in names:
            self.parse(load_dict, ResMapBase, self.res_mapBase,prepareFunc=self.init_ai_name)  #
        if not names or ResMapConf.RES_TABLE in names:
            self.parse(load_dict, ResMapConf, self.res_mapConf, prepareFunc=self.inti_pvpMapConf)  #
        if not names or ResItemData.RES_TABLE in names:
            self.parse(load_dict, ResItemData, self.res_itemData)  # 物品表
        if not names or ResUpgradeData.RES_TABLE in names:
            self.parse(load_dict, ResUpgradeData, self.res_upgrade)  # 升级表
        if not names or NameData.RES_TABLE in names:
            self.parse(load_dict, NameData, self.res_name)  # 名字表
        if not names or ResShopData.RES_TABLE in names:
            self.parse(load_dict, ResShopData, self.res_shopData,prepareFunc=self.inti_shopRes)  # 商品表
        if not names or game.res.MiniGameData.ResMiniGameData.RES_TABLE in names:
            self.parse(load_dict, game.res.MiniGameData.ResMiniGameData, self.res_minigameData,prepareFunc=self.inti_minigameData)  # 小游戏数据
        if not names or GameConfData.RES_TABLE in names:
            self.parse(load_dict, GameConfData, self.res_gameConfData)  # 游戏配置
        if not names or game.res.SevenDayRewardData.SevenDayRewardData.RES_TABLE in names:
            self.parse(load_dict, game.res.SevenDayRewardData.SevenDayRewardData, self.res_sevenDayReward, prepareFunc=self.inti_sevenDayReward)  # 七日奖励
        if not names or game.res.WujinMapConf.WujinMapConf.RES_TABLE in names:
            self.parse(load_dict, game.res.WujinMapConf.WujinMapConf, self.res_wujinInstData, prepareFunc=self.inti_wujinInstData)  # 无尽模式
        if not names or game.res.WujinMapConf.WujinMapConf.RES_TABLE in names:
            self.parse(load_dict, game.res.WujinMapConf.WujinMapConf, self.res_roleData)  # 角色系统
        if not names or game.res.BtnConfData.BtnConfData.RES_TABLE in names:
            self.parse(load_dict, game.res.BtnConfData.BtnConfData, self.res_btnData)  # 游戏配置
        if not names or game.res.guildData.GuildData.RES_TABLE in names:
            self.parse(load_dict, game.res.guildData.GuildData, self.res_guildData, prepareFunc=self.inti_guideData)  # 引导配置
        if not names or game.res.openCtrlData.OpenCtrlData.RES_TABLE in names:
            self.parse(load_dict, game.res.openCtrlData.OpenCtrlData, self.res_openCtrlData)  # 引导配置
        if not names or game.res.SkillData.ResSkillData.RES_TABLE in names:
            self.parse(load_dict, game.res.SkillData.ResSkillData, self.res_skillDataConf, prepareFunc=self.init_skill)  # 引导配置
        if not names or game.res.HelpData.HelpData.RES_TABLE in names:
            self.parse(load_dict, game.res.HelpData.HelpData, self.res_helpData)  # 帮助表
        if not names or game.res.MapSignData.MapSignData.RES_TABLE in names:
            self.parse(load_dict, game.res.MapSignData.MapSignData, self.res_mapSignData)  # 地图签名




    def init_skill(self):
        self.res_skillDataLv = {}
        for ID, oSkillData in self.res_skillDataConf.iteritems():
            skillID = oSkillData.skillID
            lv = oSkillData.lv
            # print skillID, lv
            if not self.res_skillDataLv.has_key(skillID):
                self.res_skillDataLv[skillID] = {}
            self.res_skillDataLv[skillID][lv] = oSkillData
        # import pprint
        # pprint.pprint(self.res_skillDataLv)

    def inti_guideData(self):
        for guideID, guideObj in self.res_guildData.iteritems():
            key = guideObj.ikey
            istep = guideObj.istep
            if not self.dGuideForKey.has_key(key):
                self.dGuideForKey[key] = {}
            self.dGuideForKey[key][istep] = guideObj
        # print "----------------------:",self.dGuideForKey
        pass

    # 初始化地图信息
    def inti_pvpMapConf(self):
        for id, mapData in self.res_mapConf.iteritems():
            if mapData.Type == 2:
                self.dPvpMapData[id] = mapData
            elif mapData.Type == 3:
                self.dTrainData[id] = mapData

    def init_ai_name(self):
        pass

    # 初始化基础地图
    # dMapBaseTheme= {
    #    theme:{itype:[]}
    # }
    def init_mapBase(self):
        for mapBaseObj in self.res_mapBase.itervalues():
            itheme = mapBaseObj.itheme
            itype = mapBaseObj.itype
            if not self.dMapBaseTheme.has_key(itheme):
                self.dMapBaseTheme[itheme] = {}
                self.dMapBaseTheme[itheme][itype] = [mapBaseObj.id]
                if not self.dMapBaseTheme[itheme].get('name',""):
                    self.dMapBaseTheme[itheme]['name'] = mapBaseObj.themeName
            else:
                if not self.dMapBaseTheme[itheme].has_key(itype):
                    self.dMapBaseTheme[itheme][itype] = [mapBaseObj.id]
                else:
                    self.dMapBaseTheme[itheme][itype].append(mapBaseObj.id)
                if not self.dMapBaseTheme[itheme].get('name', ""):
                    self.dMapBaseTheme[itheme]['name'] = mapBaseObj.themeName


    #
    def inti_shopRes(self):
        for id, shopBaseObj in self.res_shopData.iteritems():
            if not shopBaseObj:
                continue
            shopType = shopBaseObj.iType
            if not self.res_lShopDataByType.has_key(shopType):
                self.res_lShopDataByType[shopType] = [shopBaseObj]
            else:
                self.res_lShopDataByType[shopType].append(shopBaseObj)

    # 初始化小游戏目标表
    def inti_minigameData(self):
        self.minGameHit2Obj = {}
        self.minGameWin2Obj = {}
        for id ,minGameTargetObj in self.res_minigameData.iteritems():
            finishType = minGameTargetObj.finishType
            hitcount = minGameTargetObj.hitcount
            if finishType == MinGameType.HIT_TYPE_TARGET:
                self.minGameHit2Obj[hitcount] = minGameTargetObj
            if finishType == MinGameType.WIN_TYPE_TARGET:
                self.minGameWin2Obj[MinGameType.WIN_TYPE_TARGET] = minGameTargetObj


    def inti_sevenDayReward(self):
        self.res_sevenDayCycleData = {}
        for id, sevenDayRewardObj in self.res_sevenDayReward.iteritems():
            cycle = sevenDayRewardObj.cycle
            day = sevenDayRewardObj.day
            if not self.res_sevenDayCycleData.has_key(cycle):
                self.res_sevenDayCycleData[cycle] = {day:sevenDayRewardObj}
            else:
                self.res_sevenDayCycleData[cycle][day] = sevenDayRewardObj
        pass

    def inti_wujinInstData(self):
        lbarrNo = self.res_wujinInstData.keys()
        lbarrNo.sort()
        for barrNo in lbarrNo:
            barrObj = self.res_wujinInstData.get(barrNo)
            if not barrObj:
                continue
            idiffLevel = barrObj.diffLevel
            # print barrNo,idiffLevel
            if not self.res_wujinInstLevelData.has_key(idiffLevel):
                self.res_wujinInstLevelData[idiffLevel] = []
            self.res_wujinInstLevelData[idiffLevel].append(barrObj)
        pass