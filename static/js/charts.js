;
var charts_ops = {
    drawLine:function (target, data, title) {
        var chart = target.highcharts({
            title:{
                text: title
            },
            chart: {
                type: 'spline'
            },
            xAxis: {
                categories: data.categories
            },
            series: data.series,
            legend: {
                enabled:true,
                align: 'right',
                verticalAlign: 'top',
                x: 0,
                y: -15
            }
        });
        return chart;
    }
};