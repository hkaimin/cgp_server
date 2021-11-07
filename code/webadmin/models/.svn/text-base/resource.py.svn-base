#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: fdm=marker

from webadmin.library import mongoengine_fields as f

from .base import BaseModel as Document

# 基础系统 {{{1
#=============================================================================
class Hero(Document):
    """ 英雄表 """

    meta = {'collection': 'hero'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    act = f.makeStringField('act', '动画')
    hero = f.makeIntField('hero', '英雄')
    level = f.makeIntField('level', '英雄等级')
    exp = f.makeIntField('exp', '等级经验')
    rid = f.makeIntField('rid', '等级对应奖励')
    sex = f.makeIntField('sex', '性别')
    # coin1 = f.makeIntField('coin1', '购买金币花费')
    # coin2 = f.makeIntField('coin2', '购买水晶花费')
    # upCoin1 = f.makeIntField('upCoin1', '升级金币花费')
    # upCoin2 = f.makeIntField('upCoin2', '升级水晶花费')
    # materials = f.makeStringField('materials', '升级材料')
    # unlock = f.makeDynamicField('unlock', '解锁条件')
    TN = f.makeIntField('TN', '体能')
    YZ = f.makeIntField('YZ', '意志')
    XYA = f.makeIntField('XYA', '信仰')
    XYO = f.makeIntField('XYO', '信用')
    CZ = f.makeIntField('CZ', '才智')
    HH = f.makeIntField('HH', '厚黑')


class HeroInfo(Document):
    """ 英雄信息表 """
    meta = {'collection': 'hero_info'}
    id = f.createIdField()  # 英雄类型
    name = f.makeStringField('name', '名字')
    pinyin = f.makeStringField('pinyin', '拼音')
    info = f.makeTextField('info', '简介')
    cards = f.makeIntListField('cards', '默认卡组')
    high = f.makeIntField('high', '高度')
    priceType = f.makeIntField('priceType','购买方式')
    price =  f.makeIntField('price','价格')
    story =  f.makeTextField('story','角色故事')
    phrase = f.makeTextField('phrase','口头禅')
    home   = f.makeTextField('home','主场') 
    is_show   = f.makeIntField('is_show','是否显示在角色选择界面') 
    voice = f.makeIntListField('voice', '出场语音')


class Reward(Document):
    """ 奖励表 """

    meta = {'collection': 'reward'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '说明')
    useid = f.makeIntField('useid', '消耗品ID')
    useNum = f.makeIntField('useNum', '消耗数量')
    reward = f.makeDynamicField('reward', '奖励')


class Attr(Document):
    """ 属性配置表 """

    meta = {'collection': 'attr'}

    id = f.createIdField()
    info = f.makeTextField('info', '说明')
    TN = f.makeStringField('TN', '体能')
    YZ = f.makeStringField('YZ', '意志')
    XYA = f.makeStringField('XYA', '信仰')
    XYO = f.makeStringField('XYO', '信用')
    CZ = f.makeStringField('CZ', '才智')
    HH = f.makeStringField('HH', '厚黑')
    sk1 = f.makeStringField('sk1', '技能1ID')
    skv1 = f.makeStringField('skv1', '技能1值')
    sk2 = f.makeStringField('sk2', '技能2ID')
    skv2 = f.makeStringField('skv2', '技能2值')
    sk3 = f.makeStringField('sk3', '技能3ID')
    skv3 = f.makeStringField('skv3', '技能3值')


class HeroSkill(Document):
    """ 英雄技能表 """

    meta = {'collection': 'hero_skill'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    act = f.makeStringField('act', '动画')
    quality = f.makeIntField('quality', '品质')
    attrType = f.makeIntField('attrType', '属性类型')
    funcType = f.makeStringField('funcType', '功能类型')
    dataType = f.makeIntField('dataType', '数值类型')
    trAis = f.makeIntListField('trAis', '触发ai列表') #具体效果
    ai = f.makeIntField('ai', '激活AI') #技能客户端表现
    values = f.makeDynamicField('values', '数值列表')
    rc = f.makeIntField('rc', '触发条件AI') #技能生效条件

class Skill(Document):
    """ 英雄技能表 """

    meta = {'collection': 'skill'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    stype = f.makeStringField('stype', '类别')
    use = f.makeStringField('use', '作用')
    lv = f.makeIntField('lv', '等级')
    desc = f.makeStringField('desc', '技能描述')
    battle_desc = f.makeStringField('battle_desc', '场内技能描述')
    ai_condition = f.makeIntField('ai_condition', '额外条件AI')
    ai_effect = f.makeDynamicField('ai_effect', '效果AI列表')

    x = f.makeIntField('x', 'x坐标')
    y = f.makeIntField('y', 'y坐标')
    is_arr = f.makeIntField('is_arr', '是否显示箭头')
    next_skill = f.makeIntField('next_skill', '下一技能ID')

    attr_type = f.makeIntField('attr_type', '属性类型')
    act = f.makeIntField('act', '技能特效动画')
    value1 = f.makeDynamicField('value1', "数值1")
    value2 = f.makeDynamicField('value2', "数值2")
    value3 = f.makeDynamicField('value3', "数值3")
    value4 = f.makeDynamicField('value4', "数值4")
    max_lv = f.makeDynamicField('max_lv', "角色最大等级列表")
    battle_count = f.makeDynamicField('battle_count', "游戏场次列表")
    pre_skill1 = f.makeDynamicField("pre_skill1", "前置技能1")
    lv_list1 = f.makeDynamicField('lv_list1', "等级列表1")
    pre_skill2 = f.makeDynamicField("pre_skill2", "前置技能2")
    lv_list2 = f.makeDynamicField('lv_list2', "等级列表2")
    point_list = f.makeDynamicField('point_list', "天赋点列表")
    cost_type_list = f.makeDynamicField('cost_type_list', "升级消耗类型列表")
    cost_value_list = f.makeDynamicField('cost_value_list', "升级消耗数值列表")

class SkillResetCost(Document):
    """ 英雄技能重置消耗 """

    meta = {'collection': 'skill_reset_cost'}
    id = f.createIdField()
    count = f.makeIntField('count', '次数')
    coin2 = f.makeIntField('coin2', '扣除幸运星')

class RankRefreshCost(Document):
    """ 排行界面刷新消耗 """

    meta = {'collection': 'rank_refresh_cost'}
    id = f.createIdField()
    count = f.makeIntField('count', '次数')
    type = f.makeIntField('type', '货币类型')
    amount = f.makeIntField('amount', '扣除数量')

class CheckIn(Document):

    """ 签到表 """

    meta = {'collection': 'checkin'}
    id = f.createIdField()
    lv = f.makeIntField('lv', '级别')

    item_type = f.makeIntField('item_type', '内容类型')
    item_id = f.makeIntField('item_id', '内容id')
    item_amount = f.makeIntField('item_amount', '内容数量')

    item_type2 = f.makeIntField('item_type2', '内容类型')
    item_id2 = f.makeIntField('item_id2', '内容id')
    item_amount2 = f.makeIntField('item_amount2', '内容数量')

class DailyTask(Document):

    """ 日常任务表 """

    meta = {'collection': 'daily_task'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeStringField('info', '简介')
    kind = f.makeIntField('kind', '所属级别')

    active_reward = f.makeIntField('active_reward', '活跃值奖励')
    coin1_reward = f.makeIntField('coin1_reward', '金币奖励')
    star_reward = f.makeIntField('star_reward', '星星奖励')

    type = f.makeIntField('type', '任务类型')
    count = f.makeIntField("count", "个数或次数")
    item = f.makeIntField('item', '道具id')
    item_type = f.makeIntField('item_type', '物品种类')
    hero = f.makeIntField('hero', '角色id')

    mode = f.makeIntField('mode', '模式id')
    modelv = f.makeIntField('modelv', '模式难度或者区域编号')
    modenode = f.makeIntField('modenode', '模式节点')
    iswin = f.makeIntField('iswin', '是否获胜')

    lv = f.makeIntField('lv', '等级')
    checkin = f.makeIntField('checkin', '签到格')

class DailyTaskEgg(Document):
    
    """ 日常任务彩蛋奖励表 """

    meta = {'collection': 'daily_task_egg'}

    id = f.createIdField()
    kind = f.makeIntField('kind', '所属级别')
    egg_id = f.makeStringField('egg_id', '礼包id')
    name = f.makeStringField('name', '礼包显示名')
    desc = f.makeStringField('desc', '描述')
    active = f.makeIntField('active', '活跃值需求')


    type = f.makeIntField('type', '类型')
    c_amount = f.makeIntField('c_amount', '配置个数')
    r_amount = f.makeIntField('r_amount', '奖励个数')
    random_time = f.makeIntField('random_time', '随机次数')
    random_id = f.makeIntField('random_id', '随机极限目标序号')

    item_type1 = f.makeIntField('item_type1', '道具类型1')
    item_id1 = f.makeIntField('item_id1', '道具id1')
    item_amount1 = f.makeIntField('item_amount1', '个数1')
    item_ratio1 = f.makeIntField('item_ratio1', '几率1')

    item_type2 = f.makeIntField('item_type2', '道具类型2')
    item_id2 = f.makeIntField('item_id2', '道具id2')
    item_amount2 = f.makeIntField('item_amount2', '个数2')
    item_ratio2 = f.makeIntField('item_ratio2', '几率2')

    item_type3 = f.makeIntField('item_type3', '道具类型3')
    item_id3 = f.makeIntField('item_id3', '道具id3')
    item_amount3 = f.makeIntField('item_amount3', '个数3')
    item_ratio3 = f.makeIntField('item_ratio3', '几率3')

    item_type4 = f.makeIntField('item_type4', '道具类型4')
    item_id4 = f.makeIntField('item_id4', '道具id4')
    item_amount4 = f.makeIntField('item_amount4', '个数4')
    item_ratio4 = f.makeIntField('item_ratio4', '几率4')

    item_type5 = f.makeIntField('item_type5', '道具类型5')
    item_id5 = f.makeIntField('item_id5', '道具id5')
    item_amount5 = f.makeIntField('item_amount5', '个数5')
    item_ratio5 = f.makeIntField('item_ratio5', '几率5')

    item_type6 = f.makeIntField('item_type6', '道具类型6')
    item_id6 = f.makeIntField('item_id6', '道具id6')
    item_amount6 = f.makeIntField('item_amount6', '个数6')
    item_ratio6 = f.makeIntField('item_ratio6', '几率6')

    item_type7 = f.makeIntField('item_type7', '道具类型7')
    item_id7 = f.makeIntField('item_id7', '道具id7')
    item_amount7 = f.makeIntField('item_amount7', '个数7')
    item_ratio7 = f.makeIntField('item_ratio7', '几率7')

    item_type8 = f.makeIntField('item_type8', '道具类型8')
    item_id8 = f.makeIntField('item_id8', '道具id8')
    item_amount8 = f.makeIntField('item_amount8', '个数8')
    item_ratio8 = f.makeIntField('item_ratio8', '几率8')

    item_type9 = f.makeIntField('item_type9', '道具类型9')
    item_id9 = f.makeIntField('item_id9', '道具id9')
    item_amount9 = f.makeIntField('item_amount9', '个数9')
    item_ratio9 = f.makeIntField('item_ratio9', '几率9')

    item_type10 = f.makeIntField('item_type10', '道具类型10')
    item_id10 = f.makeIntField('item_id10', '道具id10')
    item_amount10 = f.makeIntField('item_amount10', '个数10')
    item_ratio10 = f.makeIntField('item_ratio10', '几率10')

class BattleEgg(Document):
    
    """ 战斗彩蛋奖励表 """

    meta = {'collection': 'battle_egg'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    desc = f.makeStringField('desc', '描述')
    type = f.makeIntField('type', '类型')
    c_amount = f.makeIntField('c_amount', '配置个数')
    r_amount = f.makeIntField('r_amount', '奖励个数')
    random_time = f.makeIntField('random_time', '随机次数')
    random_id = f.makeIntField('random_id', '随机极限目标序号')
    
    item_type1 = f.makeIntField('item_type1', '道具类型1')
    item_id1 = f.makeIntField('item_id1', '道具id1')
    item_amount1 = f.makeIntField('item_amount1', '个数1')
    item_ratio1 = f.makeIntField('item_ratio1', '几率1')

    item_type2 = f.makeIntField('item_type2', '道具类型2')
    item_id2 = f.makeIntField('item_id2', '道具id2')
    item_amount2 = f.makeIntField('item_amount2', '个数2')
    item_ratio2 = f.makeIntField('item_ratio2', '几率2')

    item_type3 = f.makeIntField('item_type3', '道具类型3')
    item_id3 = f.makeIntField('item_id3', '道具id3')
    item_amount3 = f.makeIntField('item_amount3', '个数3')
    item_ratio3 = f.makeIntField('item_ratio3', '几率3')

    item_type4 = f.makeIntField('item_type4', '道具类型4')
    item_id4 = f.makeIntField('item_id4', '道具id4')
    item_amount4 = f.makeIntField('item_amount4', '个数4')
    item_ratio4 = f.makeIntField('item_ratio4', '几率4')

    item_type5 = f.makeIntField('item_type5', '道具类型5')
    item_id5 = f.makeIntField('item_id5', '道具id5')
    item_amount5 = f.makeIntField('item_amount5', '个数5')
    item_ratio5 = f.makeIntField('item_ratio5', '几率5')

    item_type6 = f.makeIntField('item_type6', '道具类型6')
    item_id6 = f.makeIntField('item_id6', '道具id6')
    item_amount6 = f.makeIntField('item_amount6', '个数6')
    item_ratio6 = f.makeIntField('item_ratio6', '几率6')

    item_type7 = f.makeIntField('item_type7', '道具类型7')
    item_id7 = f.makeIntField('item_id7', '道具id7')
    item_amount7 = f.makeIntField('item_amount7', '个数7')
    item_ratio7 = f.makeIntField('item_ratio7', '几率7')

    item_type8 = f.makeIntField('item_type8', '道具类型8')
    item_id8 = f.makeIntField('item_id8', '道具id8')
    item_amount8 = f.makeIntField('item_amount8', '个数8')
    item_ratio8 = f.makeIntField('item_ratio8', '几率8')

    item_type9 = f.makeIntField('item_type9', '道具类型9')
    item_id9 = f.makeIntField('item_id9', '道具id9')
    item_amount9 = f.makeIntField('item_amount9', '个数9')
    item_ratio9 = f.makeIntField('item_ratio9', '几率9')

    item_type10 = f.makeIntField('item_type10', '道具类型10')
    item_id10 = f.makeIntField('item_id10', '道具id10')
    item_amount10 = f.makeIntField('item_amount10', '个数10')
    item_ratio10 = f.makeIntField('item_ratio10', '几率10')

class GiftPackage(Document):
    
    """ 礼包表 """

    meta = {'collection': 'gift_package'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    desc = f.makeStringField('desc', '描述')

    type = f.makeIntField('type', '类型')
    icon = f.makeIntField("icon", "图标")
    c_amount = f.makeIntField('c_amount', '配置个数')
    r_amount = f.makeIntField('r_amount', '奖励个数')
    random_time = f.makeIntField('random_time', '随机次数')
    random_id = f.makeIntField('random_id', '随机极限目标序号')
    
    item_type1 = f.makeIntField('item_type1', '道具类型1')
    item_id1 = f.makeIntField('item_id1', '道具id1')
    item_amount1 = f.makeIntField('item_amount1', '个数1')
    item_ratio1 = f.makeIntField('item_ratio1', '几率1')

    item_type2 = f.makeIntField('item_type2', '道具类型2')
    item_id2 = f.makeIntField('item_id2', '道具id2')
    item_amount2 = f.makeIntField('item_amount2', '个数2')
    item_ratio2 = f.makeIntField('item_ratio2', '几率2')

    item_type3 = f.makeIntField('item_type3', '道具类型3')
    item_id3 = f.makeIntField('item_id3', '道具id3')
    item_amount3 = f.makeIntField('item_amount3', '个数3')
    item_ratio3 = f.makeIntField('item_ratio3', '几率3')

    item_type4 = f.makeIntField('item_type4', '道具类型4')
    item_id4 = f.makeIntField('item_id4', '道具id4')
    item_amount4 = f.makeIntField('item_amount4', '个数4')
    item_ratio4 = f.makeIntField('item_ratio4', '几率4')

    item_type5 = f.makeIntField('item_type5', '道具类型5')
    item_id5 = f.makeIntField('item_id5', '道具id5')
    item_amount5 = f.makeIntField('item_amount5', '个数5')
    item_ratio5 = f.makeIntField('item_ratio5', '几率5')

    item_type6 = f.makeIntField('item_type6', '道具类型6')
    item_id6 = f.makeIntField('item_id6', '道具id6')
    item_amount6 = f.makeIntField('item_amount6', '个数6')
    item_ratio6 = f.makeIntField('item_ratio6', '几率6')

    item_type7 = f.makeIntField('item_type7', '道具类型7')
    item_id7 = f.makeIntField('item_id7', '道具id7')
    item_amount7 = f.makeIntField('item_amount7', '个数7')
    item_ratio7 = f.makeIntField('item_ratio7', '几率7')

    item_type8 = f.makeIntField('item_type8', '道具类型8')
    item_id8 = f.makeIntField('item_id8', '道具id8')
    item_amount8 = f.makeIntField('item_amount8', '个数8')
    item_ratio8 = f.makeIntField('item_ratio8', '几率8')

    item_type9 = f.makeIntField('item_type9', '道具类型9')
    item_id9 = f.makeIntField('item_id9', '道具id9')
    item_amount9 = f.makeIntField('item_amount9', '个数9')
    item_ratio9 = f.makeIntField('item_ratio9', '几率9')

    item_type10 = f.makeIntField('item_type10', '道具类型10')
    item_id10 = f.makeIntField('item_id10', '道具id10')
    item_amount10 = f.makeIntField('item_amount10', '个数10')
    item_ratio10 = f.makeIntField('item_ratio10', '几率10')

class CheckinExtraReward(Document):
    
    """ 礼包表 """

    meta = {'collection': 'checkin_extra_reward'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    desc = f.makeStringField('desc', '描述')

    type = f.makeIntField('type', '类型')
    icon = f.makeIntField("icon", "图标")
    c_amount = f.makeIntField('c_amount', '配置个数')
    r_amount = f.makeIntField('r_amount', '奖励个数')
    random_time = f.makeIntField('random_time', '随机次数')
    random_id = f.makeIntField('random_id', '随机极限目标序号')
    
    item_type1 = f.makeIntField('item_type1', '道具类型1')
    item_id1 = f.makeIntField('item_id1', '道具id1')
    item_amount1 = f.makeIntField('item_amount1', '个数1')
    item_ratio1 = f.makeIntField('item_ratio1', '几率1')

    item_type2 = f.makeIntField('item_type2', '道具类型2')
    item_id2 = f.makeIntField('item_id2', '道具id2')
    item_amount2 = f.makeIntField('item_amount2', '个数2')
    item_ratio2 = f.makeIntField('item_ratio2', '几率2')

    item_type3 = f.makeIntField('item_type3', '道具类型3')
    item_id3 = f.makeIntField('item_id3', '道具id3')
    item_amount3 = f.makeIntField('item_amount3', '个数3')
    item_ratio3 = f.makeIntField('item_ratio3', '几率3')

    item_type4 = f.makeIntField('item_type4', '道具类型4')
    item_id4 = f.makeIntField('item_id4', '道具id4')
    item_amount4 = f.makeIntField('item_amount4', '个数4')
    item_ratio4 = f.makeIntField('item_ratio4', '几率4')

    item_type5 = f.makeIntField('item_type5', '道具类型5')
    item_id5 = f.makeIntField('item_id5', '道具id5')
    item_amount5 = f.makeIntField('item_amount5', '个数5')
    item_ratio5 = f.makeIntField('item_ratio5', '几率5')

    item_type6 = f.makeIntField('item_type6', '道具类型6')
    item_id6 = f.makeIntField('item_id6', '道具id6')
    item_amount6 = f.makeIntField('item_amount6', '个数6')
    item_ratio6 = f.makeIntField('item_ratio6', '几率6')

    item_type7 = f.makeIntField('item_type7', '道具类型7')
    item_id7 = f.makeIntField('item_id7', '道具id7')
    item_amount7 = f.makeIntField('item_amount7', '个数7')
    item_ratio7 = f.makeIntField('item_ratio7', '几率7')

    item_type8 = f.makeIntField('item_type8', '道具类型8')
    item_id8 = f.makeIntField('item_id8', '道具id8')
    item_amount8 = f.makeIntField('item_amount8', '个数8')
    item_ratio8 = f.makeIntField('item_ratio8', '几率8')

    item_type9 = f.makeIntField('item_type9', '道具类型9')
    item_id9 = f.makeIntField('item_id9', '道具id9')
    item_amount9 = f.makeIntField('item_amount9', '个数9')
    item_ratio9 = f.makeIntField('item_ratio9', '几率9')

    item_type10 = f.makeIntField('item_type10', '道具类型10')
    item_id10 = f.makeIntField('item_id10', '道具id10')
    item_amount10 = f.makeIntField('item_amount10', '个数10')
    item_ratio10 = f.makeIntField('item_ratio10', '几率10')

# 房间系统 {{{1
#=============================================================================
class RankBattle(Document):

    """ 排行挑战 """

    meta = {'collection': 'rankbattle'}

    id = f.createIdField()
    name = f.makeStringField('name', '名字')
    map_ids = f.makeDynamicField("map_ids", "地图id列表")
    room_cash = f.makeIntField("room_cash", "起始资金")
    max_star = f.makeIntField("max_star", "最高能量")
    credit_coin = f.makeIntField("credit_coin", "贷款费用")
    battle_egg = f.makeIntField("battle_egg", "彩蛋奖励")

    winrule  = f.makeIntListField("winrule", "额外胜利条件")
    winarg  = f.makeIntListField("winarg", "额外胜利参数")

class PvpRoomMode(Document):
    """ PVP房间模式表 """

    meta = {'collection': 'pvpmode'}

    id = f.createIdField()



    pvpid = f.makeIntField("pvpid", "模式id")
    order = f.makeIntField("order", "排序顺序")
    room_rate = f.makeIntField("room_rate", "翻倍系数")
    aid = f.makeIntField("aid", "活动id")
    mode_type = f.makeIntField("mode_type", "模式类型")
    no_skill = f.makeIntField("no_skill", "屏蔽技能")
    icon = f.makeIntField("icon", "图标ic")
    name = f.makeStringField('name', '难度名')
    map_ids = f.makeDynamicField("map_ids", "地图id列表")
    room_cash = f.makeIntField("room_cash", "起始资金")
    max_star = f.makeIntField("max_star", "最高能量")
    credit_coin = f.makeIntField("credit_coin", "贷款费用")
    has_robot = f.makeDynamicField("has_robot", "机器人")


    grade_limit2 = f.makeIntField("grade_limit2", "有限次数进入等级")
    min_enter_amount = f.makeIntField("min_enter_amount", "进入次数限制（试玩，每日）")
    grade_limit = f.makeIntField("grade_limit", "无限次数进入等级")

    enter_amount_grade = f.makeIntField("enter_amount_grade", "开始胜率判断等级")
    enter_amount_limit = f.makeIntField("enter_amount_limit", "游戏场数")
    ratio = f.makeIntField("ratio", "胜率（%）")


    vip_limit = f.makeIntField("vip_limit", "VIP等级")
    zichan_limit = f.makeIntField("zichan_limit", "金币资产")
    coin2_limit = f.makeIntField("coin2_limit", "幸运星资产")

    begin_time = f.makeIntField("begin_time", "开始时间")
    end_time = f.makeIntField("end_time", "结束时间")
    need_sign = f.makeIntField("need_sign", "需要报名")

    cost_type = f.makeIntField('cost_type', '进场费用类型')
    cost_amount = f.makeIntField('cost_amount', '进程费用')

    reward_type = f.makeIntField('reward_type', '最高奖励类型')
    reward_amount = f.makeIntField('reward_amount', '最高奖励单人数额')
    talent  = f.makeIntField('talent', '天赋点奖励')
    vitality_cost = f.makeIntField('vitality_cost', '体力消耗')

    exp_reward = f.makeIntField('exp_reward', '奖励经验基线')
    cash_base = f.makeIntField('cash_base', '计算经验资产基线')
    exp_min_percent = f.makeFloatField('exp_min_percent', '经验比例下限')
    exp_max_percent = f.makeFloatField('exp_max_percent', '经验比例上限')

    have_score = f.makeIntField("have_score", "可获得积分开关（0,1）")
    can_invite = f.makeIntField("can_invite", "是否可以邀请")
    can_private = f.makeIntField("can_private", "是否可以私人")
    can_giveup = f.makeIntField("can_giveup", "是否可以认输")
    fixed_team_amount = f.makeIntField("fixed_team_amount", "固定玩家人数")

    battle_egg = f.makeIntField("battle_egg", "彩蛋奖励")

    winrule  = f.makeIntListField("winrule", "额外胜利条件")
    winarg  = f.makeIntListField("winarg", "额外胜利参数")

class Npc(Document):
    """ NPC表 """

    meta = {'collection': 'npc'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    act = f.makeIntField('act', '动画')
    talk = f.makeIntField('talk', '附身话')
    type = f.makeIntField('type', '类型')
    kind = f.makeIntField('kind', '性质')
    round = f.makeIntField('round', '出现回合间隔')
    step = f.makeIntField('step', '持续格子数')
    car = f.makeIntField('car', '与载具关系')
    initai = f.makeIntListField('initais', '出场AI列表')
    ais = f.makeIntListField('ais', 'AI列表')
    oais = f.makeIntListField('oais', '别人AI列表')


class Card(Document):
    """ 道具卡表 """
    meta = {'collection': 'card'}
    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    act = f.makeStringField('act', '动画')
    type = f.makeIntField('type', '类型')
    effect = f.makeIntField('effect', '效果类型')
    status = f.makeIntField('status', '状态')
    nature = f.makeIntField('nature', '性质')
    gold = f.makeIntField('gold', '是否金卡')
    cost = f.makeIntField('cost', '房间消耗')
    cash = f.makeIntField('cash', '现金')
    coin1 = f.makeIntField('coin1', '点卷')
    coin2 = f.makeIntField('coin2', '幸运星')
    sellCoin1 = f.makeIntField('sellCoin1', '出售点卷')
    hero = f.makeIntField('hero', '专属英雄')
    lock = f.makeDynamicField('lock', '解锁')
    passive = f.makeDynamicField('passive', '被动触发')
    card_target = f.makeIntField('card_target', '用卡对象配置')
    target = f.makeIntField('target', '目标')
    cond = f.makeDynamicField('cond', '目标条件')
    select = f.makeIntField('select', '是否选择')
    ai = f.makeIntField('ai', 'AI')
    upgrade = f.makeDynamicField('upgrade', '升级条件')

    star = f.makeIntField("star", "星级")
    piece_lv = f.makeIntField("piece_lv", "碎片级别")
    piece_amount = f.makeIntField("piece_amount", "碎片数量")

class CardPiece(Document):
    """ 卡片碎片表 """
    meta = {'collection': 'cardpiece'}
    id = f.createIdField()

    compose_amount = f.makeIntField("compose_amount", "合成数量")
    compose_cost_type = f.makeIntField("compose_cost_type", "合成消耗类型")
    compose_cost_amount = f.makeIntField("compose_cost_amount", "合成消耗数量")

    decompose_amount = f.makeIntField("decompose_amount", "分解数量")
    decompose_cost_type = f.makeIntField("decompose_cost_type", "分解消耗类型")
    decompose_cost_amount = f.makeIntField("decompose_cost_amount", "分解消耗数量")

class Talk(Document):
    """ 对话表 """

    meta = {'collection': 'talk'}

    id = f.createIdField()
    act = f.makeStringField('act', '动画')
    type = f.makeIntField('type', '类型')
    hero = f.makeIntListField('hero', '专属英雄')
    tType = f.makeIntField('tType', '对话类型')
    voice = f.makeIntField('voice', '语音')
    talk = f.makeTextField('talk', '对话')
    talkTime = f.makeIntField('talkTime', '对话时长')


class Fate(Document):
    """ 命运表 """

    meta = {'collection': 'fate'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '显示信息')
    t = f.makeIntField('t', '类型')
    tInfo = f.makeStringField('tInfo', '类型信息')
    tRate = f.makeStringField('tRate', '类型出现概率')
    rate = f.makeStringField('rate', '出现概率')
    ai = f.makeIntField('ai', 'AI')
    rc = f.makeIntField('rc', '执行条件AI')
    guide = f.makeIntField('guide', '引导时屏蔽')
    is_good = f.makeIntField('is_good', '是否有利')


class News(Document):
    """ 新闻表 """

    meta = {'collection': 'news'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '新闻事件')
    t = f.makeIntField('t', '类型')
    tInfo = f.makeStringField('tInfo', '类型信息')
    tRate = f.makeStringField('tRate', '类型出现概率')
    rate = f.makeStringField('rate', '出现概率')
    ai = f.makeIntField('ai', 'AI')
    rc = f.makeIntField('rc', '执行条件AI')
    guide = f.makeIntField('guide', '引导时屏蔽')
    is_good = f.makeIntField('is_good', '是否有利')


class Market(Document):
    """ 消费 """

    meta = {'collection': 'market'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '消费原因')
    t = f.makeIntField('t', '类型')
    tInfo = f.makeStringField('tInfo', '类型信息')
    rate = f.makeStringField('rate', '出现概率')
    ai = f.makeIntField('ai', 'AI')
    guide = f.makeIntField('guide', '引导时屏蔽')


class Robot(Document):
    """ 机器人配置 """
    meta = {'collection': 'robot'}

    id = f.createIdField()
    hLevel = f.makeIntField('hLevel', '最低英雄等级')
    cloths = f.makeIntListField('cloths', '服装列表')
    dices = f.makeIntListField('dices', '骰子列表')
    cars = f.makeIntListField('cars', '载具列表')
    cards = f.makeDynamicField('cards', '道具卡')
    skills = f.makeDynamicField('skills', '技能')
    heroExc = f.makeIntListField('heroExc', '不允许的英雄类型')
    ailv = f.makeIntField('ailv', 'AI等级')

# 地图系统 {{{1
#=============================================================================
class MapModel(Document):
    """ 地图模式表 """

    meta = {'collection': 'map_model'}

    id = f.createIdField()
    mids = f.makeIntListField('mids', '地图ID列表')
    tmids = f.makeIntListField('tmids', '测试地图ID列表')
    # model = f.makeIntField('model', '模式')
    mode = f.makeIntField('mode', '地图模式')
    level = f.makeIntField('level', '地图难度等级')
    reward = f.makeStringField('reward', '奖励')
    miniGame = f.makeIntListField('miniGame', '小游戏列表')
    coin1 = f.makeIntField('coin1', '金币花费')
    coin2 = f.makeIntField('coin2', '水晶花费')
    cash = f.makeIntField('cash', '初始现金')


class Map(Document):
    """ 地图表 """

    meta = {'collection': 'map'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    act = f.makeStringField('act', '动画')
    unlock = f.makeDynamicField('unlock', '解锁条件')
    back = f.makeStringField('back', '地图背景')
    mapSize = f.makePointField('mapSize', '地图大小')
    tileSize = f.makePointField('tileSize', '格子大小')
    startPos = f.makeIntListField('startPos', '起始ID列表')
    miniGame = f.makeIntListField('miniGame', '小游戏列表')
    time = f.makeIntField('time', '游戏时间')
    actRes = f.makeStringField('actRes', '资源包名称')
    npcs = f.makeStringField('npcs', 'NPCID列表')
    # props = f.makeIntListField('props', '道具ID列表')
    cards = f.makeIntListField('cards', '道具卡ID列表')
    cash = f.makeIntField('cash', '初始现金')
    miniMap = f.makeDynamicField('miniMap', '地图缩放比例')

class Tile(Document):
    """ 地格表 """

    meta = {'collection': 'tile'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    act = f.makeStringField('act', '动画')
    mid = f.makeIntField('mid', '地图ID')
    pos = f.makePointField('pos', '位置')
    tid = f.makeIntField('tid', '序号')
    area = f.makeIntField('area', '所属地域')
    street = f.makeIntField('street', '所属街')
    route = f.makeDynamicField('route', '路由表')
    bid = f.makeIntField('bid', '建筑物')
    price = f.makeIntField('price', '基础地价')
    mark = f.makeStringField('mark', '地标建筑动画')
    owner = f.makeIntField('owner', '初始主人')
    car = f.makeIntField('car', '赛车场车型')

class Building(Document):
    """ 建筑表 """

    meta = {'collection': 'building'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    act = f.makeStringField('act', '动画')
    type = f.makeIntField('type', '建筑物类型')
    stype = f.makeIntField('stype', '子类型')
    level = f.makeIntField('level', '建筑物等级')
    logic = f.makeIntListField('logic', 'AI列表')

# AI系统 {{{1
#=============================================================================
class Ai(Document):
    """ [AI系统]AI """

    meta = {'collection': 'ai'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    lid = f.makeIntField('lid', '逻辑ID')
    event = f.makeStringField('event', '触发事件名')
    param = f.makeTextField('param', '参数')


class AiCode(Document):
    """ [AI系统]代码 """

    meta = {'collection': 'ai_code'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    code = f.makeTextField('code', '代码')


class Buff(Document):
    """ [AI系统]Buff表 """

    meta = {'collection': 'buff'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    status = f.makeIntField('status', '状态列表')
    event = f.makeStringField('event', '生命周期事件')
    ai = f.makeIntField('ai', '作用AI')
    re_ai = f.makeIntField('re_ai', '反作用AI')
    tr_ai = f.makeIntField('tr_ai', '触发AI')

    used = f.makeIntField('used', '是否已经使用过')
class ExchangeCode(Document):
    """ 兑换表 """
    meta = {'collection': 'exchangecode',}

    #id = f.createIdField()
    id = f.createStringIdField()
    batchName = f.makeStringField('batchName', '批次名')
    createTime = f.makeTimeField('createTime', '创建批次时间')
    endTime = f.makeTimeField('endTime', '结束时间')
    roleIsOnce = f.makeIntField('roleIsOnce', '一个角色是否只能领取一次')
    rewardId = f.makeIntField('rewardId', '奖励ID')
    useCount = f.makeIntField('useCount', '可用次数')
    #exchCode = f.makeStringField('exchCode', '兑换码')

class ActivityTask(Document):
    """ 活动任务表 """
    meta = {'collection': 'activity_task'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    kind = f.makeIntField('kind', '子活动类型')
    gui = f.makeIntField('gui', '界面类型')
    info = f.makeTextField('info', '简介')
    ui = f.makeIntField('ui', '跳转ID')
    task_kind = f.makeIntField('task_kind', '任务类型')
    lv = f.makeIntField('lv', '级别')
    item_kind = f.makeIntField('item_kind', '物品种类')
    item_id = f.makeIntField('item_id', '物品ID')
    qual = f.makeIntField('qual', '道具品质')
    c = f.makeIntField('c', '个数或次数要求')
    ilv = f.makeIntField('ilv', '强化等级')
    hid = f.makeIntField('hid', '角色ID')
    hlv = f.makeIntField('hlv', '角色等级')
    tlv = f.makeIntField('tlv', '天赋级别')
    tp = f.makeIntField('tp', '天赋投点数')
    rid = f.makeIntField('rid', '排行榜ID')
    rlv = f.makeIntField('rlv', '排行榜名次或段位')
    mode = f.makeIntField('mode', '模式ID')
    modelv = f.makeIntField('modelv', '模式难度或者区域编号')
    modenode = f.makeIntField('modenode', '模式节点')
    win = f.makeIntField('win', '是否获胜')
    checkin = f.makeIntField('checkin', '签到格ID')
    daily = f.makeIntField('daily', '日常宝箱ID')
    for i in range(1, 5):
        exec "reward_type%s = f.makeIntField('reward_type%s', '奖励类型%s')"%(i, i, i) in globals(), locals()
        exec "reward_id%s = f.makeIntField('reward_id%s', '奖励ID%s')"%(i, i, i) in globals(), locals()
        exec "reward_amount%s = f.makeIntField('reward_amount%s', '奖励数量%s')"%(i, i, i) in globals(), locals()

# 物品系统 {{{1
#=============================================================================
class Item(Document):
    """ 物品表 """

    meta = {'collection': 'item'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    act = f.makeStringField('act', '动画')
    price = f.makeIntField('price', '出售金币价格')
    quality = f.makeIntField('quality', '品质')
    type = f.makeIntField('type', '类型')
    hero = f.makeIntField('hero', '专属英雄')
    stack = f.makeIntField('stack', '最大堆叠数')
    rid = f.makeIntField('rid', '奖励ID')


class Dice(Document):
    """ 骰子表 """

    meta = {'collection': 'dice'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    act = f.makeStringField('act', '动画')
    price = f.makeIntField('price', '出售金币价格')
    quality = f.makeIntField('quality', '品质')
    hero = f.makeIntField('hero', '专属英雄')
    explode = f.makeIntField('explode', '分解奖励ID')
    min = f.makeIntField('min', '最小点数')
    max = f.makeIntField('max', '最大点数')
    rate = f.makeIntField('rate', '命中概率')
    attr = f.makeIntField('attr', '属性配置ID')
    goods = f.makeIntField('goods', '是否商品')


class Car(Document):
    """ 载具表 """

    meta = {'collection': 'car'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    act = f.makeStringField('act', '动画')
    price = f.makeIntField('price', '出售金币价格')
    quality = f.makeIntField('quality', '品质')
    type = f.makeIntField('type', '类型')
    sex = f.makeIntField('sex', '性别')
    hero = f.makeIntField('hero', '专属英雄')
    explode = f.makeIntField('explode', '分解奖励ID')
    dice = f.makeIntField('dice', '骰子数')
    round = f.makeIntField('round', '回合数')
    attr = f.makeIntField('attr', '属性配置ID')
    goods = f.makeIntField('goods', '是否商品')


class Cloth(Document):
    """ 服装表 """

    meta = {'collection': 'cloth'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    act = f.makeStringField('act', '动画')
    price = f.makeIntField('price', '出售金币价格')
    quality = f.makeIntField('quality', '品质')
    sex = f.makeIntField('sex', '性别限定')
    hero = f.makeIntField('hero', '专属英雄')
    explode = f.makeIntField('explode', '分解奖励ID')
    attr = f.makeIntField('attr', '属性配置ID')
    goods = f.makeIntField('goods', '是否商品')


class Enhance(Document):
    """ 强化表 """

    meta = {'collection': 'enhance'}

    id = f.createIdField()
    itype = f.makeIntField('itype', '道具类型')
    iid = f.makeIntField('iid', '道具ID')
    smax = f.makeIntField('smax', '最大阶级')
    board = f.makeIntListField('board', '边框')
    act = f.makeIntListField('act', '动画')
    coin_type = f.makeIntListField('coin_type', '货币种类')
    coin_count = f.makeIntListField('coin_count', '货币价格')
    TN = f.makeIntListField('TN', '体能')
    YZ = f.makeIntListField('YZ', '意志')
    XYA = f.makeIntListField('XYA', '信仰')
    XYO = f.makeIntListField('XYO', '信用')
    CZ = f.makeIntListField('CZ', '才智')
    HH = f.makeIntListField('HH', '厚黑')


class RewardMail(Document):
    """ 奖励邮件配置表 """

    meta = {'collection': 'reward_mail'}

    id = f.createIdField()
    title = f.makeStringField('title', '标题')
    content = f.makeTextField('content', '内容')

class Mall(Document):
    """ 商城配置表 """

    meta = {'collection': 'mall'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '说明')
    act = f.makeStringField('act', '动画')
    type = f.makeIntField('type', '商城分类')
    t = f.makeIntField('t', '显示类型')
    status = f.makeIntField('status', '状态')
    quality = f.makeIntField('quality', '品质')
    coin1 = f.makeIntField('coin1', '花费金币数')
    coin2 = f.makeIntField('coin2', '花费水晶数')
    pcoin1 = f.makeIntField('pcoin1', '金币原价')
    pcoin2 = f.makeIntField('pcoin2', '水晶原价')
    friend = f.makeIntField('friend', '是否友情商品')
    rid = f.makeIntField('rid', '奖励ID')


# 活动 {{{1
#=============================================================================
class MovieTicket(Document):
    """ 电影票 """
    meta = {'collection': 'movieticket'}
    id = f.createIdField()
    code = f.makeStringField('code', '电影票兑换码')
    used = f.makeIntField('used', '是否已经使用过')

class Activity(Document):
    """ 活动表 """

    meta = {'collection': 'activity'}

    id = f.createIdField()
    name = f.makeStringField('name', '活动名称')
    type = f.makeIntField('type', '活动类型')
    link = f.makeIntField('link', '连接类型')
    offlinerewardtype = f.makeIntField('offlinerewardtype', '线下奖励类型')
    offlinerewardamount = f.makeIntField('offlinerewardamount', '线下奖励数量')
    need_signup = f.makeIntField('need_signup', '是否需要报名')

    announcement = f.makeStringField('announcement', '走字内容')
    announcement_bef = f.makeIntField('announcement_bef', '走字提前秒数')

    backtips = f.makeStringField('backtips', '返回提示')
    countdown = f.makeIntField('countdown', '倒计时类型')
    costtime = f.makeIntField('costtime', '扣款时机')

    rank_name = f.makeStringField('rank_name', '排行榜标题')
    rank_desc = f.makeStringField('rank_desc', '排行榜内容')

    reward_btn = f.makeIntField('reward_btn', '领取奖励按钮')
    icon = f.makeIntField('icon', 'ICON')
    has_pct = f.makeIntField('has_pct', '有无宣传图')
    desc = f.makeStringField('desc', '活动简介')
    info = f.makeTextField('info', '活动规则')
    acttext = f.makeStringField('acttext', '活动结算显示')

    begin_date = f.makeStringField('begin_date', '周期开始日期')
    begin_time = f.makeStringField('begin_time', '周期开始时间')
    end_date = f.makeStringField('end_date', '周期结束日期')
    end_time = f.makeStringField('end_time', '周期结束时间')

    reward_begin_date = f.makeStringField('reward_begin_date', '领奖开始日期')
    reward_begin_time = f.makeStringField('reward_begin_time', '领奖开始时间')
    reward_end_date = f.makeStringField('reawrd_end_date', '领奖结束日期')
    reward_end_time = f.makeStringField('reawrd_end_time', '领奖结束时间')

    time_type = f.makeIntField('time_type', '活动日期类型')
    days = f.makeDynamicField('days', '活动日期数')

    a_begin_time = f.makeStringField('a_begin_time', '活动开始时间')
    a_end_time = f.makeStringField('a_end_time', '活动结束时间')

    rank = f.makeDynamicField('rank', '排行名次列表')
    rank_type = f.makeDynamicField('rank_type', '排行奖励类型列表')
    rank_reward = f.makeDynamicField('rank_reward', '排行奖励ID列表')
    rank_amount = f.makeDynamicField('rank_amount', '排行奖励数量列表')

    gpid = f.makeDynamicField('gpid', '礼包id列表')
    gpid_type = f.makeDynamicField('gpid_type', '礼包类型列表')
    gpid_n = f.makeDynamicField('gpid_n', '礼包奖励数量列表')

    for i in range(1, 11):
        exec "reward_name%s = f.makeStringField('reward_name%s', '奖励名称%s')"%(i, i, i) in globals(), locals()
        exec "reward_coin_id%s = f.makeIntField('reward_coin_id%s', '货币奖励类型%s')"%(i, i, i) in globals(), locals()
        exec "reward_coin_amount%s = f.makeIntField('reward_coin_amount%s', '货币奖励数量%s')"%(i, i, i) in globals(), locals()
        exec "reward_amount%s = f.makeIntField('reward_amount%s', '道具奖励数%s')"%(i, i, i) in globals(), locals()
        exec "reward_choose%s = f.makeIntField('reward_choose%s', '可选奖励数%s')"%(i, i, i) in globals(), locals()
        for j in xrange(1, 5):
            exec "reward_item_type_%s_%s = f.makeIntField('reward_item_type_%s_%s', '道具奖励类型%s_%s')"%(i, j, i, j, i, j) in globals(), locals()
            exec "reward_item_id_%s_%s = f.makeIntField('reward_item_id_%s_%s', '道具奖励ID%s_%s')"%(i, j, i, j, i, j) in globals(), locals()
            exec "reward_item_amount_%s_%s = f.makeIntField('reward_item_amount_%s_%s', '道具奖励数量%s_%s')"%(i, j, i, j, i, j) in globals(), locals()
            del j
        del i

    """
        活动类型（1：游戏内活动（奖励游戏内领取），2：充值活动（奖励游戏内领取），3：运营活动（奖励外送））	
        活动IconID	有无宣传图（0：普通文字显示方式，非0：在详情部分显示整张宣传图的ID序号）	
        活动简介	活动规则（富文本）	周期开始日期	周期开始时间	周期结束日期	周期结束时间	
        活动日期类型（0：整个周期内，1：月内某几天，2：周内星期几）	
        活动日期数列(为0时指全部，类型为0时此值必为0)	
        活动开始时间（为空时为整天）	活动结束时间（为空时为整天）	

        奖励名称1（为空表示无该奖励或第一组为空时表示该奖励通过其他形式发送不在活动面板领取）	
        货币奖励类型1（为0时表示没有货币奖励）	货币奖励数值1	道具奖励数1（决定该等级道具奖励数量，可以为0，为0表示没有道具奖励）	道具奖励类型1_1	道具奖励ID1_1	道具奖励数量1_1	道具奖励类型1_2	道具奖励ID1_2	道具奖励数量1_2	道具奖励类型1_3	道具奖励ID1_3	道具奖励数量1_3	道具奖励类型1_4	道具奖励ID1_4	道具奖励数量1_4	
        奖励名称2	货币奖励类型2	货币奖励数值2	道具奖励数2	道具奖励类型2_1	道具奖励ID2_1	道具奖励数量2_1	道具奖励类型2_2	道具奖励ID2_2	道具奖励数量2_2	道具奖励类型2_3	道具奖励ID2_3	道具奖励数量2_3	道具奖励类型2_4	道具奖励ID2_4	道具奖励数量2_4	
        奖励名称3	货币奖励类型3	货币奖励数值3	道具奖励数3	道具奖励类型3_1	道具奖励ID3_1	道具奖励数量3_1	道具奖励类型3_2	道具奖励ID3_2	道具奖励数量3_2	道具奖励类型3_3	道具奖励ID3_3	道具奖励数量3_3	道具奖励类型3_4	道具奖励ID3_4	道具奖励数量3_4	
        奖励名称4	货币奖励类型4	货币奖励数值4	道具奖励数4	道具奖励类型4_1	道具奖励ID4_1	道具奖励数量4_1	道具奖励类型4_2	道具奖励ID4_2	道具奖励数量4_2	道具奖励类型4_3	道具奖励ID4_3	道具奖励数量4_3	道具奖励类型4_4	道具奖励ID4_4	道具奖励数量4_4	
        奖励名称5	货币奖励类型5	货币奖励数值5	道具奖励数5	道具奖励类型5_1	道具奖励ID5_1	道具奖励数量5_1	道具奖励类型5_2	道具奖励ID5_2	道具奖励数量5_2	道具奖励类型5_3	道具奖励ID5_3	道具奖励数量5_3	道具奖励类型5_4	道具奖励ID5_4	道具奖励数量5_4	
        奖励名称6	货币奖励类型6	货币奖励数值6	道具奖励数6	道具奖励类型6_1	道具奖励ID6_1	道具奖励数量6_1	道具奖励类型6_2	道具奖励ID6_2	道具奖励数量6_2	道具奖励类型6_3	道具奖励ID6_3	道具奖励数量6_3	道具奖励类型6_4	道具奖励ID6_4	道具奖励数量6_4	
        奖励名称7	货币奖励类型7	货币奖励数值7	道具奖励数7	道具奖励类型7_1	道具奖励ID7_1	道具奖励数量7_1	道具奖励类型7_2	道具奖励ID7_2	道具奖励数量7_2	道具奖励类型7_3	道具奖励ID7_3	道具奖励数量7_3	道具奖励类型7_4	道具奖励ID7_4	道具奖励数量7_4
    """

class SpActivity(Document):
    """ 推广活动表 """

    meta = {'collection': 'spactivity'}

    id = f.createIdField()
    name = f.makeStringField('name', '活动名称')
    type = f.makeIntField('type', '活动类型')
    offlinerewardtype = f.makeIntField('offlinerewardtype', '线下奖励类型')
    offlinerewardamount = f.makeIntField('offlinerewardamount', '线下奖励数量')
    uiid = f.makeIntField('uiid', '界面id')
    ui = f.makeIntField('ui', '界面序号')

    announcement = f.makeStringField('announcement', '走字内容')
    announcement_bef = f.makeIntField('announcement_bef', '走字提前秒数')

    need_mobile = f.makeIntField('need_mobile', '是否需要手机')
    backtips = f.makeStringField('backtips', '返回提示')
    countdown = f.makeIntField('countdown', '倒计时类型')

    link = f.makeIntField('link', '连接类型')

    rank_name = f.makeStringField('rank_name', '排行榜标题')
    rank_desc = f.makeStringField('rank_desc', '排行榜内容')

    reward_btn = f.makeIntField('reward_btn', '领取奖励按钮')
    icon = f.makeIntField('icon', 'ICON')
    has_pct = f.makeIntField('has_pct', '有无宣传图')
    desc = f.makeStringField('desc', '活动简介')
    info = f.makeTextField('info', '活动规则')
    timedesc = f.makeStringField('timedesc', '时间简介')

    begin_date = f.makeStringField('begin_date', '周期开始日期')
    begin_time = f.makeStringField('begin_time', '周期开始时间')
    end_date = f.makeStringField('end_date', '周期结束日期')
    end_time = f.makeStringField('end_time', '周期结束时间')

    reward_begin_date = f.makeStringField('reward_begin_date', '领奖开始日期')
    reward_begin_time = f.makeStringField('reward_begin_time', '领奖开始时间')
    reward_end_date = f.makeStringField('reawrd_end_date', '领奖结束日期')
    reward_end_time = f.makeStringField('reawrd_end_time', '领奖结束时间')

    time_type = f.makeIntField('time_type', '活动日期类型')
    days = f.makeDynamicField('days', '活动日期数')

    a_begin_time = f.makeStringField('a_begin_time', '活动开始时间')
    a_end_time = f.makeStringField('a_end_time', '活动结束时间')


    rank = f.makeDynamicField('rank', '排行名次列表')
    rank_type = f.makeDynamicField('rank_type', '排行奖励类型列表')
    rank_reward = f.makeDynamicField('rank_reward', '排行奖励ID列表')
    rank_amount = f.makeDynamicField('rank_amount', '排行奖励数量列表')

    gpid = f.makeDynamicField('gpid', '礼包id列表')
    gpid_type = f.makeDynamicField('gpid_type', '礼包类型列表')
    gpid_n = f.makeDynamicField('gpid_n', '礼包奖励数量列表')

    for i in range(1, 11):
        exec "reward_name%s = f.makeStringField('reward_name%s', '奖励名称%s')"%(i, i, i) in globals(), locals()
        exec "reward_coin_id%s = f.makeIntField('reward_coin_id%s', '货币奖励类型%s')"%(i, i, i) in globals(), locals()
        exec "reward_coin_amount%s = f.makeIntField('reward_coin_amount%s', '货币奖励数量%s')"%(i, i, i) in globals(), locals()
        exec "reward_amount%s = f.makeIntField('reward_amount%s', '道具奖励数%s')"%(i, i, i) in globals(), locals()
        for j in xrange(1, 5):
            exec "reward_item_type_%s_%s = f.makeIntField('reward_item_type_%s_%s', '道具奖励类型%s_%s')"%(i, j, i, j, i, j) in globals(), locals()
            exec "reward_item_id_%s_%s = f.makeIntField('reward_item_id_%s_%s', '道具奖励ID%s_%s')"%(i, j, i, j, i, j) in globals(), locals()
            exec "reward_item_amount_%s_%s = f.makeIntField('reward_item_amount_%s_%s', '道具奖励数量%s_%s')"%(i, j, i, j, i, j) in globals(), locals()
            del j
        del i

class ActivityBattle(Document):
    """ 活动战斗表 """
    meta = {'collection': 'activitybattle'}

    id = f.createIdField()
    acttype = f.makeIntField('acttype', '活动类型')
    tid = f.makeIntField('tid', 'TID')

    is_player = f.makeIntField('is_player', '是否玩家')
    hero = f.makeIntListField('hero', '英雄')
    ailv = f.makeIntField('ailv', 'AI等级')
    god_id = f.makeIntField('god_id', '神仙id')
    re_god_rate = f.makeFloatField('re_god_rate', 'NPC再次附身几率')
    order = f.makeIntField('order', '队伍顺序')

    star = f.makeIntField('star', '初始能量')
    cash = f.makeIntField('cash', '初始资金')

    forbid_cards = f.makeIntListField('forbid_cards', '禁用卡片列表')

    card1 = f.makeIntField('card1', '卡片1')
    card2 = f.makeIntField('card2', '卡片2')
    card3 = f.makeIntField('card3', '卡片3')
    card4 = f.makeIntField('card4', '卡片4')
    card5 = f.makeIntField('card5', '卡片5')

    car = f.makeIntField('car', '载具')

    skill1 = f.makeIntField('skill1', '技能1')
    skill2 = f.makeIntField('skill2', '技能2')
    skill3 = f.makeIntField('skill3', '技能3')
    skill4 = f.makeIntField('skill4', '技能4')
    skill5 = f.makeIntField('skill5', '技能5')


# 小游戏 {{{1
#=============================================================================
class MiniGame(Document):
    """ 小游戏表 """
    meta = {'collection': 'mini_game'}
    id = f.createIdField()
    order = f.makeIntField('order', '顺序')
    name = f.makeStringField('name', '名字')
    desc = f.makeStringField('desc', '场外简介')
    idesc = f.makeStringField('idesc', '场内简介')

    daylimit = f.makeIntField("daylimit", "进入次数限制（每日）")
    tili = f.makeIntField("tili", "单次体力消耗")

    costtype = f.makeIntField("costtype", "进入消耗货币类型（0为无，1为金币，2为幸运星，3为场内初始资金）")
    costamount = f.makeIntField("costamount", "进入消耗货币值")

    ratio = f.makeFloatField("ratio", "场外无投注方获胜概率")

    bettype1 = f.makeDynamicField("bettype1", "场外投注金额类型列表1（0为无，1为金币，2为幸运星，3为场内初始资金）")
    betn1 = f.makeDynamicField("betn1", "场外投注金额数值列表1（百分比，实际计算以进入消耗为基数，入场费为a）")
    betreward1 = f.makeDynamicField("betreward1", "场外获胜金额数值列表1（百分比，实际计算以进入消耗为基数,入场费为a，倍数为n）")
    bettype2 = f.makeDynamicField("bettype2", "场外投注金额类型列表2")
    betn2 = f.makeDynamicField("betn2", "场外投注金额数值列表2")
    betreward2 = f.makeDynamicField("betreward2", "场外获胜金额数值列表2")
    bettype3 = f.makeDynamicField("bettype3", "场外投注金额类型列表3")
    betn3 = f.makeDynamicField("betn3", "场外投注金额数值列表3")
    betreward3 = f.makeDynamicField("betreward3", "场外获胜金额数值列表3")

    conwintype = f.makeDynamicField("conwintype", "连中三元奖励类型列表（0为无，1为金币，2为幸运星，3为场内初始资金）")
    conwinn = f.makeDynamicField("conwinn", "连中三元奖励数值列表（百分比，以参赛费用为基数，a为入场费，b为3回合累积投注额度）")

    i_ratio = f.makeDynamicField("i_ratio", "场内无投注方获胜概率")
    i_bettype1 = f.makeDynamicField("i_bettype1", "场内投注金额类型列表1（0为无，1为金币，2为幸运星，3为场内初始资金）")
    i_betn1 = f.makeDynamicField("i_betn1", "场内投注金额数值列表1（百分比，实际计算以初始资金为基数，场内资金为e）")
    i_betreward1 = f.makeDynamicField("i_betreward1", "场内获胜金额数值列表1（百分比，实际计算以初始资金为基数，场内初始资金为b）")
    i_bettype2 = f.makeDynamicField("i_bettype2", "场内投注金额类型列表2（0为无，1为金币，2为幸运星，3为场内初始资金）")
    i_betn2 = f.makeDynamicField("i_betn2", "场内投注金额数值列表2，场内资金为b")
    i_betreward2 = f.makeDynamicField("i_betreward2", "场内获胜金额数值列表2，场内资金为b")
    i_bettype3 = f.makeDynamicField("i_bettype3", "场内投注金额类型列表3（0为无，1为金币，2为幸运星，3为场内初始资金）")
    i_betn3 = f.makeDynamicField("i_betn3", "场内投注金额数值列表3，场内资金为b")
    i_betreward3 = f.makeDynamicField("i_betreward3", "场内获胜金额数值列表3，场内资金为b")

    i_conwintype = f.makeDynamicField("i_conwintype", "连中三元奖励类型列表（0为无，1为金币，2为幸运星，3为场内初始资金）")
    i_conwinn = f.makeDynamicField("i_conwinn", "连中三元奖励数值列表（百分比，以参赛费用为基数，a为入场费，b为3回合累积投注额度）")

    chamtype = f.makeDynamicField("chamtype", "排行榜冠军奖励类型列表")
    chamn = f.makeDynamicField("chamn", "排行榜冠军奖励数值列表")

    lvlist = f.makeDynamicField("lvlist", "关卡难度随机组列表")
    avg = f.makeDynamicField("avg", "难度加成的平均分数列表")
    extralv = f.makeDynamicField("extralv", "对应提高难度数列表")
    point = f.makeDynamicField("point", "场外分数列表")
    point2 = f.makeDynamicField("point2", "场外分数奖金列表")
    point_reward_type = f.makeDynamicField("point_reward_type", "场外分数奖金类型")
    point_reward_rate = f.makeDynamicField("point_reward_rate", "场外分数奖励比例浮点列表（比例*入场费=实际奖励）")
    i_point = f.makeDynamicField("i_point", "场内分数列表")
    i_point2 = f.makeDynamicField("i_point2", "场内分数奖金列表")
    i_point_reward_type = f.makeDynamicField("i_point_reward_type", "场内分数奖金类型")
    i_point_reward_rate = f.makeDynamicField("i_point_reward_rate", "场内分数奖励比例浮点列表")
    con = f.makeDynamicField("con", "场外连中列表")
    con_type = f.makeDynamicField("con_type", "场外连中奖励类型列表")
    con_rate = f.makeDynamicField("con_rate", "场外连中奖励比例数值列表（实际奖励为比例*入场费）")
    i_con = f.makeDynamicField("i_con", "场内连中列表")
    i_con_type = f.makeDynamicField("i_con_type", "场内连中奖励类型列表")
    i_con_rate = f.makeDynamicField("i_con_rate", "场内连中奖励比例数值列表（实际奖励为比例*入场费）")
    box = f.makeDynamicField("box", "场外暴击列表")
    box_type = f.makeDynamicField("box_type", "场外暴击奖励类型列表")
    box_n = f.makeDynamicField("box_n", "场外暴击奖励数值列表")
    box_amount = f.makeDynamicField("box_amount", "场外暴击个数列表")
    box_time = f.makeDynamicField("box_time", "场外暴击停留时间列表")
    i_box = f.makeDynamicField("i_box", "场内暴击列表")
    i_box_type = f.makeDynamicField("i_box_type", "场内暴击奖励类型列表")
    i_box_n = f.makeDynamicField("i_box_n", "场内暴击奖励数值列表")
    i_box_amount = f.makeDynamicField("i_box_amount", "场内暴击个数列表")
    i_box_time = f.makeDynamicField("i_box_time", "场内暴击停留时间列表")
    hint_type = f.makeDynamicField("hint_type", "场外提示消耗类型列表")
    hint_cost = f.makeDynamicField("hint_cost", "场外提示消耗数值列表")
    i_hint_type = f.makeDynamicField("i_hint_type", "场内提示消耗类列表")
    i_hint_cost = f.makeDynamicField("i_hint_cost", "场内提示消耗数值列表")
    must_type = f.makeDynamicField("must_type", "场外必中金额类型列表（0为无，1为金币，2为幸运星，3为场内初始资金）")
    must_n = f.makeDynamicField("must_n", "场外必中金额数值列表（每日）")
    i_must_type = f.makeDynamicField("i_must_type", "场内必中金额类型列表（0为无，1为金币，2为幸运星，3为场内初始资金）")
    i_must_n = f.makeDynamicField("i_must_n", "场内必中金额数值列表（每日）")
    
class MiniGameTips(Document):
    """ 小游戏 冠军位置冒泡 """
    meta = {'collection': 'mini_game_tips'}
    id = f.createIdField()
    text = f.makeStringField('text', '文本')

class LHJ(Document):
    """ 老虎机概率 """
    meta = {'collection': 'lhj'}
    id = f.createIdField()
    icon_name = f.makeStringField("icon_name", "图案类型")

    t2 = f.makeFloatField("t2", "2个相同:倍数")
    t2_ir = f.makeFloatField("t2_ir", "2个相同:场内概率")
    t2_or = f.makeFloatField("t2_or", "2个相同:场外概率")

    t28 = f.makeFloatField("t28", "2个相同*8:倍数")
    t28_ir = f.makeFloatField("t28_ir", "2个相同*8:场内概率")
    t28_or = f.makeFloatField("t28_or", "2个相同*8:场外概率")

    t3 = f.makeFloatField("t3", "3个相同:倍数")
    t3_ir = f.makeFloatField("t3_ir", "3个相同:场内概率")
    t3_or = f.makeFloatField("t3_or", "3个相同:场外概率")

class DDD(Document):
    """ 点点点 """
    meta = {'collection': 'ddd'}

    id = f.createIdField()
    lv = f.makeIntField("lv", "难度")
    n = f.makeIntField("n", "总格子数")
    colors = f.makeDynamicField("colors", "颜色种类")
    right = f.makeIntField("right", "正确格子数")

class ZXL(Document):
    """ 找笑脸 """
    meta = {'collection': 'zxl'}

    id = f.createIdField()
    lv = f.makeIntField("lv", "难度")
    type = f.makeIntField("type", "类型")
    map = f.makeDynamicField("map", "格子定义")
    dir = f.makeIntField("dir", "方向")
    time = f.makeFloatField("time", "时间")
    detime = f.makeFloatField("detime", "扣除时间")


# 引导 {{{1
#=============================================================================
class GuideBattleMain(Document):

    """ 引导战斗节点表 """

    meta = {'collection': 'guidebattlemain'}

    id = f.createIdField()

    map = f.makeIntField('map', '地图id')
    tili = f.makeIntField('tili', '能量消耗')

    star1_round = f.makeIntField("star1_round", "1星回合数")
    star2_round = f.makeIntField("star2_round", "2星回合数")
    star3_round = f.makeIntField("star3_round", "3星回合数")

    # 奖励
    hero_id = f.makeIntField('hero_id', '英雄id')
    hero_level = f.makeIntField('hero_level', '英雄等级')
    item_id1 = f.makeIntField('item_id1', '道具id1')
    item_type1 = f.makeIntField('item_type1', '道具类型1')
    item_amount1 = f.makeIntField('item_amount1', '道具个数1')
    item_id2 = f.makeIntField('item_id2', '道具id2')
    item_type2 = f.makeIntField('item_type2', '道具类型2')
    item_amount2 = f.makeIntField('item_amount2', '道具个数2')
    item_id3 = f.makeIntField('item_id3', '道具id3')
    item_type3 = f.makeIntField('item_type3', '道具类型3')
    item_amount3 = f.makeIntField('item_amount3', '道具个数3')

    coin_type = f.makeIntField('coin_type', '奖励货币种类')
    coin_amount = f.makeIntField('coin_amount', '奖励货币数量')

    star1_exp = f.makeIntField("star1_exp", "1星经验")
    star2_exp = f.makeIntField("star2_exp", "2星经验")
    star3_exp = f.makeIntField("star3_exp", "3星经验")

    battle_egg = f.makeIntField("battle_egg", "彩蛋奖励")

class GuideBattle(Document):
    """ 引导战斗表 """

    meta = {'collection': 'guidebattle'}

    id = f.createIdField()

    guide_id = f.makeIntField('guide_id', '引导id')
    tid = f.makeIntField('tid', 'TID')

    is_player = f.makeIntField('is_player', '是否玩家')
    hero = f.makeIntField('hero', '英雄')
    god_id = f.makeIntField('god_id', '神仙id')
    re_god_rate = f.makeFloatField('re_god_rate', 'NPC再次附身几率')
    order = f.makeIntField('order', '队伍顺序')

    star = f.makeIntField('star', '初始能量')
    cash = f.makeIntField('cash', '初始资金')

    card1 = f.makeIntField('card1', '卡片1')
    card2 = f.makeIntField('card2', '卡片2')
    card3 = f.makeIntField('card3', '卡片3')
    card4 = f.makeIntField('card4', '卡片4')
    card5 = f.makeIntField('card5', '卡片5')

    car = f.makeIntField('car', '载具')

    skill1 = f.makeIntField('skill1', '技能1')
    skill2 = f.makeIntField('skill2', '技能2')
    skill3 = f.makeIntField('skill3', '技能3')
    skill4 = f.makeIntField('skill4', '技能4')
    skill5 = f.makeIntField('skill5', '技能5')

class BQuiz(Document):
    """ 场内问答表 """
    meta = {'collection': 'bquiz'}
    id = f.createIdField()
    question = f.makeStringField('question', '问题')
    answer = f.makeIntField('answer', '正确答案')

class AreaBox(Document):
    """ 区域宝箱 """
    meta = {'collection': 'areabox'}
    id = f.createIdField()
    area = f.makeStringField('area', '区域名称')
    desc = f.makeStringField('desc', '区域描述')
    star = f.makeIntField('star', '宝箱星数要求')
    node1 = f.makeIntField('node1', '宝箱重复挑战节点ID1')
    n1 = f.makeIntField('n1', '宝箱重复挑战次数要求1')
    node2 = f.makeIntField('node2', '宝箱重复挑战节点ID2')
    n2 = f.makeIntField('n2', '宝箱重复挑战次数要求2')

    for i in range(1, 6):
        exec "reward_type%s = f.makeIntField('reward_type%s', '道具类型%s')"%(i, i, i) in globals(), locals()
        exec "reward_id%s = f.makeIntField('reward_id%s', '道具ID%s')"%(i, i, i) in globals(), locals()
        exec "reward_amount%s = f.makeIntField('reward_amount%s', '个数%s')"%(i, i, i) in globals(), locals()

    heros = f.makeIntListField("heros", "角色奖励ID列表")
    hero_amount = f.makeIntField("hero_amount", "角色奖励可选个数")

class Pve(Document):
    """ PVE表 """
    meta = {'collection': 'pve'}

    id = f.createIdField()
    area = f.makeIntField('area', '区域')
    node = f.makeIntField('node', '节点')
    nodename = f.makeStringField('nodename', '节点名称')
    nodedesc = f.makeStringField('nodedesc', '节点描述')

    map = f.makeIntField('map', '地图id')
    tili = f.makeIntField('tili', '体力消耗')
    max_star = f.makeIntField("max_star", "最高能量")

    day_amount = f.makeIntField('day_amount', '每日次数')
    sum_amount = f.makeIntField('sum_amount', '总次数')

    r_area = f.makeIntField('r_area', '节点关联区域')
    r_node = f.makeIntField('r_node', '节点关联节点')

    winrule = f.makeIntListField("winrule", "额外胜利条件")
    winarg = f.makeIntListField("winarg", "额外胜利参数")

    # 限制条件
    l_coin_type = f.makeIntField('l_coin_type', '货币种类')
    l_coin_amount = f.makeIntField('l_coin_amount', '货币数量')
    l_card_level = f.makeIntField('l_card_level', '卡片星级')
    l_item_type = f.makeIntField('l_item_type', '道具类型')
    l_item_level = f.makeIntField('l_item_level', '道具等级')
    l_item_id = f.makeIntField('l_item_id', '道具id')
    l_skill_id = f.makeIntField('l_skill_id', '技能激活层级')
    l_skill_point = f.makeIntField('l_skill_point', '天赋投点数')
    l_max_hero_level = f.makeIntField('l_max_hero_level', '最大英雄等级')

    star1_round = f.makeIntField("star1_round", "1星回合数")
    star2_round = f.makeIntField("star2_round", "2星回合数")
    star3_round = f.makeIntField("star3_round", "3星回合数")


    # 奖励
    hero_id = f.makeIntField('hero_id', '英雄id')
    hero_level = f.makeIntField('hero_level', '英雄等级')
    item_id1 = f.makeIntField('item_id1', '道具id1')
    item_type1 = f.makeIntField('item_type1', '道具类型1')
    item_amount1 = f.makeIntField('item_amount1', '道具个数1')
    item_id2 = f.makeIntField('item_id2', '道具id2')
    item_type2 = f.makeIntField('item_type2', '道具类型2')
    item_amount2 = f.makeIntField('item_amount2', '道具个数2')
    item_id3 = f.makeIntField('item_id3', '道具id3')
    item_type3 = f.makeIntField('item_type3', '道具类型3')
    item_amount3 = f.makeIntField('item_amount3', '道具个数3')

    coin_type = f.makeIntField('coin_type', '奖励货币种类')
    coin_amount = f.makeIntField('coin_amount', '奖励货币数量')

    star1_exp = f.makeIntField("star1_exp", "1星经验")
    star2_exp = f.makeIntField("star2_exp", "2星经验")
    star3_exp = f.makeIntField("star3_exp", "3星经验")

    battle_egg = f.makeIntField("battle_egg", "彩蛋奖励")

    for i in range(1, 4):
        exec "repeat_n_%s = f.makeIntField('repeat_n_%s', '刷刷次数%s')"%(i, i, i) in globals(), locals()
        for j in range(1, 5):
            exec "repeat_reward_type%s_%s = f.makeIntField('repeat_reward_type%s_%s', '道具类型%s_%s')"%(i, j, i, j, i, j) in globals(), locals()
            exec "repeat_reward_id%s_%s = f.makeIntField('repeat_reward_id%s_%s', '道具ID%s_%s')"%(i, j, i, j, i, j) in globals(), locals()
            exec "repeat_reward_amount%s_%s = f.makeIntField('repeat_reward_amount%s_%s', '个数%s_%s')"%(i, j, i, j, i, j) in globals(), locals()


class PveBattle(Document):
    """ PVE表 """
    meta = {'collection': 'pvebattle'}

    id = f.createIdField()
    area = f.makeIntField('area', '区域')
    node = f.makeIntField('node', '节点')
    tid = f.makeIntField('tid', 'TID')

    is_player = f.makeIntField('is_player', '是否玩家')
    hero = f.makeIntListField('hero', '英雄')
    ailv = f.makeIntField('ailv', 'AI等级')
    god_id = f.makeIntField('god_id', '神仙id')
    re_god_rate = f.makeFloatField('re_god_rate', 'NPC再次附身几率')
    order = f.makeIntField('order', '队伍顺序')

    star = f.makeIntField('star', '初始能量')
    cash = f.makeIntField('cash', '初始资金')

    card1 = f.makeIntField('card1', '卡片1')
    card2 = f.makeIntField('card2', '卡片2')
    card3 = f.makeIntField('card3', '卡片3')
    card4 = f.makeIntField('card4', '卡片4')
    card5 = f.makeIntField('card5', '卡片5')

    car = f.makeIntField('car', '载具')

    skill1 = f.makeIntField('skill1', '技能1')
    skill2 = f.makeIntField('skill2', '技能2')
    skill3 = f.makeIntField('skill3', '技能3')
    skill4 = f.makeIntField('skill4', '技能4')
    skill5 = f.makeIntField('skill5', '技能5')

class AchieveIcon(Document):
    """ 成就徽章表 """
    meta = {'collection': 'achieveicon'}
    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    desc = f.makeStringField('desc', "简介")

class Achieve(Document):
    """ 成就表 """
    meta = {'collection': 'achieve'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    info = f.makeTextField('info', '简介')
    ui = f.makeIntField('ui', '跳转ID')

    kind = f.makeIntField('kind', '任务类型')
    lv = f.makeIntField('lv', '级别')
    icon = f.makeIntField('icon', '徽章ID')

    item_kind = f.makeIntField('item_kind', '物品种类')
    item_id = f.makeIntField('item_id', '物品ID')
    qual = f.makeIntField('qual', '道具品质')
    c = f.makeIntField('c', '个数或次数要求')
    ilv = f.makeIntField('ilv', '强化等级')
    hid = f.makeIntField('hid', '角色ID')
    hlv = f.makeIntField('hlv', '角色等级')
    tlv = f.makeIntField('tlv', '天赋级别')
    tp = f.makeIntField('tp', '天赋投点数')
    rid = f.makeIntField('rid', '排行榜ID')
    rlv = f.makeIntField('rlv', '排行榜名次或段位')
    mode = f.makeIntField('mode', '模式ID')
    modelv = f.makeIntField('modelv', '模式难度或者区域编号')
    modenode = f.makeIntField('modenode', '模式节点')
    win = f.makeIntField('win', '是否获胜')
    checkin = f.makeIntField('checkin', '签到格ID')
    daily = f.makeIntField('daily', '日常宝箱ID')

    for i in range(1, 5):
        exec "reward_type%s = f.makeIntField('reward_type%s', '奖励类型%s')"%(i, i, i) in globals(), locals()
        exec "reward_id%s = f.makeIntField('reward_id%s', '奖励ID%s')"%(i, i, i) in globals(), locals()
        exec "reward_amount%s = f.makeIntField('reward_amount%s', '奖励数量%s')"%(i, i, i) in globals(), locals()


# 前端配置 {{{1
#=============================================================================
class RankReward(Document):

    """ 排行奖励表 """

    meta = {'collection': 'rankreward'}
    id = f.createIdField()

    rank_id = f.makeIntField("rank_id", "排行榜ID")
    rank_name = f.makeStringField("rank_name", "排行榜名")
    rank_desc = f.makeStringField("rank_desc", "排行榜简介")
    rank_rank = f.makeIntField("rank_rank", "排行榜名次")
    time = f.makeIntField("time", "奖励周期（0：不奖，1：月内某几天，2：周内星期几，3：每天）")
    date = f.makeIntListField("date", "奖励日期数列(为0时指全部，类型为0时此值必为0)")
    n = f.makeIntField("n", "奖励数量（用于配置排行榜奖励的配置数）")
    reward_n = f.makeIntField("reward_n", "道具奖励数1（决定该等级道具奖励数量，可以为0，为0表示没有道具奖励）")
    item_type1 = f.makeIntField("item_type1", "道具奖励类型1_1")
    item_id1 = f.makeIntField("item_id1", "道具奖励ID1_1")
    item_amount1 = f.makeIntField("item_amount1", "道具奖励数量1_1")
    item_type2 = f.makeIntField("item_type2", "道具奖励类型1_2")
    item_id2 = f.makeIntField("item_id2", "道具奖励ID1_2")
    item_amount2 = f.makeIntField("item_amount2", "道具奖励数量1_2")
    item_type3 = f.makeIntField("item_type3", "道具奖励类型1_3")
    item_id3 = f.makeIntField("item_id3", "道具奖励ID1_3")
    item_amount3 = f.makeIntField("item_amount3", "道具奖励数量1_3")
    item_type4 = f.makeIntField("item_type4", "道具奖励类型1_4")
    item_id4 = f.makeIntField("item_id4", "道具奖励ID1_4")
    item_amount4 = f.makeIntField("item_amount4", "道具奖励数量1_4")
    item_type5 = f.makeIntField("item_type5", "道具奖励类型1_5")
    item_id5 = f.makeIntField("item_id5", "道具奖励ID1_5")
    item_amount5 = f.makeIntField("item_amount5", "道具奖励数量1_5")
    item_type6 = f.makeIntField("item_type6", "道具奖励类型1_6")
    item_id6 = f.makeIntField("item_id6", "道具奖励ID1_6")
    item_amount6 = f.makeIntField("item_amount6", "道具奖励数量1_6")

class Vip(Document):

    """ VIP 配置表 """

    meta = {'collection': 'vip'}

    id = f.createIdField()
    lv = f.makeIntField('lv', 'VIP等级')
    need_coin2 = f.makeIntField('need_coin2', 'VIP条件（充值幸运星值）')
    desc = f.makeTextField('desc', '福利说明（富文本）')

    # 永久福利
    bag_size = f.makeIntField('bag_size', '格子数')
    rank_amount = f.makeIntField('rank_amount', '排行挑战增加次数')
    pve_amount = f.makeIntField('pve_amount', '生涯每节点每日增加次数')
    play_amount = f.makeIntField('play_amount', '游乐场次数')

    # 一次性福利
    hero_id = f.makeIntField('hero_id', '英雄ID')

    for i in range(1, 4):
        exec "item_type_%s = f.makeIntField('item_type_%s', '道具分类%s')"%(i, i, i) in globals(), locals()
        exec "item_id_%s = f.makeIntField('item_id_%s', '道具ID%s')"%(i, i, i) in globals(), locals()
        exec "item_amount_%s = f.makeIntField('item_amount_%s', '道具数量%s')"%(i, i, i) in globals(), locals()

class ClientTips(Document):
    """ 流程提示表 """
    meta = {'collection': 'client_tips'}

    id = f.createIdField()
    info = f.makeStringField('info', '提示信息')
    visible = f.makeIntField('visible', '作用范围')


class ClientCss(Document):
    """ 样式表 """
    meta = {'collection': 'client_css'}

    id = f.createIdField()
    name = f.makeStringField('name', '名称')
    css = f.makeDynamicField('css', '样式')


class Tips(Document):
    """ 提示语表 """
    meta = {'collection': 'tips'}

    id = f.createIdField()
    info = f.makeStringField('info', '信息')

class Notifys(Document):
    """ 弱提示表 """
    meta = {'collection': 'notifys'}

    id = f.createIdField()
    info = f.makeStringField('info', '信息') 
    ui = f.makeIntField('ui', '跳转界面') 

class Message(Document):
    """ 信息表 """
    meta = {'collection': 'message'}

    id = f.createIdField()
    key = f.makeStringField('key', '键')
    value = f.makeTextField('value', '值')


class GuideBoard(Document):
    """ 对话框表 """
    meta = {'collection': 'guide_board'}

    id = f.createIdField()
    info = f.makeStringField('info', '简介')
    image_x = f.makeIntField('image_x', '图片X坐标')
    image_y = f.makeIntField('image_y', '图片Y坐标')
    image_scale_x = f.makeFloatField('image_scale_x', '图片X比例')
    image_scale_y = f.makeFloatField('image_scale_y', '图片Y比例')
    name = f.makeStringField('name', '名字')
    name_id = f.makeIntField('name_id', '名字id')
    name_x = f.makeIntField('name_x', '名字X坐标')
    name_y = f.makeIntField('name_y', '名字Y坐标')
    board_width = f.makeIntField('board_width', '对话框宽度')
    board_height = f.makeIntField('board_height', '对话框高度')
    board_x = f.makeIntField('board_x', '对话框X坐标')
    board_y = f.makeIntField('board_y', '对话框Y坐标')
    richtext_width = f.makeIntField('richtext_width', '富文本宽度')
    richtext_height = f.makeIntField('richtext_height', '富文本高度')
    richtext_x = f.makeIntField('richtext_x', '富文本X坐标')
    richtext_y = f.makeIntField('richtext_y', '富文本Y坐标')

class GuideMain(Document):
    """ 引导汇总表 """
    meta = {'collection': 'guidemain'}

    id = f.createIdField()
    section = f.makeIntField('section', '章节ID')
    name = f.makeStringField('name', '章节名')
    english = f.makeStringField('english', '英文名')
    brief = f.makeStringField('brief', '章节简介')
    unlock = f.makeIntField('unlock', '解锁等级')

    prop_type1 = f.makeIntField('prop_type1', '道具类型1')
    propID1 = f.makeIntField('propID1', '道具ID1')
    prop_count1 = f.makeIntField('prop_count1', '道具数量1')
    prop_type2 = f.makeIntField('prop_type2', '道具类型2')
    propID2 = f.makeIntField('propID2', '道具ID2')
    prop_count2 = f.makeIntField('prop_count2', '道具数量2')
    prop_type3 = f.makeIntField('prop_type3', '道具类型3')
    propID3 = f.makeIntField('propID3', '道具ID3')
    prop_count3 = f.makeIntField('prop_count3', '道具数量3')
    coin_type1 = f.makeIntField('coin_type1', '货币类型1')
    coin_count1 = f.makeIntField('coin_count1', '货币点数1')
    coin_type2 = f.makeIntField('coin_type2', '货币类型2')
    coin_count2 = f.makeIntField('coin_count2', '货币点数2')
    exp = f.makeIntField('exp', '经验值')

class Guide(Document):
    """ 引导表 """
    meta = {'collection': 'guide'}

    id = f.createIdField()
    section = f.makeIntField('section', '章节ID')
    name = f.makeStringField('name', '章节名')
    english = f.makeStringField('english', '英文名')
    brief = f.makeStringField('brief', '章节简介')
    step = f.makeIntField('step', '步骤ID')
    stepID = f.makeIntField('stepID', '步骤唯一ID')
    content = f.makeStringField('content', '对话内容')
    audio = f.makeIntField('audio', '音频ID')
    head = f.makeIntField('head', '头像ID')
    board = f.makeIntField('board', '对话框ID')
    show = f.makeIntField('show', '遮罩显示')
    block = f.makeIntField('block', '是否屏蔽')
    custom = f.makeIntField('custom', '自定义图片ID')
    belong = f.makeStringField('belong', '归属界面')
    max_level = f.makeIntField('max_level', '最大角色等级')
    coin_type = f.makeIntField('coin_type', '持有货币种类')
    coin_count = f.makeIntField('coin_count', '持有货币数量')
    skill_level = f.makeIntField('skill_level', '技能激活层级')
    in_battle = f.makeIntField('in_battle', '是否场内')
    round = f.makeIntField('round', '回合数')
    in_round = f.makeIntField('in_round', '是否人物回合')
    roll_sequence = f.makeIntField('roll_sequence', '掷骰顺序')
    energy = f.makeIntField('energy', '能量点')
    money = f.makeIntField('money', '资金')

    cardID1 = f.makeIntField('cardID1', '预置卡片ID1')
    cardID2 = f.makeIntField('cardID2', '预置卡片ID2')
    cardID3 = f.makeIntField('cardID3', '预置卡片ID3')
    cardID4 = f.makeIntField('cardID4', '预置卡片ID4')
    cardID5 = f.makeIntField('cardID5', '预置卡片ID5')

    skillID1 = f.makeIntField('skilID1', '预置技能ID1')
    skillID2 = f.makeIntField('skilID2', '预置技能ID2')
    skillID3 = f.makeIntField('skilID3', '预置技能ID3')
    skillID4 = f.makeIntField('skilID4', '预置技能ID4')
    skillID5 = f.makeIntField('skilID5', '预置技能ID5')

    use_card = f.makeIntField("use_card", "使用卡片")
    use_card_target = f.makeIntField('use_card_target', '使用卡片对象')
    use_skill = f.makeIntField("use_skill", "使用技能")
    func = f.makeDynamicField('func', '功能定制')

    roll_count = f.makeIntField('roll_count', '骰子数')
    roll_point = f.makeIntField('roll_point', '掷骰点数')
    skill_point = f.makeIntField('skill_point', '天赋点')
    robot_giveup = f.makeIntField('robot_giveup', '机器人认输')
    hero_id = f.makeIntField('hero_id', '英雄ID')
    hero_level = f.makeIntField('hero_level', '等级')
    prop_type1 = f.makeIntField('prop_type1', '道具类型1')
    propID1 = f.makeIntField('propID1', '道具ID1')
    prop_count1 = f.makeIntField('prop_count1', '道具数量1')
    prop_type2 = f.makeIntField('prop_type2', '道具类型2')
    propID2 = f.makeIntField('propID2', '道具ID2')
    prop_count2 = f.makeIntField('prop_count2', '道具数量2')
    prop_type3 = f.makeIntField('prop_type3', '道具类型3')
    propID3 = f.makeIntField('propID3', '道具ID3')
    prop_count3 = f.makeIntField('prop_count3', '道具数量3')
    coin_type1 = f.makeIntField('coin_type1', '货币类型1')
    coin_count1 = f.makeIntField('coin_count1', '货币点数1')
    coin_type2 = f.makeIntField('coin_type2', '货币类型2')
    coin_count2 = f.makeIntField('coin_count2', '货币点数2')
    exp = f.makeIntField('exp', '经验值')
    


class Names(Document):
    """ 名称表 """
    meta = {'collection': 'names'}

    id = f.createIdField()
    n = f.makeStringField('n', '名称')
    sex = f.makeIntField('sex', '性别')
    t = f.makeIntField('t', '类型')


#********** 前端配置 *************#

class Coin2(Document):

    """ 幸运星充值表 """

    meta = {'collection': 'coin2'}

    id = f.createIdField()
    name = f.makeStringField('name', '分类')
    desc = f.makeDynamicField('desc', '简介')
    hot = f.makeIntField('hot', '热卖')
    coin2 = f.makeIntField('coin2', '幸运星')
    t = f.makeIntField('t', '首充翻倍选项')
    old_price = f.makeIntField('old_price', '原价（人民币）')
    price = f.makeIntField('price', '实际价格（人民币）')
    k = f.makeFloatField('k', '折扣')

class IBShop(Document):

    """ IB商城配置表 """

    meta = {'collection': 'ibshop'}

    id = f.createIdField()
    type = f.makeIntField('type', '分类')
    order = f.makeIntField('order', '序号')
    enable = f.makeIntField('enable', '是否显示及可购买')
    
    item_type = f.makeIntField('item_type', '道具分类')
    item_id = f.makeIntField('item_id', '道具ID')
    item_amount = f.makeIntField('item_amount', '道具数量')
    name = f.makeStringField('name', '名字')
    desc = f.makeStringField('desc', '简介')
    coin_type = f.makeIntField('coin_type', '价格类型')
    old_price = f.makeIntField('old_price', '原价（幸运星）')
    price = f.makeIntField('price', '实际价格（幸运星）')
    k = f.makeFloatField('k', '折扣')

    hot = f.makeIntField('hot', '热卖')
    ibunlock = f.makeIntField('ibunlock', '首充解锁')
    limit_type = f.makeIntField("limit_type", "普通限制类型")
    vip_limit = f.makeIntField("vip_limit", "VIP等级限制")
    count_limit_type = f.makeIntField('count_limit_type', '限制次数类型')
    count_limit = f.makeIntField("count_limit", "限制次数")

    limit_begin_date = f.makeIntField("limit_begin_date", "限制开始日期")
    limit_end_date = f.makeIntField("limit_end_date", "限制结束日期")
    limit_begin_time = f.makeIntField("limit_begin_time", "限制开始时间")
    limit_end_time = f.makeIntField("limit_end_time", "限制结束时间")


# 其它系统 #

class Audio(Document):
    """ 音频表 """

    meta = {'collection': 'audio'}

    id = f.createIdField()
    filename = f.makeStringField('filename', "文件名")
    subfilename = f.makeStringField('subfilename', "子文件路径")
    time = f.makeFloatField('time', "时间长度")

class Error(Document):
    """ 错误表 """

    meta = {'collection': 'error'}

    id = f.createIdField()
    info = f.makeTextField('info', '说明')


class Setting(Document):
    """ 设置表  """

    meta = {'collection': 'setting'}

    id = f.createIdField()
    key = f.makeStringField('key', '键')
    value = f.makeTextField('value', '值')


class Server(Document):
    """ Server """

    meta = {'collection': 'server', 'strict': False}

    id = f.createIdField()            
    name = f.makeStringField('name', '集群名称')
    gw   = f.makeStringField('gw', '集群网关')    
    host = f.makeStringField('host', '集群登陆机')
    port = f.makeStringField('port', '集群登陆机端口')
    package_version = f.makeStringField('package_version', '匹配的安装包版本')    
    #sid = f.makeIntField('sid', 'SID')
    # status = f.makeIntField('status', '状态')
    #new = f.makeIntField('new', '是否新服')


class GConfig(Document):
    """ GConfig """

    meta = {'collection': 'gconfig'}

    id = f.createIdField()
    key = f.makeStringField('key', '键')
    value = f.makeDynamicField('value', '值')


class Goods(Document):
    """ 商品 """
    meta = {'collection': 'goods'}
    id = f.createIdField()
    act = f.makeStringField('act', '')
    coin = f.makeIntField('coin', '币数量')
    freeCoin = f.makeIntField('freeCoin', '做活动币数量')
    info = f.makeStringField('info', '信息')
    name = f.makeStringField('name', '名字')
    oprice = f.makeIntField('oprice', '对应价钱')
    price = f.makeIntField('price', '价钱')
    rid = f.makeIntField('rid', '奖励ID')
    sns = f.makeDynamicField('sns', '平台')
    status = f.makeIntField('status', '状态')
    type = f.makeIntField('type', '商品类型')
    snsType = f.makeIntField('snsType', '平台类型')


class Translation(Document):
    """ 翻译 """
    meta = {'collection': 'translation'}
    id = f.createIdField()
    tname = f.makeStringField('tname', '需要翻译表名')
    tfields = f.makeDynamicField('tfields', '翻译的表名')


# MAIN {{{1,
#=============================================================================
models = [
    RewardMail, RankBattle,
    Hero, HeroInfo, Reward, Attr, HeroSkill, DailyTask, DailyTaskEgg, CheckIn, GiftPackage, BattleEgg, CheckinExtraReward,
    Skill, SkillResetCost, RankRefreshCost,
    Npc, Talk, Fate, News, Market, PvpRoomMode,
    Map, Tile, Building, MapModel, MiniGame, MiniGameTips,
    Ai, AiCode, Buff, Robot, Vip, RankReward,
    Card, Item, Dice, Car, Cloth, Enhance, Mall, CardPiece,
    Achieve, AchieveIcon,
    ClientTips, ClientCss, Tips, Message, GuideBoard, GuideMain, Guide, Names, MovieTicket, ExchangeCode,
    Pve, PveBattle, AreaBox, BQuiz,
    Error, Setting,
    Server, GConfig, Goods, Translation,
    Activity, SpActivity, ActivityBattle, ActivityTask, IBShop, Coin2, GuideBattle, GuideBattleMain, Audio,Notifys, 
    LHJ, DDD, ZXL,
]

