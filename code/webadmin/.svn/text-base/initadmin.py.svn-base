#!/usr/bin/env python
# -*- coding: utf-8 -*-


def db_init(app):
    connection = app.extensions['mongoengine'].connection
    db_name = app.config['MONGODB_SETTINGS']['db']
    db_cfg = app.config['MONGODB_SETTINGS']
    db = connection[db_name]
    if db_cfg.get('username'):
        db.authenticate(db_cfg['username'], db_cfg['password'])

    user_tb = db['user']
    if user_tb.find().count() > 0:
        return
    #init
    print("****begin web admin init db*****")
    user_tb.insert({
          "_id" : 1,
          "groups" : [],
          "name" : "admin",
          "password" : "123456"
    })

    group_tb = db['group']
    group_tb.insert([
        {
          "_id" : 2,
          "note" : "修改和修改用户组的权限",
          "name" : "管理员",
          "permissions" : ["admin_control", "*"]
        },
        {
          "_id" : 1,
          "name" : "研发",
          "note" : "研发团队的权限",
          "permissions" : ["/dev/", "resource_model_read", "resource_model_write", "/res/", "/user/",
                           "release_version", "simulate_fight", "cache_control", "mapeditor", "reward_test",
                           "statistic", "clone_database", "/ope/", "mail_test", "ctrl_svr", "statistic_rpc"]
        }
    ])


def init_admin(app):
    db_init(app)
