#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os, sys
from os.path import join, abspath, dirname

app='game'
serverNo = '010001' #前2位渠道编号 后四位服务器编号

platform_Mode = 1 # 平台模式 1：抽水模式

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

#log_url
log_url = "http://111.230.206.39:9000/log2"

#subgame address
base_port = 17001 #游戏服起始端口
max_subgame = 50 #最大逻辑子进程数
max_players = 20000 #单服最大在线数

logic_pool = 1 #逻辑进程保留数
logic_players = 400 #单逻辑进程达到这个数后开始新逻辑进程

xiyou_room_pool = 1 #西游房间进程保留数
xiyou_room_players = 400 #西游单房间进程人数上限

paopao_room_pool = 1 #西游房间进程保留数
paopao_room_players = 400 #西游单房间进程人数上限


#ip
# db_ip = '111.230.206.39'
db_ip = '119.91.155.74'
local_ip = '127.0.0.1'
inet_ip = local_ip #外网ip

main_addr = (local_ip, base_port)
player_addr = (local_ip, base_port + 1)
web_addr = (inet_ip, base_port + 2)
inet_addr = (inet_ip, base_port)
#逻辑进程开放给玩家的端口
start = 3
free_addrs = [(local_ip, port) for port in xrange(base_port + start, base_port + start + max_subgame)]

#算法服地址
algorithm_addr = ("127.0.0.1",9004)

#gm
GM_AESKEY = b"\x17\xBB\x50\xEA\x20\xA7\x4D\xE5\x2F\x7F\x29\x4C\x96\x7D\xE5\xA5"
gm_users = {
    "admin":"123456"
}

#store
svr_name = 'ppt'
#db_pre = 'mongodb://ppt3:123456@%s:27017' % db_ip
db_pre = 'mongodb://%s:27017' % db_ip
db_engine = '%s/%s' % (db_pre, svr_name)
db_params = {}  # dict(max_pool_size=30,)
# db_engine_log = '%s/%s_log' % (db_pre, svr_name)
db_params_log = {}  # dict(max_pool_size=10,)
# db_engine_res = '%s/%s_res' % (db_pre, svr_name)
db_params_res = {}  # dict(max_pool_size=5, pool_set_s1ize=5)
db_engine_pay = None
db_params_pay = None

# tree 的根节点, 每个区唯一, 权限最高的管理员账号密码
# root_player_account = "root_player_%s"%(serverNo)
# root_player_password = "root_pwd_%s"%(serverNo)
root_player_account = "root_player_010001"
root_player_password = "root_pwd_010001"
# root_player_code = "182b72d11LL"


# 登录时是否需要验证码
verified_code = False


#主服进程配置
frames = [
    #全局玩家管理进程及其子进程
    # {'name': 'app_gplayer_mgr', 'funcs': ['game.init_app_gplayer_mgr',], 'addr':player_addr},
    {'name': 'app_common', 'funcs': ['game.init_app_common',], 'addr':player_addr},
    {'name': 'app_logic', 'mode': 'multi', 'funcs': ['game.init_app_logic',],
        'kw': {'check': 'game.mgr.logicgame.logic_capacity_check', }},
    # {'name': 'app_common', 'funcs': ['game.init_app_common',], 'addr':player_addr},
    # 全局泡泡房间管理进程及其子进程
    {'name': 'app_paopao_room_mgr', 'funcs': ['game.init_app_paopao_room_mgr', ], 'kw': {}},
    {'name': 'app_paopao_room', 'mode': 'multi', 'funcs': ['game.init_app_paopao_room', ],
     'kw': {'check': 'game.mgr.paopao.paopaoroomgame.room_capacity_check', }},

    # {'name': 'app_xiyou_room_mgr', 'funcs': ['game.init_app_xiyou_room_mgr',], 'kw': {}},
    # {'name': 'app_xiyou_room', 'mode': 'multi', 'funcs': ['game.init_app_xiyou_room',],
    #     'kw': {'check': 'game.mgr.xiyou.xiyouroomgame.room_capacity_check', }},
    # #N叉树玩家关系管理进程
    # {'name': 'app_tree_mgr', 'funcs': ['game.init_app_tree_mgr', ], 'kw': {}},
    # #全局邮件进程
    # {'name': 'app_mail_mgr', 'funcs': ['game.init_app_mail_mgr', ], 'kw': {}},
]
