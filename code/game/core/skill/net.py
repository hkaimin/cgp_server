#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from game import Game

class SkillPayType(object):
    COIN_TYPE = 1
    DIAMOND_TYPE = 2


# @observable
class netCmd(object):
    # 协议处理模块
    def __init__(self):
        self.SkillData = Game.res_mgr.res_skillDataLv
        self.SkillConfData = Game.res_mgr.res_skillDataConf
        pass

    def getRoleSkillData(self):
        dSkill = self.base.getSkill()
        return dSkill

    # 打开技能升级主界面
    def rc_C2G_Open_MainUI(self):
        dData = {}
        keys = self.SkillData.keys()
        for skillID in keys:
            skillLvData = self.SkillData.get(skillID)
            curLv = self.getCurSkillLv(skillID)
            maxLv = self.getSkillMaxLv(skillID)
            # print skillLvData
            oSkillData = skillLvData.get(curLv)
            name = oSkillData.name
            isOpen = oSkillData.isOpen
            costType = oSkillData.costType
            cost = oSkillData.cost
            effectTime = oSkillData.effectTime
            skillType = oSkillData.skillType
            param = oSkillData.param
            param2 = oSkillData.param2
            cd = oSkillData.cd
            icon = ""
            desc = "当前效果：减少对方速度%s级，持续%s秒，技能恢复时间%s秒"%(param, effectTime, cd)
            if skillType == conf.CSkillType.REDUCE_PP_CNT:
                desc = "当前效果：减少对方泡泡数量%s个，持续%s秒，技能恢复时间%s秒"%(param, effectTime, cd)
            if not dData.has_key(skillID):
                dData[skillID] = {}
            nextObjDesc = self.getNextLvObjDesc(skillID)

            nextdesc = nextObjDesc

            dData[skillID]["name"] = name#"%s Lv.%s"%(name, curLv)
            dData[skillID]["curLv"] = curLv # 当前等级
            dData[skillID]["maxLv"] = maxLv # 最高等级
            dData[skillID]["isOpen"] = isOpen # 是否可以升级
            dData[skillID]["costType"] = costType # 支付类型
            dData[skillID]["cost"] = cost # 价格
            dData[skillID]["icon"] = icon
            dData[skillID]["desc"] = desc  # 当前描述
            dData[skillID]["nextdesc"] = nextdesc #下级描述
        try:
            Game.glog.log2File("openSkill",
                               "%s|%s|%s" % (
                                   self.id, self.Name(), self.data.account))
        except:
            pass
        return dData

    def getNextLvObj(self, skillID):
        curLv = self.getCurSkillLv(skillID)
        maxLv = self.getSkillMaxLv(skillID)
        if curLv >= maxLv:
            return None
        nextLv = curLv + 1
        skillLvData = self.SkillData.get(skillID)
        oNextSkillData = skillLvData.get(nextLv)
        return oNextSkillData

    def getNextLvObjDesc(self, skillID):
        desc = "已满级"
        try:
            oNextSkillData = self.getNextLvObj(skillID)
            effectTime = oNextSkillData.effectTime
            param = oNextSkillData.param
            cd = oNextSkillData.cd
            skillType = oNextSkillData.skillType
            desc = "减少对方速度%s级，持续%s秒，技能恢复时间%s秒"%(param, effectTime, cd)
            if skillType == conf.CSkillType.REDUCE_PP_CNT:
                desc = "减少对方泡泡数量%s个，持续%s秒，技能恢复时间%s秒"%(param, effectTime, cd)
        except:
            pass
        return desc

    # 技能升级
    def rc_C2G_Upgrade(self, SkillID):
        SkillID = str(SkillID)
        curSkillLv = self.getCurSkillLv(SkillID)
        maxSkillLv = self.getSkillMaxLv(SkillID)
        if curSkillLv >= maxSkillLv:
            self.notify("技能已满级!")
            return
        oSkillConfObj = self.getSkillConfObj(SkillID)
        # 消耗金币
        cost = self.getSkillUpCost(SkillID)
        if cost < 0:
            return
        payType = oSkillConfObj.costType
        if payType == SkillPayType.COIN_TYPE:
            print "-------------------cost", cost
            own_coin = self.base.getCoin()
            if own_coin < cost:
                self.notify("金币不足！")
                return
            self.base.setCoin((-1 * cost))
        elif payType == SkillPayType.DIAMOND_TYPE:
            own_diamond = self.base.getDiamond()
            if own_diamond < cost:
                self.notify("钻石不足！")
                return
            self.base.setDiamond((-1 * cost))
        else:
            return
        if curSkillLv < maxSkillLv:
            curSkillLv = curSkillLv + 1
        dSkill = self.getRoleSkillData()
        if not dSkill.has_key(SkillID):
            dSkill[SkillID] = {}
        dSkill[SkillID]["lv"] = curSkillLv
        self.base.setSkill(dSkill)
        dData = self.rc_C2G_Open_MainUI()
        self.broadcast("C2G_Open_MainUI", dData)
        dReflashData = self.base.to_reflash_simple()
        self.broadcast("reflashsimple", dReflashData)
        self.notify("技能升级成功!")
        try:
            Game.glog.log2File("updateSkill",
                               "%s|%s|%s|%s|%s" % (
                                   self.id, self.Name(), self.data.account, SkillID, curSkillLv))
        except:
            pass


    # 技能打包到战斗服
    def packSkilltoFight(self):
        dSkill = self.getRoleSkillData()
        dData = {}
        for skillID, skillInfo in dSkill.iteritems():
            skillLv = skillInfo.get("lv",0)
            skillLvData = self.SkillData.get(skillID)
            maxLv = max(skillLvData.keys())
            if skillLv > maxLv:
                skillLv = maxLv
            oSkillData = skillLvData.get(skillLv)
            effectTime = oSkillData.effectTime
            skillType = oSkillData.skillType
            param = oSkillData.param
            cd = oSkillData.cd
            if not dData.has_key(skillID):
                dData[skillID] = {}
            dData[skillID]["skillType"] = skillType
            dData[skillID]["param"] = param
            dData[skillID]["effectTime"] = effectTime
            dData[skillID]["cd"] = cd
        print "-----------packSkilltoFight---------->>>", dData
        return dData

    # 获取当前技能ID
    # ud game.core.skill.net
    def getCurSkillLv(self, SkillID):
        SkillID = str(SkillID)
        dSkill = self.getRoleSkillData()
        print "0-0000000000000upSkill",dSkill
        # lv = dSkill.get(SkillID, 0)
        dSkill = dSkill.get(SkillID, {})
        lv = dSkill.get("lv", 0)
        return lv

    # 获取技能升级价钱
    def getSkillUpCost(self, SkillID):
        curSkillLv = self.getCurSkillLv(SkillID)
        skillLvData = self.SkillData.get(SkillID)
        oSkillData = skillLvData.get(curSkillLv, None)
        print "---------->>>>>> ????", oSkillData, oSkillData.cost
        if not oSkillData:
            return -1
        cost = oSkillData.cost
        return cost

    # 获取技能升级支付类型
    def getSkillConfObj(self, SkillID):
        curSkillLv = self.getCurSkillLv(SkillID)
        skillLvData = self.SkillData.get(SkillID)
        oSkillData = skillLvData.get(curSkillLv, None)
        return oSkillData

    def getSkillMaxLv(self, SkillID):
        skillLvData = self.SkillData.get(SkillID)
        lvKeys = skillLvData.keys()
        maxLv = max(lvKeys)
        return maxLv

    def loadRoleSkillInfo(self):
        pass



import game.core.shop
import conf