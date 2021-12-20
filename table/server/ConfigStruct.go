package main
type ConfigData struct {
	BtnConf map[string]*BtnConfConfVO
	OpenCtrl map[string]*OpenCtrlConfVO
	MapBase map[string]*MapBaseConfVO
	MapConf map[string]*MapConfConfVO
	HelpConf map[string]*HelpConfConfVO
	UpgradeData map[string]*UpgradeDataConfVO
	ItemData map[string]*ItemDataConfVO
	SkillConf map[string]*SkillConfConfVO
	Role map[string]*RoleConfVO
	NameConf map[string]*NameConfConfVO
	Mapsign map[string]*MapsignConfVO
	SevenDayReward map[string]*SevenDayRewardConfVO
	ShopData map[string]*ShopDataConfVO
	WujinMapConf map[string]*WujinMapConfConfVO
	MiniGameData map[string]*MiniGameDataConfVO
	GuildData map[string]*GuildDataConfVO
	GameConf map[string]*GameConfConfVO
}
type BtnConfConfVO struct{
	// 按钮配置 
	Id string;
	// 名字 
	Name string;
	// 位置（1为右边，2为上面） 
	Pos int64;
	// 是否开启 
	IsOpen int64;
	// 权重 
	Weight int64;
}
type OpenCtrlConfVO struct{
	// 按钮配置 
	Id int64;
	// 名字 
	Name string;
	// 是否开启 
	IsOpen int64;
	// 开放等级 
	OpenLv int64;
}
type MapBaseConfVO struct{
	// 地图砖块表 
	Id int64;
	// 名称 
	Name string;
	// 砖块类型 
	Type int64;
	// 主题类型 
	Theme int64;
	// 所属地图批次（大类型） 
	MapType int64;
	// 资源名称 
	Res string;
	// 主题名称 
	ThemeName string;
}
type MapConfConfVO struct{
	// 地图关卡 
	Id int64;
	// 类型 
	Type int64;
	// 底图配置 
	Bgconf []int64;
	// 障碍物 
	Layerconf []int64;
	// 速度道具数量 
	ItemSpeed int64;
	// 泡泡数量道具 
	ItemNum int64;
	// 泡泡威力道具 
	ItemPower int64;
	// 增加生命道具 
	ItemLife int64;
	// 刺穿泡泡道具 
	ItemDestory int64;
	// 防护罩道具 
	ItemDef int64;
	// 速度道具数量概率 
	ItemSpeedPer int64;
	// 泡泡数量道具概率 
	ItemNumPer int64;
	// 泡泡威力道具概率 
	ItemPowerPer int64;
	// 增加生命道具概率 
	ItemLifePer int64;
	// 总游戏时常 
	BarrTime int64;
	// ai数量 
	AiNum int64;
}
type HelpConfConfVO struct{
	// 帮助库 
	Id int64;
	// 标题 
	Name string;
	// 内容 
	Content string;
}
type UpgradeDataConfVO struct{
	// 道具表 
	Id int64;
	// 经验 
	Exp int64;
	// 速度 
	Speed int64;
	// 泡泡威力 
	Power int64;
	// 泡泡数量 
	Count int64;
	// 生命 
	Life int64;
	// 幸运值（随机道具掉好东西的增强概率） 
	Luck int64;
	// 奖励 
	Reward int64;
	// 数量 
	RewardNum int64;
}
type ItemDataConfVO struct{
	// 道具表 
	Id int64;
	// 名称 
	Name string;
	// 类型 
	Type int64;
	// 资源名称 
	Res string;
	// 可叠加数量 
	MaxAmount int64;
	// 物品描述 
	Desc string;
	// 功能类型 
	SpType int64;
	// 功能类型参数1 
	Param1 int64;
	// 功能类型参数2 
	Param2 int64;
	// 功能类型参数3 
	Param3 string;
	// 道具使用持续效果周期 
	Cycle int64;
}
type SkillConfConfVO struct{
	// 技能 
	Id string;
	// 技能ID 
	SkillID string;
	// 等级 
	Lv int64;
	// 是否能开放 
	IsOpen int64;
	// 升级付费类型 
	CostType int64;
	// 花费 
	Cost int64;
	// 效果持续时间 
	EffectTime float64;
	// 类型 
	SkillType int64;
	// 数值 
	Param int64;
	// 数值2 
	Param2 int64;
	// 技能CD 
	Cd int64;
	// 名字 
	Name string;
}
type RoleConfVO struct{
	// 游戏配置 
	Id int64;
	// 角色名字 
	Name string;
	// 角色描述 
	Desc string;
	// PVP生命 
	Pvp_life int64;
	// PVP速度 
	Pvp_speed int64;
	// PVP威力 
	Pvp_power int64;
	// PVP数量 
	Pvp_cnt int64;
	// PVE生命 
	Pve_life int64;
	// PVE速度 
	Pve_speed int64;
	// PVE威力 
	Pve_power int64;
	// PVE数量 
	Pve_cnt int64;
	// 额外属性 
	Ex_property string;
	// 是否上线 
	Isonline int64;
	// 价钱 
	Price int64;
	// 支付种类 
	PayType int64;
	// 小头像 
	SmallHead string;
	// 背景图 
	BgHead string;
	// 动画资源 
	AminRes string;
}
type NameConfConfVO struct{
	// 名字库 
	Id int64;
	// 名字 
	Name string;
}
type MapsignConfVO struct{
	// 游戏配置 
	Id int64;
	// 角色名字 
	Name string;
}
type SevenDayRewardConfVO struct{
	// 游戏配置 
	Id int64;
	// 批次 
	Cycle int64;
	// 名字 
	Day int64;
	// 展示奖励 
	Show string;
	// 奖励 
	Reward string;
	// 描述 
	Exps string;
}
type ShopDataConfVO struct{
	// 商品表 
	Id int64;
	// 关联物品ID 
	ItemId int64;
	// 购买物品数量 
	BuyitemNum int64;
	// 名称 
	Name string;
	// 商品类型(对应物品） 
	Type int64;
	// 购买类型 
	BuyType int64;
	// 可购买次数 
	Buycount int64;
	// 支付类型 
	PayType int64;
	// 需要金币 
	Coin int64;
	// 需要钻石 
	Diamond int64;
	// 需要播放广告次数 
	Ad int64;
	// 结束时间 
	EndTime string;
	// 资源名称 
	Res string;
	// 商品描述 
	Desc string;
}
type WujinMapConfConfVO struct{
	// 无尽关卡 
	Id int64;
	// 第几层关卡 
	DiffLevel int64;
	// 底图配置 
	Bgconf []int64;
	// 障碍物 
	Layerconf []int64;
	// 速度道具数量 
	ItemSpeed int64;
	// 泡泡数量道具 
	ItemNum int64;
	// 泡泡威力道具 
	ItemPower int64;
	// 增加生命道具 
	ItemLife int64;
	// 刺穿泡泡道具 
	ItemDestory int64;
	// 防护罩道具 
	ItemDef int64;
	// 速度道具数量概率 
	ItemSpeedPer int64;
	// 泡泡数量道具概率 
	ItemNumPer int64;
	// 泡泡威力道具概率 
	ItemPowerPer int64;
	// 增加生命道具概率 
	ItemLifePer int64;
	// 总游戏时常 
	BarrTime int64;
	// 通关条件类型 
	Itype int64;
	// 通关条件 {星星数：{类似:通关条件}, …} 
	Condition string;
	// ai等级 
	AiLevel int64;
	// AI生命 
	AiLife int64;
	// AI速度 
	AiSpeed int64;
	// AI泡泡数量 
	AiPaoNum int64;
	// AI泡泡威力 
	AiPower int64;
	// ai形象 
	AiClass int64;
	// 通关门 
	LGuanKaDoorIdx []int64;
	//  怪物探索区域 
	LMonsterArea [][]int64;
	// 随机怪物等级池 
	LranMonsterLevel []int64;
	// 随机怪物形象 
	DranMonstSkin string;
	// 随机怪物速度 
	DranMonstSpeed string;
	// 胜利条件 
	WinCondi string;
}
type MiniGameDataConfVO struct{
	// 小游戏加成表 
	Id int64;
	// 完成类型 
	FinishType int64;
	// 点击次数 
	Hitcount int64;
	// 增加类型 
	Type int64;
	// 增加参数 
	Param int64;
	// 描述 
	Desc string;
}
type GuildDataConfVO struct{
	// 新手引导 
	Id int64;
	// 引导KEY 
	Ikey int64;
	// 步骤 
	Istep int64;
	// 类型 
	Itype int64;
	// 界面引导按钮编号 
	Btnkey int64;
	// 子界面引导编号 
	InnerIndex int64;
	// 备注 
	Desc string;
	// 是否战斗触发 
	IsFight int64;
}
type GameConfConfVO struct{
	// 游戏配置 
	Id string;
	// 名字 
	Value string;
	// 描述 
	Exps string;
}
