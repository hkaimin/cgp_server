#!/usr/bin/env python
# -*- coding:utf-8 -*-
EXCHANGE_RATE = 100#汇率：合约币100个=1个游戏内显示，主要用于保留2位有效数
EXHIBITION_EVERY_MINUTE = 10#每分钟产出主币数
TICKET_COST_TYPE = 1 #门票价格消耗类型 1为主币
TICKET_COST_NUM  = 100 #门票价格消耗数量

ENERGY_CONFIG = 100  #游戏体力上限
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

MERGE_COST_MAIN = TICKET_COST_NUM*0.08 #合约的的8%
MERGE_COST_SUB = TICKET_COST_NUM*0.8 #合约的的80%
HIGH_MERGE_COST_MAIN = TICKET_COST_NUM*0.1 #合约的的10%
HIGH_MERGE_COST_SUB = TICKET_COST_NUM*1 #合约的的100%
MERGE_INFO = {#合并相关配置
	1:{
		"lowMerge":{"success":750,"fail":200,"lost":50,"dRate":{750:1,950:2,1000:3}},
		"highMerge":{"success":900,"fail":100,"lost":0,"dRate":{900:1,1000:2,1001:3}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	2:{
		"lowMerge":{"success":600,"fail":250,"lost":150,"dRate":{600:1,850:2,1000:3}},
		"highMerge":{"success":750,"fail":200,"lost":50,"dRate":{750:1,950:2,1000:3}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	3:{
		"lowMerge":{"success":450,"fail":300,"lost":250,"dRate":{450:1,750:2,1000:3}},
		"highMerge":{"success":600,"fail":250,"lost":150,"dRate":{600:1,850:2,1000:3}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	4:{
		"lowMerge":{"success":300,"fail":350,"lost":350,"dRate":{300:1,650:2,1000:3}},
		"highMerge":{"success":450,"fail":300,"lost":250,"dRate":{450:1,750:2,1000:3}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	}
}

BREED_COST_MAIN = TICKET_COST_NUM*0.35#合约的的35%
BREED_COST_SUB = TICKET_COST_NUM*3.5#合约的的350%
HIGH_BREED_COST_MAIN = TICKET_COST_NUM*0.4#合约的的40%
HIGH_BREED_COST_SUB = TICKET_COST_NUM*4#合约的的400%
BREED_INFO = {#繁殖相关配置
	("d","d"):{
		"lowBreed":{"success":900,"fail":100,"dSuccess":{900:1,1000:2},"dRate":{450:"d",900:"d"}},
		"highBreed":{"success":970,"fail":30,"dSuccess":{970:1,1000:2},"dRate":{485:"d",970:"d"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("d","c"):{
		"lowBreed":{"success":850,"fail":150,"dSuccess":{850:1,1000:2},"dRate":{210:"c",850:"d"}},
		"highBreed":{"success":940,"fail":60,"dSuccess":{940:1,1000:2},"dRate":{235:"c",940:"d"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("d","b"):{
		"lowBreed":{"success":800,"fail":200,"dSuccess":{800:1,1000:2},"dRate":{110:"b",800:"d"}},
		"highBreed":{"success":910,"fail":90,"dSuccess":{910:1,1000:2},"dRate":{130:"b",910:"d"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("d","a"):{
		"lowBreed":{"success":750,"fail":250,"dSuccess":{750:1,1000:2},"dRate":{70:"a",750:"d"}},
		"highBreed":{"success":880,"fail":120,"dSuccess":{880:1,1000:2},"dRate":{80:"b",880:"d"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("d","s"):{
		"lowBreed":{"success":700,"fail":300,"dSuccess":{700:1,1000:2},"dRate":{40:"s",600:"d"}},
		"highBreed":{"success":850,"fail":150,"dSuccess":{850:1,1000:2},"dRate":{53:"s",850:"d"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("c","c"):{
		"lowBreed":{"success":850,"fail":150,"dSuccess":{850:1,1000:2},"dRate":{430:"c",850:"c"}},
		"highBreed":{"success":940,"fail":60,"dSuccess":{940:1,1000:2},"dRate":{470:"c",940:"c"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("c","b"):{
		"lowBreed":{"success":800,"fail":200,"dSuccess":{940:1,1000:2},"dRate":{200:"b",800:"c"}},
		"highBreed":{"success":910,"fail":90,"dSuccess":{910:1,1000:2},"dRate":{230:"b",910:"c"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("c","a"):{
		"lowBreed":{"success":750,"fail":250,"dSuccess":{750:1,1000:2},"dRate":{110:"a",750:"c"}},
		"highBreed":{"success":880,"fail":120,"dSuccess":{880:1,1000:2},"dRate":{130:"a",880:"c"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("c","s"):{
		"lowBreed":{"success":750,"fail":250,"dSuccess":{750:1,1000:2},"dRate":{110:"s",750:"c"}},
		"highBreed":{"success":880,"fail":120,"dSuccess":{880:1,1000:2},"dRate":{130:"s",880:"c"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("b","b"):{
		"lowBreed":{"success":800,"fail":200,"dSuccess":{800:1,1000:2},"dRate":{400:"b",800:"b"}},
		"highBreed":{"success":910,"fail":90,"dSuccess":{910:1,1000:2},"dRate":{455:"b",910:"b"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("b","a"):{
		"lowBreed":{"success":750,"fail":250,"dSuccess":{750:1,1000:2},"dRate":{190:"a",750:"b"}},
		"highBreed":{"success":880,"fail":120,"dSuccess":{880:1,1000:2},"dRate":{220:"a",880:"b"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("b","s"):{
		"lowBreed":{"success":700,"fail":300,"dSuccess":{700:1,1000:2},"dRate":{100:"s",700:"b"}},
		"highBreed":{"success":850,"fail":150,"dSuccess":{850:1,1000:2},"dRate":{120:"s",850:"b"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("a","a"):{
		"lowBreed":{"success":700,"fail":300,"dSuccess":{700:1,1000:2},"dRate":{180:"a",700:"a"}},
		"highBreed":{"success":850,"fail":150,"dSuccess":{850:1,1000:2},"dRate":{210:"a",850:"a"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("a","s"):{
		"lowBreed":{"success":700,"fail":300,"dSuccess":{700:1,1000:2},"dRate":{180:"s",700:"a"}},
		"highBreed":{"success":850,"fail":150,"dSuccess":{850:1,1000:2},"dRate":{210:"s",850:"a"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
	("s","s"):{
		"lowBreed":{"success":700,"fail":300,"dSuccess":{700:1,1000:2},"dRate":{350:"s",700:"s"}},
		"highBreed":{"success":850,"fail":150,"dSuccess":{850:1,1000:2},"dRate":{425:"s",850:"s"}},
		"up_rate":{30:70,100:80,200:90,350:100,650:110,800:120,900:130,970:140,1000:150},
	},
}

TRAIN_CONF = {#1拉力 2快跑 3障碍 4快步 5综合
	1:{
		"costEnergy":10,"addList":[2,0,1,0],"costSubCoin":3
	},
	2:{
		"costEnergy":10,"addList":[0,2,0,1],"costSubCoin":3
	},
	3:{
		"costEnergy":10,"addList":[1,0,2,0],"costSubCoin":3
	},
	4:{
		"costEnergy":10,"addList":[0,1,0,2],"costSubCoin":3
	},
	5:{
		"costEnergy":15,"addList":[1,1,1,1],"costSubCoin":4.5
	},
}

#低级打金
CARGO_TRANS = {
	1:{
		"success":800,"dSuccess":{800:1,1000:2},"dRewardArea":[800,1200],"rateToMini":1,"costEnergy":20,
	},
	2:{
		"success":700,"dSuccess":{700:1,1000:2},"dRewardArea":[960,1440],"rateToMini":1.2,"costEnergy":20,
	},
	3:{
		"success":500,"dSuccess":{500:1,1000:2},"dRewardArea":[1320,1980],"rateToMini":1.65,"costEnergy":20,
	},
	4:{
		"success":300,"dSuccess":{300:1,1000:2},"dRewardArea":[2240,3360],"rateToMini":2.8,"costEnergy":20,
	},
}

CARGO_STAR_TRANS = {
	1:{
		"rate":1
	},
	2:{
		"rate":2.5
	},
	3:{
		"rate":6.25
	},
	4:{
		"rate":15.625
	},
	5:{
		"rate":39.0625
	},
}

#-----增加币的事件定义
CLAIM_EXHI_EVENT = 1 #获取质押奖励
CARGO_EVENT = 2 #获取低级打金奖励
PEDDLERY_EVENT = 3 #获取低级打金奖励


