#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import random
import game.core.PaoPaoPVP.paopaoPlayer
import weakref


class PaoPaoSkillObj(object):
    def __init__(self, owner, skillID, dSkillInfo):
        self.owner = weakref.proxy(owner)  # 拥有者
        self.skillID = skillID
        self.effectTime = dSkillInfo.get("effectTime", 0)
        self.skillType = dSkillInfo.get("skillType", 0)
        self.param = dSkillInfo.get("param", 0)
        self.param2 = dSkillInfo.get("param2", 0)
        self.cd = dSkillInfo.get("cd", 0)

# 处理技能事件
def dealSkllAttack(attacker, beattacker, skillID):
    # type: (object, object, object) -> object
    skillInfo = attacker.getSkillInfoBySkillID(skillID)
    skillObj = PaoPaoSkillObj(attacker, skillID, skillInfo)
    skillID = skillObj.skillID
    effectTime = skillObj.effectTime
    skillType = skillObj.skillType
    param = skillObj.param
    param2 = skillObj.param2
    cd = skillObj.cd
    dBuff = {}
    if skillType == game.core.skill.conf.CSkillType.REDUCE_SPEED:
        dBuff["speed"] = param*-1
    elif skillType == game.core.skill.conf.CSkillType.REDUCE_PP_CNT:
        dBuff["paopaocnt"] = param*-1
    elif skillType == game.core.skill.conf.CSkillType.REDUCE_POWER:
        dBuff["power"] = param*-1
    print "-----dealSkllAttack----", skillID, effectTime, skillType, param, cd
    if not dBuff:
        return False
    beattacker.dealbuff(skillType, dBuff, effectTime, skillID)
    attacker.setSkillNextUseTime(skillID, cd)
    return True



import game.core.skill.conf