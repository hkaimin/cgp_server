#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os, sys
from os.path import join, abspath, dirname

app='part'
part_name = 'part1'
serverNo = '010001' #前2位渠道编号 后四位服务器编号  part部件服必须保持和主服一致

debug = 1  # 1, 2(内部调试)

#编码
sys_setting = sys.modules['SysSetting']
sys_encoding = sys_setting.sys_encoding

#路径设置
root_path = sys_setting.root_path
res_base_dir = join(root_path, 'res')
locale_code = 'zh_CN'
#配置文件所在目录,linux系统下用于存放配置、sock等文件
cfg_path = dirname(__file__)
#cmd
py_params = ' subgame %(name)s %(pid)s "%(addr)s"'
executable = sys_setting.executable
sub_game_cmd = executable + py_params


#subgame address
base_port = 19001 #游戏服起始端口
max_subgame = 50 #最大逻辑子进程数
max_players = 20000 #单服最大在线数
logic_players = 400 #单逻辑进程达到这个数后开始新逻辑进程
logic_pool = 1 #逻辑进程保留数
room_pool = 1 #房间进程保留数
room_players = 400 #单房间进程人数上限

#ip
db_ip = '193.112.128.112'
local_ip = '127.0.0.1'
inet_ip = local_ip #外网ip

#主节点的地址
main_addr = ('127.0.0.1', 18001)
inet_addr = (inet_ip, base_port)
#逻辑进程开放给玩家的端口
start = 3
free_addrs = [(local_ip, port) for port in xrange(base_port + start, base_port + start + max_subgame)]


#store
svr_name = 'djxy%s'%serverNo
db_pre = 'mongodb://djxy:djxy123@%s:27017' % db_ip
db_engine = '%s/%s' % (db_pre, svr_name)
db_params = {}  # dict(max_pool_size=30,)


#主服进程配置
frames = [
    # {'name': 'app_glog', 'funcs': ['game.init_app_glog',], 'kw': {}},
    # {'name': 'app_gplayer_mgr', 'funcs': ['game.init_app_gplayer_mgr',], 'addr':player_addr},
    # {'name': 'app_room_mgr', 'funcs': ['game.init_app_room_mgr',], 'kw': {}},
    {'name': 'app_logic', 'mode': 'multi', 'funcs': ['game.init_app_logic',],
        'kw': {'check': 'game.mgr.logicgame.logic_capacity_check', }},
    {'name': 'app_room', 'mode': 'multi', 'funcs': ['game.init_app_room',],
        'kw': {'check': 'game.mgr.roomgame.room_capacity_check', }},
]

