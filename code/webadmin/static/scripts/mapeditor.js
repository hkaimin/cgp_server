$(function(){
'use strict';

/*
 * 命名规则
 * ========
 *
 * grid: 叫「格子」，指 HTML DOM 上的一个矩形 Node
 * tile: 叫「地格」，指 Javascript 上的对象
 *
 * 一个 tile 绑定到一个 grid 上
 *
 */

/* 信息显示 */

// 工具栏接口
var Toolbar = {

    // 显示提示信息
    showAlertMessage: function(type, message) {
        $('#alert-area')
            .attr('class', 'alert alert-' + type)
            .text(message)
            .show().delay(3000).fadeOut(1000);
    },

    // 更新地图信息
    updateMapInfo: function(id, name, mapSize) {
        $('#info-area .value-id').text(id);
        $('#info-area .value-name').text(name);
        $('#info-area .value-size').text(mapSize.join('x'));
    },

    // 类似上面，但仅仅更新地图大小信息
    updateSizeInfo: function(mapSize) {
        $('#info-area .value-size').text(mapSize.join('x'));
    },

};

// 工作区接口
var Wokspace = {

    // 显示无效地图ID错误
    showNoMapError: function(mapId) {
        var errorInfo = $('<p>').addClass('text-error')
                                .text('当前地图ID无效。')
        $('.gridster').empty().append(errorInfo);
    },

    // 显示未设置地图大小的链接
    showNoMapSizeError: function(mapId) {
        var editUrl = '../map/edit/?id=' + mapId + '#mapSize';
        var editLink = $('<a>').attr('href', editUrl)
                                .text('编辑地图属性');
        var errorInfo = $('<p>').addClass('text-error')
                                .text('未设置地图大小，')
                                .append(editLink);
        $('.gridster').empty().append(errorInfo);
    },

};

/* 各种 API */

// 地格对象接口

var tileApi = {

    // 地格详情属性条目
    createGridDetailEntry: function(tile, attr) {
        var key = attr[0];
        var name = attr[1];
        var value = tile[key];
        var titleNode = $('<span>').addClass('title')
                                   .text(name + '(' + key + '):');
        var valueNode = $('<span>').addClass('value').text(value);
        var entryNode = $('<div>').addClass('.entry')
                                  .append(titleNode)
                                  .append(valueNode);
        return entryNode;
    },

    // 创建悬停时显示的地格详情
    createGridDetailHTML: function(tile) {
        var attrs = [
            ['name', '名称'],
            ['info', '简介'],
            ['act', '动作'],
            ['route', '路由'],
            ['bid', '建筑物'],
            ['price', '基础地价'],
            ['area', '所属地域'],
            ['street', '所属街'],
            ['mark', '地标建筑动画'],
            ['owner', '初始主人'],
            ['car', '赛车场车型'],
        ];

        var detailNode = $('<div>').addClass('tile-detail');
        var self = this;
        $.each(attrs, function(i, attr) {
            detailNode.append(self.createGridDetailEntry(tile, attr));
        });
        return detailNode[0].outerHTML;
    },

};

// 格子接口，只处理单个格子

var Grid = {

    // 获取格子的序号
    getGridTid: function(grid, mapSize) {
        var width = mapSize[0];
        var pos = this.getGridPos(grid);
        var tid = pos[0] + width * pos[1];
        return tid + 1; // 从 1 开始
    },

    // 获取格子的位置
    getGridPos: function(grid) {
        // girdster 以 (1,1) 开始，偏移回 (0,0)
        var posX = grid.attr('data-col') - 1;
        var posY = grid.attr('data-row') - 1;
        return [posX, posY];
    },

    // 更新格子的基本摘要信息（地域、名称、基础地价）
    updateGridBaseSummary: function(grid) {
        var tile = grid.data('tile');
        if (tile._isSaved) {
            if (tile.bid == 0) {
                grid.removeAttr('data-value-area')
            } else {
                grid.attr('data-value-area', tile.area);
            }
            grid.find('.tile-summary .value-name').text(tile.name);
            grid.find('.tile-summary .value-price').text('$' + tile.price);
        }
    },

    // 更新格子的坐标信息（位置和序号）
    updateGridCoordinateSummary: function(grid, mapSize) {
        var tid = this.getGridTid(grid, mapSize);
        var pos = this.getGridPos(grid, mapSize);
        grid.find('.tile-summary .value-tid').text('#' + tid);
        grid.find('.tile-summary .value-pos').text('(' + pos + ')');
        // 写入到对应  tile 对象里
        var tile = grid.data('tile');
        tile.tid = tid;
        tile.pos = pos;
    }
};

// 表单字段验证

var fieldApi = {

    shouldBeInt: function(value) {
        return /^[0-9]+$/.test(value);
    },

    shouldBeJSON: function(value) {
        if (value == "") {
            return true;
        }
        try {
            JSON.parse(value);
        } catch(e) {
            return false;
        }
        return true;
    },

    shouldBeIntList: function(value) {
        try {
            JSON.parse('[' + value + ']');
        } catch(e) {
            return false;
        }
        return true;
    },

    // 自定义一个格式化 JSON 字符串的函数
    prettyJson: function(value) {
        // 已经格式化过了
        if (value.indexOf('{\n') === 0) {
            return value
        }
        return value.replace(/"/g, '\n    "')
                    .replace(/\n    ":/g, '": ')
                    .replace(/}/g, '\n}');
    },

};

var Utils = {

    groupTileDatasByTid: function(tileDatas) {
        var group = {};
        $.each(tileDatas, function(i, tileData) {
            group[tileData.tid] = tileData;
        });
        return group;
    },

    groupGridsByTid: function(grids) {
        var group = {};
        $.each(grids, function(i, node) {
            var grid = $(node);
            var tile = grid.data('tile');
            group[tile.tid] = grid;
        });
        return group;
    },


    actualCoordinate: function(value) {
        return 54 * value + 2;
    },

    centerCoordinate: function(value) {
        return 56 / 2 + this.actualCoordinate(value);
    },

};

/* 全局对象 */

var mapEditor = {
    gridsterApi: null,
    mapId: null,
    mapSize: null,
    recalcMapSize: function() {
        var items = this.gridsterApi.serialize();
        var maxCol = 0;
        var maxRow = 0;
        $.each(items, function(i, item) {
            if (item.col > maxCol) { maxCol = item.col; }
            if (item.row > maxRow) { maxRow = item.row; }
        });
        this.mapSize = [maxCol, maxRow];
    },
};
window.mapEditor = mapEditor; // 顺便注册到 window 中去

// 编辑器接口，批量处理多个格子

var mapEditorApi = {

    // 根据地图大小创建格子
    createGrids: function() {
        var mapSize = mapEditor.mapSize;
        var width = mapSize[0];
        var height = mapSize[1];
        var grids = [];
        var x, y, grid;
        for (y = 1; y <= height; y += 1) {
            for (x = 1; x <= width; x += 1) {
                grid = this.newGrid(x, y);
                grids.push(grid);
            }
        }
        return grids;
    },

    // 创建一个格子
    newGrid: function(x, y) {
        var grid = $('<li>').addClass('grid')
                            .attr('data-col', x)
                            .attr('data-row', y)
                            .attr('data-sizex', 1)
                            .attr('data-sizey', 1);

        // 摘要信息
        var summary = $('<div>').addClass('tile-summary')
                .append($('<div>').addClass('value-tid').text('-1'))
                .append($('<div>').addClass('value-pos').text('(x,y)').hide())
                .append($('<div>').addClass('value-name'))
                .append($('<div>').addClass('value-price'))
                .appendTo(grid);

        return grid;
    },


    // 更新所有格子的摘要信息
    updateAllGrids: function() {
        $('.grid').each(function(i, node) {
            var grid = $(node);
            Grid.updateGridBaseSummary(grid);
            Grid.updateGridCoordinateSummary(grid, mapEditor.mapSize);
        });
    },

    // 创建 tiles 地格对象列表
    createTiles: function(tileDatas) {
        var mapSize = mapEditor.mapSize;
        var group = Utils.groupTileDatasByTid(tileDatas);
        var tiles = [];
        var count = mapSize[0] * mapSize[1];
        var i, tid, tile;
        for (i = 0; i < count; i += 1) {
            // 序号从 1 开始
            tid = i + 1;
            tile = this.newTile(tid, group[tid]);
            tiles.push(tile);
        }
        return tiles;
    },

    // 创建 tile 对象
    newTile: function(tid, tileData) {
        var tile = {
            mid: mapId,
            tid: tid,
            name: '',
            info: '',
            act: '',
            route: '',
            bid: 0,
            price: 0,
            area: 0,
            street: 0,
            mark: '',
            owner: 0,
            car: 0,
            _isSaved: false,
        };

        // 如果数据库没有预先的定义的，就直接返回这个默认值的对象
        if (tileData === undefined) {
            return tile;
        }

        // 用数据库定义的值覆盖
        tile.name = tileData.name || '';
        tile.info = tileData.info || '';
        tile.act = tileData.act || '';
        tile.route = tileData.route && JSON.stringify(tileData.route) || '';
        tile.bid = tileData.bid || 0;
        tile.price = tileData.price || 0;
        tile.area = tileData.area || 0;
        tile.street = tileData.street || 0;
        tile.mark = tileData.mark || '';
        tile.owner = tileData.owner || 0;
        tile.car = tileData.car || 0;
        tile._isSaved = true;
        return tile;
    },

    // 把 tile 对象绑定到 grid 节点
    bindTileToGrids: function(tiles, grids) {
        $.each(tiles, function(i, tile) {
            grids[i].data('tile', tile);
        });
    },

    // 绑定鼠标事件
    bingGridEvents: function(grid) {
        var self = this;

        // 双击编辑格子
        grid.dblclick(function(event) {
            if (!event.ctrlKey) {
                self.editGrid(grid);
            }
        });

        // Ctrl+单击，移除格子
        grid.click(function(event) {
            if (event.ctrlKey) {
                self.removeGrid(grid);
            }
        });

        // 鼠标悬停，显示地格信息
        grid.popover({
            trigger: 'hover',
            container: 'body',
            delay: { show: 500, hide: 0 },
            html: true,
            content: function() {
                return tileApi.createGridDetailHTML(grid.data('tile'));
            }
        });
    },

    // 验证表单输入
    validateField: function() {
        var field = $(this);
        var name = field.attr('name');
        var value = field.val();

        // 各属性格式
        var validatorMapping = {
            name: null,
            info: null,
            act: null,
            route: fieldApi.shouldBeJSON,
            bid: fieldApi.shouldBeInt,
            price: fieldApi.shouldBeInt,
            area: fieldApi.shouldBeInt,
            street: fieldApi.shouldBeInt,
            owner: fieldApi.shouldBeInt,
            car: fieldApi.shouldBeInt,
            mark: null,
        };

        // 验证
        var validator = validatorMapping[name];
        var passValidate = !validator || validator(value);

        // 错误回显
        var controlGroup = field.parents('.control-group');
        if (passValidate) {
            controlGroup.removeClass('error');
        } else {
            controlGroup.addClass('error');
        }

        // 是否全部通过验证
        var allPass = $('.control-group.error').length === 0;

        // 激活/禁用「提交」按钮
        var submitBtn = $('#tile-dialog button[type="submit"]');
        if (allPass) {
            submitBtn.attr('disabled', null);
        } else {
            submitBtn.attr('disabled', true);
        }
    },

    // 获取编辑器的地格数据文本，可以直接提交到服务器
    dumpEditorData: function() {
        var mapMeta = {mapSize: mapEditor.mapSize};

        var tileDatas = [];
        $('.grid').each(function(i, node) {
            var grid = $(node);
            var tile = grid.data('tile');

            // 不要保存没数据的格子
            if (!tile._isSaved) {
                return;
            }

            var tileData = {
                tid: tile.tid,
                pos: tile.pos,
                name: tile.name,
                info: tile.info,
                act: tile.act,
                route: tile.route==="" ? "" : JSON.parse(tile.route), // 本身是个字符串，转换为 JSON
                bid: parseInt(tile.bid),
                price: parseInt(tile.price),
                area: parseInt(tile.area),
                street: parseInt(tile.street),
                owner: parseInt(tile.owner),
                car: parseInt(tile.car),
                mark: tile.mark,
            }
            tileDatas.push(tileData);
        });

        var editorData = {
            map: mapMeta,
            tiles: tileDatas,
        }

        return JSON.stringify(editorData, null, '    ');
    },

    /* 操作格子 { */

    // 编辑格子
    editGrid: function(grid) {
        var tile = grid.data('tile');
        var dialog = $('#tile-dialog');
        var fields = dialog.find('input[name], select[name], textarea[name]');
        var form = dialog.find('form');

        // 设置表单对话框标题头
        dialog.find('.tid').text('#' + tile.tid);
        dialog.find('.pos').text('(' + tile.pos + ')');

        var self = this;

        // 给每个属性输入框设定预设值
        fields.each(function(i, node) {
            var field = $(node);
            var name = field.attr('name');
            var value = tile[name];

            // 路由表特殊处理一下
            if (name === 'route'){
                value = fieldApi.prettyJson(value);
            }

            // 设定值，去掉之前的错误回显（如果有）
            field.val(value);
            field.parents('.control-group').removeClass('error');

            // 监听修改事件，触发检查器
            field.off('change');
            field.on('change', self.validateField);
            self.validateField.apply(node);
        });

        //监听重置事件
        $('#reset-btn').click(function() {
            dialog.find("[name='name']").val("");
            dialog.find("[name='info']").val("");
            dialog.find("[name='act']").val("");
            dialog.find("[name='route']").val("");
            dialog.find("[name='bid']").val(0);
            dialog.find("[name='price']").val(0);
            dialog.find("[name='area']").val(0);
            dialog.find("[name='street']").val(0);
            dialog.find("[name='mark']").val("");
            dialog.find("[name='owner']").val(0);
            dialog.find("[name='car']").val(0);
        });

        // 监听提交事件
        form.off('submit');
        form.on('submit', function() {
            // 可以隐藏掉对话框了
            dialog.modal('hide');

            // 把修改的值写入到绑定的 tile 对象
            fields.each(function(i, node) {
                var field = $(node);
                var name = field.attr('name');
                tile[name] = field.val();
            });

            // 这个属性被设置为 true，才会保存到数据库
            tile._isSaved = true;

            // 更新基本摘要信息
            Grid.updateGridBaseSummary(grid);

            return false;
        });

        // 显示对话框
        dialog.modal('show');
    },

    // 删除格子
    removeGrid: function(grid) {
        var self = this;
        mapEditor.gridsterApi.remove_widget(grid, function() {
            // 如果悬停的详情正在显示，把他去掉
            $('.popover').remove();
            // 地图大小可能改变了，更新格子
            mapEditor.recalcMapSize();
            self.updateAllGrids();
            Toolbar.updateSizeInfo(mapEditor.mapSize);
        });
    },

};

var initEditor = function(mapMeta, tileDatas) {

    // 更新地图信息
    mapEditor.mapId = mapMeta.mapId;
    mapEditor.mapName = mapMeta.mapName;
    mapEditor.mapSize = mapMeta.mapSize;
    Toolbar.updateMapInfo(mapEditor.mapId, mapEditor.mapName, mapEditor.mapSize);

    // 创建格子结构
    var grids = mapEditorApi.createGrids();
    var gridBox = $('<ul>').append(grids);
    $('.gridster').empty().append(gridBox);

    // 应用拖曳碰撞库
    var gridsterApi = gridBox.gridster({

        // 不自动创建格子的 CSS，避免添加格子时越来越慢
        // https://github.com/ducksboard/gridster.js/issues/166
        autogenerate_stylesheet: false,

        widget_margins: [2, 2], // 每个格子的间隔
        widget_base_dimensions: [50, 50], // 每个格子的大小
        draggable: {
            stop: function(event, ui) {
                mapEditor.recalcMapSize();
                mapEditorApi.updateAllGrids();
                Toolbar.updateSizeInfo(mapEditor.mapSize);
            }
        }
    }).data('gridster');

    // 手动创建一次格子的 CSS
    gridsterApi.generate_stylesheet();

    mapEditor.gridsterApi = gridsterApi;

    // 把地格绑定到格子中去
    var tiles = mapEditorApi.createTiles(tileDatas);
    mapEditorApi.bindTileToGrids(tiles, grids);
    $.each(grids, function(i, grid) {
        mapEditorApi.bingGridEvents(grid);
    });

    // 根据地格属性，更新格子信息
    mapEditorApi.updateAllGrids();
};

// 工具栏按钮及动作
var initButtons = function() {

    // 保存
    $('#save-btn').click(function() {

        var editorData = mapEditorApi.dumpEditorData();
        console.log(editorData);

        $.ajax({
            type: 'POST',
            url: 'map/' + mapId,
            contentType: 'application/json; charset=utf-8',
            data: editorData
        }).done(function(data) {
            if (data.success) {
                Toolbar.showAlertMessage('success', '保存成功');
            } else {
                Toolbar.showAlertMessage('error', '保存失败');
            }
        });

    });

    // 显示坐标（tid 和 pos 之间切换)
    $('#toggle-coordinate-btn').click(function() {
        var button = $(this);
        if (button.hasClass('active')) {
            $('.tile-summary .value-pos').hide();
            $('.tile-summary .value-tid').show();
        } else {
            $('.tile-summary .value-pos').show();
            $('.tile-summary .value-tid').hide();
        }
    });

    // 路由路径
    $('#toggle-routepath-btn').click(function() {
        var button = $(this);
        var layer = $('#routepath-layer')

        // 显示 -> 隐藏
        // 隐藏时清空当前的路径，下次显示时重算
        if (button.hasClass('active')) {
            layer.find('svg').empty();
            layer.hide();
            return;
        }

        /* d3.js 各种处理 */

        // 初始化 svg，定义一个箭头格式
        var svg = d3.select('#routepath-layer svg');
        svg.append('defs').append('marker')
            .attr('id', 'arrow')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 14)
            .attr('refY', 0)
            .attr('markerWidth', 4)
            .attr('markerHeight', 4)
            .attr('orient', 'auto')
        .append('path')
            .attr('d', 'M0,-5 L10,0 L0,5');

        // 从路由数据取得路径数据
        var mapSize = mapEditor.mapSize;
        var pathData = [];
        var grids = Utils.groupGridsByTid($('.grid'));
        var newPath = function(fromTile, toTile) {
            var path = {
                x1: fromTile.pos[0],
                y1: fromTile.pos[1],
                x2: toTile.pos[0],
                y2: toTile.pos[1],
                colorIndex: toTile.tid,
            }
            return path;
        }
        $.each(grids, function(i, node) {
            var grid = $(node);
            var fromTile = grid.data('tile');

            // 也不处理未标记为保存的地格
            if (!fromTile._isSaved || !fromTile.bid) {
                return;
            }

            var routeObject = JSON.parse(fromTile.route);
            var routeType = typeof(routeObject);
            var path, toTile, tids;

            if (routeType === 'number') {
                // 简单的整数形式，直路
                toTile = $(grids[routeObject]).data('tile');
                if (toTile !== undefined) {
                    path = newPath(fromTile, toTile);
                    pathData.push(path);
                }
            } else {
                // 对象形式，岔路
                tids = $.map(routeObject, function(i, v) {
                    return routeObject[v];
                });
                $.each(tids, function(i, tid) {
                    toTile = $(grids[tid]).data('tile');
                    if (toTile !== undefined) {
                        path = newPath(fromTile, toTile);
                        pathData.push(path);
                    }
                });
            }
        });

        // 画路径
        var pathColors = d3.scale.category20();
        var path = svg.selectAll('path.link').data(pathData);
        path.enter().append('path')
            .attr('d', function(d) {
                var x1 = Utils.centerCoordinate(d.x1);
                var y1 = Utils.centerCoordinate(d.y1);
                var x2 = Utils.centerCoordinate(d.x2);
                var y2 = Utils.centerCoordinate(d.y2);
                return 'M ' + x1 + ',' + y1 + 'L ' + x2 + ',' + y2;
            })
            .attr('class', 'link')
            .attr('stroke', function(d) {
                return d3.rgb(pathColors(d.colorIndex));
            })
            .attr('marker-end', 'url(#arrow)');

        // 从路径数据取得圆圈数据
        var circleData = (function() {
            var i;
            var points = [];
            $.each(pathData, function(i, path) {
                var point1 = path.x1 + ',' + path.y1;
                var point2 = path.x2 + ',' + path.y2;

                // 只需要添加一次
                if (points.indexOf(point1) === -1) {
                    points.push(point1);
                }
                if (points.indexOf(point2) === -1) {
                    points.push(point2);
                }
            });
            return points.map(function(v) { return v.split(',') });
        })();

        // 画圆圈
        var circle = svg.selectAll('circle').data(circleData);
        circle.enter().append('circle')
              .attr('cx', function(d) { return Utils.centerCoordinate(d[0]) })
              .attr('cy', function(d) { return Utils.centerCoordinate(d[1]) })
              .attr('r', 6);

        // 把 svg 图层显示出来
        var gridster = $('.gridster');
        var usedWidth = Utils.centerCoordinate(mapSize[0]);
        layer.find('svg')
                .width(usedWidth)
                .height(gridster.height());
        layer.show();

    });

    $('#toggle-isometric-btn').click(function() {
        var button = $(this);
        var workspace = $('#workspace');
        var mapSize = mapEditor.mapSize;
        var usedWidth = Utils.actualCoordinate(mapSize[0]);
        var usedHeight = Utils.actualCoordinate(mapSize[1]);
        var halfWidth = usedWidth * 0.5
        var halfHeight = usedHeight * 0.5
        var radius = Math.pow(
                        Math.pow(halfWidth, 2) + Math.pow(halfHeight, 2), 0.5);

        var offset = halfWidth / halfHeight * 0.3;
        if (button.hasClass('active')) {
            workspace.removeClass('isometric');
            workspace.css('width', 'auto');
            workspace.css('margin-left', 'auto');
            workspace.css('margin-top', 'auto');
        } else {
            workspace.addClass('isometric');
            workspace.css('width', usedWidth);
            workspace.css('margin-left',
                          Math.ceil(radius * (1 + offset) - halfWidth));
            workspace.css('margin-top',
                          Math.ceil(radius * (1 - offset) - halfHeight));
        }
    });

    $('#add-grid-btn').click(function() {
        var mapSize = mapEditor.mapSize;
        var width = mapSize[0];
        var height = mapSize[1];
        var x = width + 1;
        var y = 1;
        var grid = mapEditorApi.newGrid(x, y);
        var tile = mapEditorApi.newTile();
        grid.data('tile', tile);
        mapEditor.gridsterApi.add_widget(grid, 1, 1, x, y);
        mapEditor.recalcMapSize();
        mapEditorApi.bingGridEvents(grid);
        mapEditorApi.updateAllGrids();
        Toolbar.updateSizeInfo(mapEditor.mapSize);
    });

};

/* 开始执行 */

// 高亮侧边栏的「地图」
$('.nav.nav-list a:contains("地图表")').parent().addClass('active');

// 取得地图ID并初始化编辑器
var mapId = location.href.match(/id=(\d+)/)[1];
$.getJSON('map/' + mapId).done(function(resp) {
    // 检查地图是否已经建立
    if (resp.map == undefined) {
        Workspace.showNoMapError(mapId);
        return;
    }
    // 检查是否设置了大小
    if (resp.map.mapSize == undefined) {
        Workspace.showNoMapSizeError(mapId);
        return;
    }
    initEditor(resp.map, resp.tiles);
    initButtons();
});

});
