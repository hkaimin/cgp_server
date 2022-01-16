#!/usr/bin/env python
# -*- coding:utf-8 -*-

from game.define import errcode, constant
from game import Game

from corelib import log

# 地图协议
class mapProtocal(object):
    if 0:
        from game.core import player as player_md
        player = player_md.Player()

    #请求打开DIY地图 UI
    def rc_openDiyMapUI(self, theme):
        rs = self.player.rc_openDiyMapUI(theme)
        return 1, rs

    #切换主题
    def rc_changeTheme(self, theme):
        rs = self.player.rc_changeTheme(theme)
        return 1, rs

    # 保存地图， 按战斗下发的形式上传
    # lBgConf: 地图层
    # lLayerConf: 障碍层
    # mapName 地图名字
    # mapSign 地图签名
    # mapkey # 地图ID，如果第一次保存，就传0；
    def rc_saveMap(self, lBgConf, lLayerConf, mapName, mapSign, mapkey):
        rs = self.player.rc_saveMap(lBgConf, lLayerConf, mapName, mapSign, mapkey)
        return 1, rs

    # 点赞
    def rc_addLike(self,rid, mapKey, iType):
        rs = self.player.rc_addLike(rid, mapKey, iType)
        return 1, rs

    # 获取排行榜(最热)
    def rc_getHopRank(self):
        rs = self.player.rc_getHopRank()
        return 1, rs

    # 获取排行榜(最新)
    def rc_getNewRank(self):
        rs = self.player.rc_getNewRank()
        return 1, rs

    # 获取我的地图
    def rc_getMyMaps(self):
        rs = self.player.rc_getMyMaps()
        return 1, rs

    # 获取nftMarket
    def rc_getNftMarket(self):
        rs = self.player.rc_getNftMarket()
        return 1, rs

    # sell nft
    def rc_SellNft(self,nftIndex):
        rs = self.player.rc_SellNft(nftIndex)
        return 1, rs

    # 设置出战地图
    def rc_setFightMap(self, mapId):
        rs = self.player.rc_setFightMap(mapId)
        return 1, rs