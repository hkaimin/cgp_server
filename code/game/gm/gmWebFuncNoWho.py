#!/usr/bin/env python
# -*- coding:utf-8 -*-

from corelib import spawn
from game.gm import *
# app.frame.reload_modules(["game.player.player", "game.player.bag"])

lPath = ["game.gm.gmWebFuncNoWho",]


# 执行后台GM指令接口总入口
# 不带who
def ExecWebGmFuncNoWho(cmd, data):
    print 111111111111111111111112,"cmd",cmd,data
    func = None
    for sPath in lPath:
        mod = __import__(sPath)
        lPart=sPath.split('.')
        for sPart in lPart[1:]:
            mod=getattr(mod,sPart)
            print mod
        if hasattr(mod, cmd):
            func = getattr(mod, cmd)
            if func:
                break
    if func:
        return func(data)
    else:
        return "Error: not exists gm function:%s !!"%cmd
    pass

# 回包统一封装
def packBack(data,success,err="0"):
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

# 微信登录，openID请求，
# http://127.0.0.1:17003/api/gm/WebGmFuncNormal?cmd=wx_login&code=0239bKWf2AhBGH0YpLZf2mDFWf29bKWv
def wx_login(data):
    code = data.get('code',"")
    if not code:
        return packBack({},0,"not code")
    import urllib2
    try:
        data = {
                # "appid":"wx11adc66e301668c0",
                # "secret":"0a16cd00dab8deb4c42dc8fb4ad7c8a9",
                "appid":"wxa398adcebcb30f11",
                "secret":"ea7e02995c65eec80f006c0a591de274",
                "js_code":code,
                "grant_type":"authorization_code"
            }
        header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
        url = "https://api.weixin.qq.com/sns/jscode2session?"
        req = urllib2.Request(url + urllib.urlencode(data),headers=header_dict)
        res = urllib2.urlopen(req,timeout=5)
        res = res.read()
        return packBack(res, 1)
    except:
        return packBack({}, 0, "request timeout!")


# http://127.0.0.1:17003/api/gm/WebGmFuncNormal?cmd=ov_login&token=0239bKWf2AhBGH0YpLZf2mDFWf29bKWv
def ov_login(data):
    token = data.get('token',"")
    if not token:
        return packBack({},0,"not token")
    import urllib2
    try:
        # appKey（接入前开发者平台申请的appKey）
        # appSecret（接入前开发者平台申请的appSecret）
        # nonce（随机数）
        # pkgName（游戏包名）
        # timestamp（时间戳，毫秒，取当前时间值）
        # token（登录接口获得的token）
        appKey = "9e93bbd6b95a838da5d27be482a29188"
        appSecret = "3a0b27a87dbe66a87091bae669955633"
        nonce = random.randint(1000000000000000, 9999999999999999)
        pkgName = "com.yq.ppdzz.vivominigame"
        timestamp = int(time.time())*1000
        _token = token
        _code = "appKey=%s&appSecret=%s&nonce=%s&pkgName=%s&timestamp=%s&token=%s"%(appKey,appSecret,nonce,pkgName,timestamp,_token)
        s = hashlib.sha256()
        s.update(_code)
        b = s.hexdigest()
        signature = b
        url = "https://quickgame.vivo.com.cn/api/quickgame/cp/account/userInfo?" + _code + "&signature=%s"%signature
        print "------------------------>> url", url, timestamp
        header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
        req = urllib2.Request(url ,headers=header_dict)
        res = urllib2.urlopen(req,timeout=5)
        res = res.read()
        return packBack(res, 1)

        # data = {
        #         # "appid":"wx11adc66e301668c0",
        #         # "secret":"0a16cd00dab8deb4c42dc8fb4ad7c8a9",
        #         "appid":"wxa398adcebcb30f11",
        #         "secret":"ea7e02995c65eec80f006c0a591de274",
        #         "js_code":code,
        #         "grant_type":"authorization_code"
        #     }
        # header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        #            "Content-Type": "application/json"}
        # url = "https://api.weixin.qq.com/sns/jscode2session?"
        # req = urllib2.Request(url + urllib.urlencode(data),headers=header_dict)
        # res = urllib2.urlopen(req,timeout=5)
        # res = res.read()
        # return packBack(res, 1)
    except:
        return packBack({}, 0, "request timeout!")
    pass

import config
import types
from game.define import  errcode
from corelib.data import json, json_dumps
import urllib2
import json
import time
import urllib
import random
import hashlib