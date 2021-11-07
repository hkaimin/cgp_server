#!/usr/bin/env python
# -*- coding:utf-8 -*-

from corelib.frame import Game, MSG_FRAME_START

from game.common.gateway import GateWayMgr
from game.define import msg_define, store_define
from game.mgr.res import ResMgr


def public_init():
    """ 初始化rpc功能模块  """
    from game.common.db import new_game_store
    store = new_game_store()
    Game.store = store

    #日志
    from game.mgr.logger import GameLogger
    Game.glog = GameLogger()
    from game.mgr.logger import createLogErrorHandler
    createLogErrorHandler()
    from game.mgr.timer import Timer
    Game.timer = Timer()
    #资源
    Game.res_mgr = ResMgr()
    Game.res_mgr.load()

def init_app_common():
    public_init()
    #注册开始消息
    Game.sub(MSG_FRAME_START, start_common)
    # 初始化rpc功能模块
    import game.mgr.player
    rpc_player_mgr = game.mgr.player.GPlayerMgr()
    # 服务器信息
    import game.mgr.server
    rpc_server_info = game.mgr.server.ServerInfo()

    # # 竞技场
    # import game.mgr.waitroom
    # rpc_wait_mgr = game.mgr.waitroom.CWaitRoomMng()


    #排行榜信息
    import game.core.rank.rankMgr
    rpc_rank_info = game.core.rank.rankMgr.RankInfo()

    #DIY地图信息
    import game.core.diyMap.diymapMgr
    rpc_diymap_info = game.core.diyMap.diymapMgr.DiyMapInfo()
    return rpc_player_mgr, rpc_server_info, rpc_rank_info, rpc_diymap_info


def start_common():
    Game.unsub(MSG_FRAME_START, start_common)
    #gateway
    Game.gateway = GateWayMgr(Game.rpc_player_mgr)
    Game.app.register(Game.gateway)

    Game.rpc_player_mgr.start()
    Game.rpc_server_info.start()
    Game.rpc_rank_info.start()
    Game.rpc_diymap_info.start()
    Game.timer.start()



#-------------- app_logic --------------------
def init_app_logic():
    #注册开始消息
    Game.sub(MSG_FRAME_START, start_logic)
    #初始化rpc功能模块
    import game.mgr.logicgame #import LogicGame
    Game.logic_game = game.mgr.logicgame.LogicGame()
    #玩家管理器
    # from game.mgr.player import SubPlayerMgr
    import game.mgr.player
    Game.player_mgr = game.mgr.player.SubPlayerMgr()
    Game.logic_game.stop_mgrs.append(Game.player_mgr)

    return Game.logic_game, Game.player_mgr


def start_logic():
    Game.unsub(MSG_FRAME_START, start_logic)
    public_init()
    #gateway
    Game.gateway = GateWayMgr(Game.player_mgr)
    Game.app.register(Game.gateway)
    Game.logic_game.start()
    Game.timer.start()

#-------------- app_logic end --------------------



#-------------- app_paopao_room_mgr --------------------
def init_app_paopao_room_mgr():
    #注册开始消息
    Game.sub(MSG_FRAME_START, start_paopao_room_mgr)
    #全局房间管理
    # from game.mgr.paopao.paopaoroom import GPaopaoRoomMgr
    import game.mgr.paopao.paopaoroom
    rpc_paopao_room_mgr = game.mgr.paopao.paopaoroom.GPaopaoRoomMgr()

    return rpc_paopao_room_mgr

def start_paopao_room_mgr():
    Game.unsub(MSG_FRAME_START, start_paopao_room_mgr)

    public_init()


#-------------- app_paopao_room_mgr end --------------------

#-------------- app_paopao_room --------------------
def init_app_paopao_room():
    #注册开始消息
    Game.sub(MSG_FRAME_START, start_paopao_room)
    #初始化rpc功能模块
    # from game.mgr.paopao.paopaoroomgame import PaopaoRoomGame
    import game.mgr.paopao.paopaoroomgame
    Game.paopao_room_game = game.mgr.paopao.paopaoroomgame.PaopaoRoomGame()
    #子房间管理器
    # from game.mgr.paopao.paopaoroom import SubPaopaoRoomMgr
    import game.mgr.paopao.paopaoroom
    Game.paopao_room_mgr = game.mgr.paopao.paopaoroom.SubPaopaoRoomMgr()
    Game.paopao_room_game.stop_mgrs.append(Game.paopao_room_mgr)

    return Game.paopao_room_game, Game.paopao_room_mgr


def start_paopao_room():
    Game.unsub(MSG_FRAME_START, start_paopao_room)
    public_init()
    Game.gateway = GateWayMgr(Game.paopao_room_mgr)
    Game.app.register(Game.gateway)
    Game.paopao_room_game.start()

#-------------- app_paopao_room end -----------------------













#-------------------------------------------------------------------------------



