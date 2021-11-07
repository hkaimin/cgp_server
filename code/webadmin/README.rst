########
后台系统
########

安装
====

可用 pip 安装一下依赖 ::

    Flask
    Flask-Admin
    Flask-Mongoengine
    Flask-BabelEx
    xlrd
    xlwt
    pycrypto
    redis

运行
====

以项目启动脚本运行
------------------

配置为项目目录的 code/app/webadmin/config.py，可以先导入默认配置，然后按需修改 ::

    SERVER_HOST_PORT = 5000
    SESSION_COOKIE_NAME = 'rich_session'

    from webadmin.web.default_config import *

然后在项目根目录 ::

    python main.py webadmin run

以独立启动脚本运行
------------------

调试用，按需修改 run.py 里的 LocalConfig 配置对象，然后 ::

    python run.py

或者随便加一个参数，连接到公共机的数据库 ::

    python run.py rich

修改数据库模型
==============

数据库
------

目前用到 4 个数据库

* 系统库 system，后台本身用来保存账户和游戏服务器信息的
* 资源库 resource，就是策划配置的资源数据
* 用户库 user，游戏运行产生的玩家数据
* 日志库 logging，游戏运行产生的日志数据

这些数据库的表定义都在 models 目录下对应名字的文件中。

添加新表
--------

假设现在要修改资源库，添加一个新的表 Example，那么编辑 resource.py， 新建一个继承 Document 的类 ::

    class Example(Document):
        ''' [其它系统]示例表 ''' # 用来作为页面标题，必须有

        meta = {'collection': 'example'} # 数据库表名，小写下划线方式，必须有

        id = f.createIdField() # 唯一ID，必须有
        count = f.makeIntField('count', '数量') # 根据对应格式填

对每个字段的格式，例如上面的 count 行：

* ``count`` 字段名，两处（开头和函数参数），都要相同
* ``数量`` 中文名，供策划参考用
* ``f.makeIntField`` 数据类型，用作格式检查和数据转换用

可用的数据类型：

* ``f.makeIntField`` 整型
* ``f.makeStringField`` 字符串
* ``f.makeTextField`` 也是字符串，供输入较多的文本用，HTML 表单会显示成一个 textarea。
* ``f.makeDynamicField`` JSON，数据结构会预先反序列化好存入数据库
* ``f.makeIntListField`` 整型列表，例如 ``[1,2,3]``
* ``f.makePointField`` 整型列表，但是元素数量限制在 2 个，用来表示尺寸/长宽等数据

当定义好这个表类后，把类名添加到文件底部的 models 列表中 ::

    models = [
        Hero,
        Dice, Car,
        Npc, Prop, HeroSkill,
        Map, Tile, Building,
        Ai, AiCode,
        Item, Reward, Cloth, Equip,
        Error, Setting,
        Server, GConfig, Example # 在这里
    ]

同类系统的都写在同一行，重启后台，以 /res/example/ 就能访问这个表的页面了。

添加侧边栏链接
--------------

目前后台顶部 3 大分类的模板都在 templates 目录下，首页分别是

* 资源管理 res.html
* 开发调试 dev.html
* 运营管理 ope.html

在 res.html 给刚才的 Exmaple 添加一个链接 ::

    <div class="nav-subtitle">其它系统</div>
    <ul class="nav nav-list">
        {{ model_menuitem('resource_model_error', '错误表') }}
        {{ model_menuitem('resource_model_setting', '设置表') }}
        {{ model_menuitem('resource_model_server', 'Server') }}
        {{ model_menuitem('resource_model_gconfig', 'GConfig') }}
        {{ model_menuitem('resource_model_example', '示例表') }} # 在这里
    </ul>

``resource_model_example`` 格式是 「数据库名+model+表名」

刷新页面即可，不需要重启后台。
