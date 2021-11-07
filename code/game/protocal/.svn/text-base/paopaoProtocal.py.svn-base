#!/usr/bin/env python
# -*- coding:utf-8 -*-

from game.define import errcode, constant
from game import Game

from corelib import log

# 西游协议
class paopaoProtocal(object):
    if 0:
        from game.core import player as player_md
        player = player_md.Player()

    # 进入泡泡，直接拉进房间
    def rc_enterPPRoom(self):
        # err, rs = self.player.rc_enterPPRoom()
        err, rs = self.player.rc_EnterWait(self.player)
        return err, rs

    # 离开泡泡房间,取消匹配exitPPRoom
    def rc_exitPPRoom(self):
        # err, rs = self.player.rc_enterPPRoom()
        err, rs = self.player.rc_ExitWait(self.player)
        return err, rs


    # # 西游压分 {u'itemId': 1, u'roleId': 6537010001L, u'itemPut': 100, u'roomId': 2}
    # def rc_putScore(self, roleId, roomId, itemId, itemPut):
    #     err, rs = self.player.rc_putScore(roleId, roomId, itemId, itemPut)
    #     return err, rs

    # 退出房间
    def rc_exitPPRoom(self):
        err, rs = self.player.rc_exitPPRoom(self.player)
        return err, rs

    def rc_syncPos(self, x, y, direction, speed, idx,playerID=0):
        # print "------------------------"
        err, rs = self.player.rc_syncPos(self.player, x, y, direction, speed, idx, playerID=playerID)
        return err, rs

    def rc_syncPut(self, x, y, idx,playerID=0):
        print "------->>>>x, y, idx,playerID:",x, y, idx,playerID
        err, rs = self.player.rc_syncPut(self.player, x, y, idx, playerID=playerID)
        return err, rs

    def rc_syncBoomPlayer(self, paopaoID, x, y, idx, killrid, killidx,playerID=0):
        err, rs = self.player.rc_syncBoomPlayer(self.player, paopaoID, x, y, idx, killrid, killidx, playerID=playerID)
        return err, rs

    def rc_syncBoomZhuan(self, paopaoID, x, y, idx,  breakidx,playerID=0):
        err, rs = self.player.rc_syncBoomZhuan(self.player, paopaoID, x, y, idx, breakidx, playerID=playerID)
        return err, rs

    def rc_pickItem(self, itype, idx,playerID=0):
        print "-=---------rc_pickItem", itype, idx
        err, rs = self.player.rc_pickItem(self.player, itype, idx, playerID=playerID)
        return err, rs

    # 开房（随机地图）
    def rc_open1V1Room(self):
        print "-0-----rc_open1V1Room"
        err, rs = self.player.open1V1Room()
        return err, rs

    # 开房（DIY地图）
    def rc_open1V1RoomByMap(self, mapID):
        print "-0-----rc_open1V1RoomByMap"
        err, rs = self.player.open1V1RoomByMap(mapID)
        return err, rs

    # 进入好友邀请房间
    def rc_enter1V1Room(self, fightRoomKey):
        err, rs = self.player.enter1V1Room(fightRoomKey)
        return err, rs

    # 点击准备
    def rc_setReady1V1(self, fightRoomKey):
        #print 111111111111111,fightRoomKey
        err, rs = self.player.setReady1V1(fightRoomKey)
        return err, rs

    # 点击开始游戏
    def rc_startGame1V1(self, fightRoomKey):
       # print 111111111111111222,fightRoomKey
        err, rs = self.player.startGame1V1(fightRoomKey)
        return err, rs

    # 离开1V1房间(房主点击退出)
    def rc_remove1V1Room(self):
        err, rs = self.player.remove1V1Room()
        return err, rs

    # 点击离开房间(非房主点击退出)
    def rc_leaveGame1v1(self, fightRoomKey):
        err, rs = self.player.leaveGame1v1(fightRoomKey)
        return err, rs


