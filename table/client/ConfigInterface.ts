interface ConfigInterface {
	btnConf	:MapDic<IBtnConfConf>;
	openCtrl	:MapDic<IOpenCtrlConf>;
	MapBase	:MapDic<IMapBaseConf>;
	MapConf	:MapDic<IMapConfConf>;
	helpConf	:MapDic<IHelpConfConf>;
	UpgradeData	:MapDic<IUpgradeDataConf>;
	ItemData	:MapDic<IItemDataConf>;
	skillConf	:MapDic<ISkillConfConf>;
	role	:MapDic<IRoleConf>;
	nameConf	:MapDic<INameConfConf>;
	mapsign	:MapDic<IMapsignConf>;
	sevenDayReward	:MapDic<ISevenDayRewardConf>;
	shopData	:MapDic<IShopDataConf>;
	WujinMapConf	:MapDic<IWujinMapConfConf>;
	MiniGameData	:MapDic<IMiniGameDataConf>;
	guildData	:MapDic<IGuildDataConf>;
	gameConf	:MapDic<IGameConfConf>;
	_mapEditConf	:MapDic<any>;
}
interface IBtnConfConf {
	/** 按钮配置 */
	id:string;
	/** 名字 */
	name:string;
	/** 位置（1为右边，2为上面） */
	pos:number;
	/** 是否开启 */
	isOpen:number;
	/** 权重 */
	weight:number;
}
interface IOpenCtrlConf {
	/** 按钮配置 */
	id:number;
	/** 名字 */
	name:string;
	/** 是否开启 */
	isOpen:number;
	/** 开放等级 */
	openLv:number;
}
interface IMapBaseConf {
	/** 地图砖块表 */
	id:number;
	/** 名称 */
	name:string;
	/** 砖块类型 */
	Type:number;
	/** 主题类型 */
	Theme:number;
	/** 所属地图批次（大类型） */
	mapType:number;
	/** 资源名称 */
	res:string;
	/** 主题名称 */
	ThemeName:string;
}
interface IMapConfConf {
	/** 地图关卡 */
	id:number;
	/** 类型 */
	Type:number;
	/** 底图配置 */
	bgconf:Array<number>;
	/** 障碍物 */
	layerconf:Array<number>;
	/** 速度道具数量 */
	itemSpeed:number;
	/** 泡泡数量道具 */
	itemNum:number;
	/** 泡泡威力道具 */
	itemPower:number;
	/** 增加生命道具 */
	itemLife:number;
	/** 刺穿泡泡道具 */
	itemDestory:number;
	/** 防护罩道具 */
	itemDef:number;
	/** 速度道具数量概率 */
	itemSpeedPer:number;
	/** 泡泡数量道具概率 */
	itemNumPer:number;
	/** 泡泡威力道具概率 */
	itemPowerPer:number;
	/** 增加生命道具概率 */
	itemLifePer:number;
	/** 总游戏时常 */
	barrTime:number;
	/** ai数量 */
	aiNum:number;
}
interface IHelpConfConf {
	/** 帮助库 */
	id:number;
	/** 标题 */
	name:string;
	/** 内容 */
	content:string;
}
interface IUpgradeDataConf {
	/** 道具表 */
	id:number;
	/** 经验 */
	exp:number;
	/** 速度 */
	speed:number;
	/** 泡泡威力 */
	power:number;
	/** 泡泡数量 */
	count:number;
	/** 生命 */
	life:number;
	/** 幸运值（随机道具掉好东西的增强概率） */
	luck:number;
	/** 奖励 */
	reward:number;
	/** 数量 */
	rewardNum:number;
}
interface IItemDataConf {
	/** 道具表 */
	id:number;
	/** 名称 */
	name:string;
	/** 类型 */
	Type:number;
	/** 资源名称 */
	res:string;
	/** 可叠加数量 */
	maxAmount:number;
	/** 物品描述 */
	desc:string;
	/** 功能类型 */
	spType:number;
	/** 功能类型参数1 */
	param1:number;
	/** 功能类型参数2 */
	param2:number;
	/** 功能类型参数3 */
	param3:string;
	/** 道具使用持续效果周期 */
	cycle:number;
}
interface ISkillConfConf {
	/** 技能 */
	id:string;
	/** 技能ID */
	skillID:string;
	/** 等级 */
	lv:number;
	/** 是否能开放 */
	isOpen:number;
	/** 升级付费类型 */
	costType:number;
	/** 花费 */
	cost:number;
	/** 效果持续时间 */
	effectTime:number;
	/** 类型 */
	skillType:number;
	/** 数值 */
	param:number;
	/** 数值2 */
	param2:number;
	/** 技能CD */
	cd:number;
	/** 名字 */
	name:string;
}
interface IRoleConf {
	/** 游戏配置 */
	id:number;
	/** 角色名字 */
	name:string;
	/** 角色描述 */
	desc:string;
	/** PVP生命 */
	pvp_life:number;
	/** PVP速度 */
	pvp_speed:number;
	/** PVP威力 */
	pvp_power:number;
	/** PVP数量 */
	pvp_cnt:number;
	/** PVE生命 */
	pve_life:number;
	/** PVE速度 */
	pve_speed:number;
	/** PVE威力 */
	pve_power:number;
	/** PVE数量 */
	pve_cnt:number;
	/** 额外属性 */
	ex_property:string;
	/** 是否上线 */
	isonline:number;
	/** 价钱 */
	price:number;
	/** 支付种类 */
	payType:number;
	/** 小头像 */
	smallHead:string;
	/** 背景图 */
	bgHead:string;
	/** 动画资源 */
	aminRes:string;
}
interface INameConfConf {
	/** 名字库 */
	id:number;
	/** 名字 */
	name:string;
}
interface IMapsignConf {
	/** 游戏配置 */
	id:number;
	/** 角色名字 */
	name:string;
}
interface ISevenDayRewardConf {
	/** 游戏配置 */
	id:number;
	/** 批次 */
	cycle:number;
	/** 名字 */
	day:number;
	/** 展示奖励 */
	show:string;
	/** 奖励 */
	reward:string;
	/** 描述 */
	Exps:string;
}
interface IShopDataConf {
	/** 商品表 */
	id:number;
	/** 关联物品ID */
	itemId:number;
	/** 购买物品数量 */
	buyitemNum:number;
	/** 名称 */
	name:string;
	/** 商品类型(对应物品） */
	Type:number;
	/** 购买类型 */
	buyType:number;
	/** 可购买次数 */
	buycount:number;
	/** 支付类型 */
	payType:number;
	/** 需要金币 */
	coin:number;
	/** 需要钻石 */
	diamond:number;
	/** 需要播放广告次数 */
	ad:number;
	/** 结束时间 */
	endTime:string;
	/** 资源名称 */
	res:string;
	/** 商品描述 */
	desc:string;
}
interface IWujinMapConfConf {
	/** 无尽关卡 */
	id:number;
	/** 第几层关卡 */
	diffLevel:number;
	/** 底图配置 */
	bgconf:Array<number>;
	/** 障碍物 */
	layerconf:Array<number>;
	/** 速度道具数量 */
	itemSpeed:number;
	/** 泡泡数量道具 */
	itemNum:number;
	/** 泡泡威力道具 */
	itemPower:number;
	/** 增加生命道具 */
	itemLife:number;
	/** 刺穿泡泡道具 */
	itemDestory:number;
	/** 防护罩道具 */
	itemDef:number;
	/** 速度道具数量概率 */
	itemSpeedPer:number;
	/** 泡泡数量道具概率 */
	itemNumPer:number;
	/** 泡泡威力道具概率 */
	itemPowerPer:number;
	/** 增加生命道具概率 */
	itemLifePer:number;
	/** 总游戏时常 */
	barrTime:number;
	/** 通关条件类型 */
	itype:number;
	/** 通关条件 {星星数：{类似:通关条件}, …} */
	condition:string;
	/** ai等级 */
	aiLevel:number;
	/** AI生命 */
	aiLife:number;
	/** AI速度 */
	aiSpeed:number;
	/** AI泡泡数量 */
	aiPaoNum:number;
	/** AI泡泡威力 */
	aiPower:number;
	/** ai形象 */
	aiClass:number;
	/** 通关门 */
	lGuanKaDoorIdx:Array<number>;
	/**  怪物探索区域 */
	lMonsterArea:Array<Array<number>>;
	/** 随机怪物等级池 */
	lranMonsterLevel:Array<number>;
	/** 随机怪物形象 */
	dranMonstSkin:string;
	/** 随机怪物速度 */
	dranMonstSpeed:string;
	/** 胜利条件 */
	winCondi:string;
}
interface IMiniGameDataConf {
	/** 小游戏加成表 */
	id:number;
	/** 完成类型 */
	finishType:number;
	/** 点击次数 */
	hitcount:number;
	/** 增加类型 */
	type:number;
	/** 增加参数 */
	param:number;
	/** 描述 */
	desc:string;
}
interface IGuildDataConf {
	/** 新手引导 */
	id:number;
	/** 引导KEY */
	ikey:number;
	/** 步骤 */
	istep:number;
	/** 类型 */
	itype:number;
	/** 界面引导按钮编号 */
	btnkey:number;
	/** 子界面引导编号 */
	innerIndex:number;
	/** 备注 */
	desc:string;
	/** 是否战斗触发 */
	isFight:number;
}
interface IGameConfConf {
	/** 游戏配置 */
	id:string;
	/** 名字 */
	Value:string;
	/** 描述 */
	Exps:string;
}
