#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import web

from corelib.data import json, json_dumps
from corelib import log
from game import Game
from game.mgr.player import *
from game.define import  errcode
import game.mgr.player
import types
from game.gm.gmWebFunc import *
from game.gm.gmWebFuncNoWho import *
import config

web.config['debug'] = False #disable autoreload
app = web.auto_application()

game_url = '/api/gm'

AES = 1
if not globals().has_key("gdInstruct"):
    gdInstruct = {}

# def C2GExecGm(sCmd=None):
#     if not sCmd:
#         return
#     sCmd = sCmd.strip()  # 去掉两端的空格
#     lSection = sCmd.split()  # 指令以空格分开

_aes_encrypt = None
def aes_encrypt(data):
    global _aes_encrypt
    if _aes_encrypt is None:
        from corelib.aes import new_aes_encrypt
        key = config.GM_AESKEY
        if key is not None:
            _aes_encrypt = new_aes_encrypt(key)
        else:
            log.warn('*****client AES key no found!')
            return data
    return _aes_encrypt(data)

def encode_json(data):
    """ 加密数据 """
    data = json_dumps(data)
    if not AES:
        return data
    return aes_encrypt(str(data))


class WebGmFuncNormal(app.page):
    """ 处理GM协议
    http://172.16.40.2:8008/api/game/WebGmFunc?cmd=1&rid=399367642
    http://127.0.0.1:17003/api/gm/WebGmFuncNormal?cmd=wx_login&code=0239bKWf2AhBGH0YpLZf2mDFWf29bKWv
    http://119.23.108.126:17003/api/gm/WebGmFuncNormal?cmd=wx_login&code=0239bKWf2AhBGH0YpLZf2mDFWf29bKWv
    """
    path = '%s/%s' % (game_url, 'WebGmFuncNormal')

    def GET(self):
        data = web.input(_method='GET')
        cmd = data.get('cmd', "")
        if not (cmd):
            return ''
        return self.exec_protocol(cmd, data)

    # GM处理协议
    def exec_protocol(self, cmd,  data):
        return ExecWebGmFuncNoWho(cmd, data)


    def packBack(self,data,success,err):
        res = {}
        if success:
            res["success"] = 1
            res["err"] = 0
            res["data"] = data
        else:
            res["success"] = 0
            res["err"] = err
            res["data"] = data
        return json.dumps(res)







# ================ 带账号密码验证的，用户或后台发起GM请求 ===================
def _wrap_permissions(func):
    def _func(*args, **kw):
        try:
            data = web.input(_method='GET')
            user, password = data.get('user'), data.get('password')
            if not user or not password:
                return
            # if config.gm_users.get(user) != password:
            #     return
            return func(*args, **kw)
        except:
            log.log_except()
        return ''
    return _func

class WebGmFunc(app.page):
    """ 处理GM协议
    http://118.89.55.39:8008/api/gm/WebGmFunc?user="gm"&password=1&cmd=setRealName&rid=6537010001&name=sss
    http://127.0.0.1:8003/api/gm/WebGmFunc?user=%22gm%22&password=1&cmd=setName&rid=6537010001&name=sss
    http://172.16.40.2:8008/api/game/WebGmFunc?cmd=1&rid=399367642
    http://127.0.0.1:8003/api/gm/WebGmFunc?user=%gm&password=1&cmd=GM_setAgentBeget&rid=6537010001&Beget=0.1
    """
    path = '%s/%s' % (game_url, 'WebGmFunc')

    @_wrap_permissions
    def GET(self):
        data = web.input(_method='GET')
        cmd, rid = data.get('cmd', ""), int(data.get('rid', 0))
        if not (cmd and rid):
            return ''
        return self.exec_protocol(cmd, rid, data)

    # GM处理协议
    def exec_protocol(self, cmd, rid, data):
        # who = get_rpc_    player(rid) # 获取存储模型

        # who = game.mgr.player.get_rpc_player(int(rid))# 获取对象
        who = get_rpc_player(int(rid))
        # print '--------------packBack---who', who
        if not who:
            rs = {'err':errcode.EC_EXEC_WEBGM_RID_ERROR}
            return json.dumps(rs)
        return ExecWebGmFunc(who, cmd, data)


    def packBack(self,data,success,err):
        res = {}
        if success:
            res["success"] = 1
            res["err"] = 0
            res["data"] = data
        else:
            res["success"] = 0
            res["err"] = err
            res["data"] = data
        return json.dumps(res)


class UserPlayers(app.page):
    """ 获取玩家列表
    http://172.16.40.2:8008/api/game/userPlayers?sns=1&sid=399367642
    """
    path = '%s/%s' % (game_url, 'userPlayers')

    @_wrap_permissions
    def GET(self):
        data = web.input(_method='GET')
        sns, sid = int(data.get('sns', 0)), data.get('sid')
        if not (sns and sid):
            return ''
        return sns, sid

# 游戏监控(json):
# 1、游戏服状态监控(cpu_scene, cpu_glog, cpu_activity,
#    cpu_union, cpu_store=store进程cpu使用量;
# max_logics=最大逻辑进程数; logics=逻辑进程数; user=当前在线用户数; max_user=允许最大用户数);
class ServerStats(app.page):
    """ 服务器运行信息
    """
    path = '%s/%s' % (game_url, 'serverstats')
    prefix = 'cpu_'

    @_wrap_permissions
    def GET(self):
        ret_val = {}
        logics = Game.rpc_logic_game.count
        max_logics = config.max_players / config.logic_players
        user = Game.rpc_player_mgr.get_count()
        max_user = config.max_players
        ret_val.update({'logics': logics, 'max_logics': max_logics,
                        'user': user, 'max_user': max_user})

        return json.dumps(ret_val)

inited = 0
def init_app():
    global inited
    if inited:
        return
    inited = 1
    #游戏功能子进程,自己初始化sns

    log.info('app mapping:\n%s', '\n'.join(map(str, app.mapping)))


def get_wsgi_app(*middleware):
    init_app()
    return app.wsgifunc(*middleware)



