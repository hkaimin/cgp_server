$(function() {
'use strict';

// 图片资源地址
var imageUrl = function(path) {
    var url ='http://10.96.131.3/clientres';
    url += path + '.png';
    return url;
}

// 应用 ACE 编辑器
var applyAceEditor = function(selector, language, height) {
    var formField = $(selector);
    formField.hide();

    var editorContainer = $('<div>').attr('id', 'code-editor')
                                    .css('height', '100%')
                                    .css('min-height', height + 'px')
                                    .insertAfter(formField);

    var codeEditor = ace.edit('code-editor');
    codeEditor.setTheme('ace/theme/textmate');
    codeEditor.getSession().setMode('ace/mode/' + language);
    codeEditor.getSession().setValue(formField.val());

    formField.closest('form').submit(function() {
        var value = codeEditor.getSession().getValue();
        formField.val(value);
    });

    editorContainer.parent()
                   .mouseup(function() { codeEditor.resize(); })
                   .css('height', height + 'px')
                   .css('resize', 'vertical')
                   .css('overflow', 'auto')
                   .css('padding-bottom', '5px');
};

// 应用 JSON 编辑器
var applyJsonEditor = function(selector, height, format) {
    var formField = $(selector);
    formField.hide();

    var options = {
        mode: 'code',
        error: function (err) {
            alert(err.toString());
        }
    };
    var editorContainer = formField.parent();
    var valueEditor = new jsoneditor.JSONEditor(editorContainer[0], options);

    if (format !== false) {
        try {
            valueEditor.set(JSON.parse(formField.val()));
        } catch(e) {
            valueEditor.setText(formField.val());
        }
    } else {
        valueEditor.setText(formField.val());
    }

    formField.closest('form').submit(function() {
        var value = valueEditor.getText();
        try {
            JSON.parse(value);
        } catch(e) {
            alert(e);
            return false;
        }
        formField.val(value);
    });
    editorContainer.find('.jsoneditor')
                   .mouseup(function() { valueEditor.resize(); })
                   .css('height', height + 'px')
                   .css('resize', 'vertical')
                   .css('overflow', 'auto')
                   .css('padding-bottom', '5px')
                   .css('background-color', '#A3AAC1');
};

// 应用语法高亮
var applyPrettyPrint = function(attr, lang) {
    var nodes = $('.model-attr-' + attr);
    nodes.wrapInner('<pre class="prettyprint lang-' + lang + '"/>');
    prettyPrint();
};

// 插入模型图片
var insertModelImage = function(small_path, big_path) {
    $('<th>').attr('class', 'model-header-image')
             .attr('title', 'image')
             .text('图片')
             .insertBefore($('.model-header-name'));

    $('.model-attr-name').each(function(i, node) {
        var node = $(node);
        var id = node.prev().text();

        var image = $('<img>').attr('src', small_path(id))
                              .attr('title', '#' + id + ' ' + node.text());
        var link = $('<a>').attr('href', big_path(id))
                           .attr('class', 'colorbox')
                           .append(image);

        $('<td>').attr('class', 'model-header-image')
                 .append(link)
                 .insertBefore(node);
        $('a.colorbox').colorbox({opacity: 0.1, rel: 'gal'});
    });
};

var compactAttrJson = function(name) {
    $('.model-attr-' + name).each(function(i, node) {
        var node = $(node);
        var value = node.text();
        try {
            value = JSON.stringify(JSON.parse(value));
        } catch(e) {
            alert('解析错误：' + e);
        }
        node.text(value);
    });
}

var applySkillsPrettyPrint = function() {
    applyPrettyPrint('TN', 'py compact');
    applyPrettyPrint('YZ', 'py compact');
    applyPrettyPrint('XYA', 'py compact');
    applyPrettyPrint('XYO', 'py compact');
    applyPrettyPrint('CZ', 'py compact');
    applyPrettyPrint('HH', 'py compact');
    applyPrettyPrint('sk1', 'py compact');
    applyPrettyPrint('skv1', 'py compact');
    applyPrettyPrint('sk2', 'py compact');
    applyPrettyPrint('skv2', 'py compact');
    applyPrettyPrint('sk3', 'py compact');
    applyPrettyPrint('skv3', 'py compact');
};

// 模型页面
var modelPages = [

/* resource */

{
    url: '/res/hero/',
    list: function() {
        applyPrettyPrint('unlock', 'javascript compact');
    },
    edit: function() {}
},
{
    url: '/res/reward/',
    list: function() {
        $('.model-attr-reward').each(function(i, node) {
            var node = $(node);
            var value = node.text();
            try {
                value = JSON.stringify(JSON.parse(value));
                value = value.replace(/]$/, '\n]')
                             .replace(/{"[iq]":/g, '\n    $&');
            } catch(e) {
                alert('奖励配置有错误：' + e);
            }
            node.text(value);
        });
        applyPrettyPrint('reward', 'javascript');
    },
    edit: function() {
        applyJsonEditor('#reward', 300);
    }
},
{
    url: '/res/attr/',
    list: function() {
        applySkillsPrettyPrint();
    },
    edit: function() {}
},
{
    url: '/res/heroskill/',
    list: function() {
        $('.model-header-tag').width('50px');
        $('.model-header-exclude').width('60px');
    },
    edit: function() {}
},
{
    url: '/res/map/',
    list: function() {
        applyPrettyPrint('unlock', 'javascript compact');
        $('a.icon').each(function(i, node) {
            var editIcon = $(node);
            var mapId = editIcon.attr('href').match(/id=(\d+)/)[1];
            var editorUrl = '/res/mapeditor/?id=' + mapId;
            var editorIcon = $('<a>').attr('href', editorUrl)
                                     .html('<i class="icon-picture"></i>');
            editIcon.parent().width('60px');
            editorIcon.insertBefore(editIcon);
        });
    },
    edit: function() {},
},
{
    url: '/res/tile/',
    list: function() {
        compactAttrJson('route');
        applyPrettyPrint('route', 'javascript compact');
    },
    edit: function() {}
},
{
    url: '/res/ai/',
    list: function() {
        applyPrettyPrint('param', 'py compact');
    },
    edit: function() {
        applyAceEditor('#param', 'python', 200);
    }
},
{
    url: '/res/aicode/',
    list: function() {
        applyPrettyPrint('code', 'py');
    },
    edit: function() {
        applyAceEditor('#code', 'python', 360);
    }
},
{
    url: '/res/gconfig/',
    list: function() {
        applyPrettyPrint('value', 'javascript compact');
    },
    edit: function() {
        applyJsonEditor('#value', 300);
    }
},

/* user */

{
    url: '/dev/player/',
    list: function() {
        $('.model-header-vipCoin').width('50px');
        $('.model-header-Payed').width('60px');
        $('.model-header-fbChat').width('40px');
        $('.model-header-fbLogin').width('40px');
    },
    edit: function() {},
},
{
    url: '/dev/pattr/',
    list: function() {
        applyPrettyPrint('cli', 'javascript compact');
    },
    edit: function() {
        applyJsonEditor('#cli', 300);
    }
},
{
    url: '/dev/powned/',
    list: function() {
        applyPrettyPrint('item', 'javascript compact');
        applyPrettyPrint('dice', 'javascript compact');
        applyPrettyPrint('car', 'javascript compact');
        applyPrettyPrint('cloth', 'javascript compact');
        applyPrettyPrint('equip', 'javascript compact');
    },
    edit: function() {}
},

/* logging */

/* system */

{
    url: '/ctr/group/',
    list: function() {
        applyPrettyPrint('permissions', 'javascript');
    },
    edit: function() {
        applyJsonEditor('#permissions', 300);
    }
},
{
    url: '/ctr/gamesvr/',
    list: function() {
        $('.model-header-zone').width('40px');
    },
    edit: function() {
        $('#resource_db').addClass('input-xxlarge');
        $('#user_db').addClass('input-xxlarge');
        $('#logging_db').addClass('input-xxlarge');
    },
},
{
    url: '/ctr/zone/',
    list: function() {},
    edit: function() {
        $('#resource_db').addClass('input-xxlarge');
        $('#user_db').addClass('input-xxlarge');
        $('#logging_db').addClass('input-xxlarge');
    },
},

];

var normalPages = [
{
    url: '/dev/reward_test/',
    handler: function() {
        applyJsonEditor('#reward', 640, false);
    }
},
{
    url: '/dev/ai_test/',
    handler: function() {
        applyAceEditor('#param', 'python', 200);
    }
},
];

// 处理模型页面
$.each(modelPages, function(i, page) {
    var pathname = location.pathname;
    if (pathname.indexOf(page.url) === -1) {
        return;
    }
    var type = pathname.split('/')[3];
    if (type === 'edit' || type === 'new') {
        page.edit();
    } else {
        page.list();
    }
});

// 处理一般页面
$.each(normalPages, function(i, page) {
    var pathname = location.pathname;
    if (pathname.indexOf(page.url) === 0) {
        page.handler();
    }
});

});
