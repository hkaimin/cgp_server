#!/usr/bin/env python
# -*- coding:utf-8 -*-

from game.define import errcode, constant
from game import Game

from corelib import log

# 西游协议
class xiyouProtocal(object):
    if 0:
        from game.core import player as player_md
        player = player_md.Player()

    # 进入西游，直接拉进房间
    def rc_enterXiyou(self, roleId):
        err, rs = self.player.rc_enterXYRoom()
        return err, rs

    # 西游压分 {u'itemId': 1, u'roleId': 6537010001L, u'itemPut': 100, u'roomId': 2}
    def rc_putScore(self, roleId, roomId, itemId, itemPut):
        err, rs = self.player.rc_putScore(roleId, roomId, itemId, itemPut)
        return err, rs

    # 退出房间
    def rc_exitRoom(self):
        err, rs = self.player.rc_exitRoom()
        return err, rs









