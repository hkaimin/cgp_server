#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webadmin.library import mongoengine_fields as f
from .base import BaseModel as Document

class Account(Document):
    """ 玩家表 """
    meta = {'collection': 'account'}

    id = f.createStringIdField()
    pid = f.makeIntField('pid', '玩家ID')
    
class Player(Document):
    """ 玩家表 """
    meta = {'collection': 'player'}

    id = f.createIdField()
    sns = f.makeIntField('sns', 'SNS类型')
    sid = f.makeStringField('sid', 'SNSID')
    name = f.makeStringField('name', '名称')
    UDID = f.makeStringField('UDID', '设备ID')
    DT = f.makeStringField('DT', '设备标记')
    MAC = f.makeStringField('MAC', 'MAC地址')
    DEV = f.makeStringField('DEV', '设备')
    VER = f.makeStringField('VER', '版本')
    tNew = f.makeStringField('tNew', '创建时间')
    tLogin = f.makeStringField('tLogin', '最后登录时间')
    tLogout = f.makeStringField('tLogout', '最后登出时间')
    coin1 = f.makeIntField('coin1', '点卷')
    coin2 = f.makeIntField('coin2', '水晶')
    vitality = f.makeIntField('vitality', '体力')
    add_vitality_time = f.makeIntField('add_vitality_time', '上一次增加体力的时间')
    total = f.makeIntField('total', '总场数')
    win = f.makeIntField('win', '胜利场数')
    exp = f.makeIntField('exp', '经验')
    vip = f.makeIntField('vip', 'VIP')
    vipCoin = f.makeIntField('vipCoin', '累计购买元宝')
    Payed = f.makeIntField('Payed', '是否已经充值过')


class PHero(Document):
    """ 玩家英雄表 """

    meta = {'collection': 'p_hero'}

    id = f.createIdField()
    h = f.makeDynamicField('h', '英雄列表')
    battle = f.makeDynamicField('battle', '出站英雄')

class PAttr(Document):
    """ 玩家属性表 """

    meta = {'collection': 'p_attr'}

    id = f.createIdField()
    hero = f.makeIntField('hero', '默认英雄')
    did = f.makeIntField('dice', '默认骰子')
    rooms = f.makeDynamicField('rooms', '场数')
    roomw = f.makeDynamicField('roomw', '连胜记录')
    key = f.makeDynamicField('key', '钥匙')
    ukey = f.makeDynamicField('ukey', '钥匙消耗')
    dtasks = f.makeDynamicField('dtasks', '任务')
    achievement = f.makeDynamicField('achievement', '成就')
    buys = f.makeDynamicField('buys', '购买')
    month = f.makeDynamicField('month', '月卡')


class PDepo(Document):
    """ 玩家寄存品表 """

    meta = {'collection': 'p_depo'}

    id = f.createIdField()
    pid = f.makeIntField('pid', '玩家ID')
    xid = f.makeStringField('xid', '物品复合ID')
    count = f.makeIntField('count', '数量')
    isNew = f.makeIntField('isNew', '新增标记')


class PDepoPack(Document):
    """ 玩家寄存包表 """

    meta = {'collection': 'p_depo_pack'}

    id = f.createIdField()
    pid = f.makeIntField('pid', '玩家ID')
    xid = f.makeStringField('xid', '物品复合ID')
    count = f.makeIntField('count', '数量')
    isNew = f.makeIntField('isNew', '新增标记')
    case = f.makeIntField('case', '宝箱类型')
    time = f.makeIntField('time', '放入时间')
    sid  = f.makeIntField('sid', '来源ID')
    sname = f.makeStringField('sname', '来源名称')


class POwned(Document):
    """ 玩家已经得到过的物品表 """

    meta = {'collection': 'p_owned'}

    id = f.createIdField()
    pid = f.makeIntField('pid', '玩家ID')
    item = f.makeIntListField('item', '物品')
    dice = f.makeIntListField('dice', '骰子')
    car = f.makeIntListField('car', '载具')
    cloth = f.makeIntListField('cloth', '服饰')


class PItem(Document):
    """ 玩家物品表 """

    meta = {'collection': 'p_item'}

    id = f.createIdField()
    pid = f.makeIntField('pid', '玩家ID')
    bid = f.makeIntField('bid', '物品ID')
    c = f.makeIntField('c', '数量')
    seat = f.makeIntField('seat', '位置')
    src = f.makeIntField('src', '来源')
    t = f.makeIntField('t', '时间')


class PDice(Document):
    """ 玩家骰子表 """

    meta = {'collection': 'p_dice'}

    id = f.createIdField()
    s = f.makeIntField('s', '背包大小')
    d = f.makeDynamicField('d', '骰子列表')

class PCar(Document):
    """ 玩家载具表 """

    meta = {'collection': 'p_car'}

    id = f.createIdField()
    s = f.makeIntField('s', '背包大小')
    d = f.makeDynamicField('d', '载具列表')
    
class PCloth(Document):
    """ 玩家服装表 """

    meta = {'collection': 'p_cloth'}

    id = f.createIdField()
    s = f.makeIntField('s', '背包大小')
    d = f.makeDynamicField('d', '服装列表')

class PCard(Document):
    """ 玩家道具卡表 """
    meta = {'collection': 'p_card'}

    id = f.createIdField()
    pid = f.makeIntField('pid', '玩家ID')
    cards = f.makeDynamicField('cards', '卡列表')
    lvs = f.makeDynamicField('card_levels', '卡等级列表')
    uses = f.makeDynamicField('uses', '累计使用次数')
    protect = f.makeDynamicField('protect', '保护状态')


class PMail(Document):
    """ 玩家邮件表 """
    meta = {'collection': 'p_mail'}

    id = f.createIdField()
    pid = f.makeIntField('pid', '玩家ID')
    type = f.makeIntField('type', '类型')
    stype = f.makeIntField('stype', '子类型')
    _save = f.makeIntField('save', '是否保留')
    time = f.makeIntField('time', '时间')
    title = f.makeStringField('title', '标题')
    content = f.makeStringField('content', '内容')
    items = f.makeDynamicField('items', '奖励')
    read = f.makeIntField('read', '已读')


class PAnnounce(Document):
    """ 玩家公告历史表 """
    meta = {'collection': 'p_announce'}

    id = f.createIdField()
    read = f.makeDynamicField('read', '已读公告')
    recv = f.makeDynamicField('recv', '已领公告')

###########公共表


class Status(Document):
    """ 服状态表 """
    meta = {'collection': 'status'}

    key = f.createKeyField()
    value = f.makeStringField('value', '值')


models = [
    Account,Player, PHero, PAttr,
    PItem, PDice, PCar, PCloth,
    PCard,
    PMail, PAnnounce,
    Status,
    # PDepo, PDepoPack, POwned,
]
