;
var dashboard_index_ops = {
    init: function () {
        this.drawChart();
    },
    drawChart: function () {
        $.ajax({
           url:common_ops.buildUrl("/chart/dashboard"),
           dataType: 'json',
           success:function (res) {
               charts_ops.drawLine($("#member_order"), res.data, "会员与订单总数折线图")
           }
        });
        $.ajax({
           url:common_ops.buildUrl("/chart/finance"),
           dataType: 'json',
           success:function (res) {
               charts_ops.drawLine($("#finance"), res.data, "日营收情况折线图")
           }
        });
    }
};

$(document).ready(function () {
    dashboard_index_ops.init();
});