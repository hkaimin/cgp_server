(function($) {

// 相当于 $.params 的反操作
$.deparams = function(text) {
    var obj = {};
    $.each(text.split('&'), function(i, entry) {
        var parts = entry.split('=');
        var key = parts[0];
        var value = parts[1];
        if (key !== '') {
            obj[parts[0]] = parts[1];
        }
    });
    return obj;
};

/* 时间转换 */

// Date 对象或时间截 转 可读格式
$.cvReadableTime = function(value) {
    var date;
    if (typeof(value) === 'object') {
        date = value;
    } else {
        // 自动判断时间截格式
        // Javascript 的时间截长度是 13 位，毫秒算在整数部分
        // 而 Python 的时间截长度是 10 位，毫秒算在小数部分
        if (String(value).length < 13) {
            value *= 1000;
        }
        date = new Date(value);
    }
    var offseted = date.getTime() - date.getTimezoneOffset() * 60 * 1000;
    return new Date(offseted).toISOString().slice(0, 19).replace('T', ' ');
};

// 可读格式 转 时间截
$.cvUnixTime = function(readabletime) {
    var isoString = readabletime.replace(' ', 'T');
    return new Date(isoString).getTime() / 1000;
};

// 时间截范围 转 可读格式描述字符串
$.cvLabelTimeRange = function(start, end) {
    return '[' + $.cvReadableTime(start) + ', ' + $.cvReadableTime(end) + ']';
}

// 秒数转 HH:MM:SS 格式
$.s2hms = function(seconds) {
    if (seconds < 0) {
        return '00:00:00'
    }

    var minutes = Math.floor(seconds / 60);
    var s = seconds % 60;
    var h = Math.floor(minutes / 60);
    var m = minutes % 60;

    var zerofill = function(v) {
        return v < 10 ? '0' + v : String(v);
    };

    s = zerofill(s);
    m = zerofill(m);
    h = zerofill(h);
    return h + ':' + m + ':' + s;
};

/* 时间生成 */

// 生成时间范围
$.mkReadableTimeRange = function(start, end) {
    var now = new Date();
    var start = new Date(now.getTime() + start * 1000);
    var end = new Date(now.getTime() + end * 1000);
    var obj = {
        start: $.cvReadableTime(start),
        end: $.cvReadableTime(end),
    }
    return obj;
};

// 生成日期范围
$.mkDateRange = function(start, end) {
    var aDaySeconds = 60 * 60 * 24;
    var now = new Date();
    var start = new Date(now.getTime() + start * aDaySeconds * 1000);
    var end = new Date(now.getTime() + end * aDaySeconds * 1000);
    var obj = {
        start: $.cvReadableTime(start).slice(0, 10),
        end: $.cvReadableTime(end).slice(0, 10),
    }
    return obj;
};

/* 数组统计函数 */

// 合计数组元素的值
$.sum = function(aArray) {
    return aArray.reduce(function(a, b) { return a + b; });
};

// 计算数组元素的平均值
$.avg = function(aArray) {
    return $.sum(aArray) / aArray.length;
};

// 找出元素最大值
$.max = function(aArray) {
    return Math.max.apply(Math, aArray);
};

// 找出元素最小值
$.min = function(aArray) {
    return Math.min.apply(Math, aArray);
};

}(jQuery));

// 通用库函数
var lib = {

    // 格式化为整数
    integer: d3.format(',d'),

    // 把表单值放到地址栏的描点里
    formStore: {
        empty: function() {
            return location.hash === '';
        },
        get: function() {
            return location.hash.slice(1).replace(/_/g, ' ');
        },
        set: function(value) {
            location.hash = decodeURIComponent(value).replace(/\+/g, '_');
        }
    },

    // 使用 d3 创建表格
    initD3Table: function(createRowHtml, rows) {
        var tbody = d3.select('tbody').selectAll('tr').data(rows);
        tbody.enter().append('tr').html(createRowHtml);
        tbody.html(createRowHtml);
        tbody.exit().remove();
    },

};
