#!/usr/bin/env python
# -*- coding:utf-8 -*-


TICKET_COST_TYPE = 1 #门票价格消耗类型
TICKET_COST_NUM  = 1 #门票价格消耗数量
ENERGY_CONFIG = 100  #游戏体力上限
HORSE_TYPE_RANDOM = {15:1,30:2,65:3,100:4,175:5,250:6,375:7,500:8,750:9,1000:10}
HORSE_INFO = {
	1:{
		"iType":"s","name":"纯血马","strength":132,"MaxStrength":264,"speed":198,"MaxSpeed":396,
		"dexterity":132,"MaxDexterity":264,"burse":198,"MaxBurse":396,"res_key":"01","grassland":"s","sand":"s","mud":"a"
	},
	2:{
		"iType":"s","name":"阿拉伯马","strength":198,"MaxStrength":396,"speed":132,"MaxSpeed":264,
		"dexterity":198,"MaxDexterity":396,"burse":132,"MaxBurse":264,"res_key":"02","grassland":"s","sand":"a","mud":"s"
	},
	3:{
		"iType":"a","name":"安达卢西亚马","strength":88,"MaxStrength":176,"speed":132,"MaxSpeed":264,
		"dexterity":88,"MaxDexterity":176,"burse":132,"MaxBurse":264,"res_key":"03","grassland":"s","sand":"b","mud":"a"
	},
	4:{
		"iType":"a","name":"汗诺威马","strength":132,"MaxStrength":264,"speed":88,"MaxSpeed":176,
		"dexterity":132,"MaxDexterity":264,"burse":88,"MaxBurse":176,"res_key":"04","grassland":"b","sand":"s","mud":"a"
	},
	5:{
		"iType":"b","name":"夸特马","strength":50,"MaxStrength":100,"speed":75,"MaxSpeed":150,
		"dexterity":50,"MaxDexterity":100,"burse":75,"MaxBurse":150,"res_key":"05","grassland":"a","sand":"a","mud":"b"
	},
	6:{
		"iType":"b","name":"三河马","strength":75,"MaxStrength":150,"speed":50,"MaxSpeed":100,
		"dexterity":75,"MaxDexterity":150,"burse":50,"MaxBurse":100,"res_key":"06","grassland":"b","sand":"a","mud":"a"
	},
	7:{
		"iType":"c","name":"奥尔洛夫马","strength":33,"MaxStrength":66,"speed":45,"MaxSpeed":90,
		"dexterity":33,"MaxDexterity":66,"burse":45,"MaxBurse":90,"res_key":"07","grassland":"b","sand":"c","mud":"b"
	},
	8:{
		"iType":"c","name":"利皮扎马","strength":45,"MaxStrength":90,"speed":33,"MaxSpeed":66,
		"dexterity":45,"MaxDexterity":90,"burse":33,"MaxBurse":66,"res_key":"08","grassland":"b","sand":"b","mud":"c"
	},
	9:{
		"iType":"d","name":"荷兰温血马","strength":22,"MaxStrength":44,"speed":33,"MaxSpeed":66,
		"dexterity":22,"MaxDexterity":44,"burse":33,"MaxBurse":66,"res_key":"09","grassland":"c","sand":"c","mud":"d"
	},
	10:{
		"iType":"d","name":"阿帕卢萨马","strength":33,"MaxStrength":66,"speed":22,"MaxSpeed":44,
		"dexterity":33,"MaxDexterity":66,"burse":22,"MaxBurse":44,"res_key":"10","grassland":"c","sand":"d","mud":"c"
	}
}

