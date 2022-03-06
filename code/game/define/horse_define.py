#!/usr/bin/env python
# -*- coding:utf-8 -*-
TICKET_COST_TYPE = 1 #门票价格消耗类型 1为主币
TICKET_COST_NUM  = 100 #门票价格消耗数量
ENERGY_CONFIG = 100  #游戏体力上限
ENERGY_COST = {#1拉力 2快跑 3障碍 4快步 5综合
	1:10,2:10,3:10,4:10,5:15
} #进行一次马操作的体力消耗
ENERGY_RESUME_CYCLE = 12*60*60 #12小时恢复
LAND_MAX_NUM = 500 #地形最大适应值
HORSE_TYPE_RANDOM = {15:1,30:2,65:3,100:4,175:5,250:6,375:7,500:8,750:9,1000:10} #随机血统概率比例
MARKET_GET = 10 #市场交易百分之10税收
HORSE_BREED_RANDOM = {150:1,450:2,750:3,900:4,970:5,1000:6} #随机繁殖次数上限

HORSE_INFO = { #血统配置 tRandom主属性 tRandom2副属性 tRandom3地形适应
	1:{
		"iType":"s","name":"纯血马","tRandom":(1200,1400),"tRandomSub":(20,30)
		,"res_key":"01","tRandom2":(410,510),"tRandomSub2":(20,30),"tRandom3":(900,1200),"tRandomSub3":(25,33)
	},
	2:{
		"iType":"s","name":"阿拉伯马","tRandom":(1200,1400),"tRandomSub":(20,30)
		,"res_key":"02","tRandom2":(410,510),"tRandomSub2":(20,30),"tRandom3":(900,1200),"tRandomSub3":(25,33)
	},
	3:{
		"iType":"a","name":"安达卢西亚马","tRandom":(800,960),"tRandomSub":(20,30)
		,"res_key":"03","tRandom2":(330,430),"tRandomSub2":(20,30),"tRandom3":(750,1050),"tRandomSub3":(25,33)
	},
	4:{
		"iType":"a","name":"汗诺威马","tRandom":(800,960),"tRandomSub":(20,30)
		,"res_key":"04","tRandom2":(330,430),"tRandomSub2":(20,30),"tRandom3":(750,1050),"tRandomSub3":(25,33)
	},
	5:{
		"iType":"b","name":"夸特马","tRandom":(440,528),"tRandomSub":(20,30)
		,"res_key":"05","tRandom2":(260,360),"tRandomSub2":(20,30),"tRandom3":(600,900),"tRandomSub3":(25,33)
	},
	6:{
		"iType":"b","name":"三河马","tRandom":(440,528),"tRandomSub":(20,30)
		,"res_key":"06","tRandom2":(260,360),"tRandomSub2":(20,30),"tRandom3":(600,900),"tRandomSub3":(25,33)
	},
	7:{
		"iType":"c","name":"奥尔洛夫马","tRandom":(300,360),"tRandomSub":(20,30)
		,"res_key":"07","tRandom2":(200,300),"tRandomSub2":(20,30),"tRandom3":(450,750),"tRandomSub3":(25,33)
	},
	8:{
		"iType":"c","name":"利皮扎马","tRandom":(300,360),"tRandomSub":(20,30)
		,"res_key":"08","tRandom2":(200,300),"tRandomSub2":(20,30),"tRandom3":(450,750),"tRandomSub3":(25,33)
	},
	9:{
		"iType":"d","name":"荷兰温血马","tRandom":(200,240),"tRandomSub":(20,30)
		,"res_key":"09","tRandom2":(150,250),"tRandomSub2":(20,30),"tRandom3":(300,600),"tRandomSub3":(25,33)
	},
	10:{
		"iType":"d","name":"阿帕卢萨马","tRandom":(200,240),"tRandomSub":(20,30)
		,"res_key":"10","tRandom2":(150,250),"tRandomSub2":(20,30),"tRandom3":(300,600),"tRandomSub3":(25,33)
	}
}

