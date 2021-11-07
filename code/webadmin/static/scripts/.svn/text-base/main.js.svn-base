$(function() {
'use strict';

// 通用
$(".alert").alert();
$(".btn-large").removeClass('btn-large');
$("table.model-list").addClass('table-hover');
$("table.table-sorted").tablesorter();

// 筛选器
(function autoShowFilterForm() {
    var toggle = function() {
        if ($('#filter_form table.filters tr').length > 0) {
            $('#filter_form').show();
        } else {
            $('#filter_form').hide();
        }
    }
    toggle();
    $('.field-filters a.filter').click(toggle);
})();

// 分类高亮
(function highlightCategory() {
    var category = $('.breadcrumb li:first a').text()
    if (category === '我的账号') {
        $('#account').addClass('active');
    }
    else if (category === '服务器') {
        $('li.gamesvr').addClass('active');
    } else {
        var selector = '.navbar a:contains("' + category + '")';
        $(selector).parent().addClass('active');
    }
})();

// 日期时间选择器
(function setupDateTimePicker() {
    var timeOptions = {language: 'zh-CN'};
    $('.datetimepicker.datetime').datetimepicker(timeOptions);
})();

// 日期选择器
(function setupDatePicker() {
    var timeOptions = {language: 'zh-CN', pickTime: false};
    $('.datetimepicker.date').datetimepicker(timeOptions);
})();

});
