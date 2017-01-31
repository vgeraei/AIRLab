var staticAddr = "http://172.20.27.94:8000/";
var dst_data;
var dst1, dst0;
var statDisplayedID = "#stat0";

$('.collapse').collapse();

function highcharts_draw(dst){
    var data_hourmap = [];
    var daysOfTheWeek = 6;
    var peopleNumber = 14;
    Math.floor((Math.random() * 11));
    for (var i=0; i<peopleNumber; i++){
        for(var j=0;j<daysOfTheWeek; j++){
            var randomForNow = Math.floor((Math.random() * 11));
            var tempArray =[i,j,randomForNow];
            data_hourmap.push(tempArray);
        }
    }

    var daysOfTheMonth = []
    for (var i=0; i<31; i++){
        daysOfTheMonth.push(i);
    }

    Highcharts.chart('stat0', {
        chart: {
            type: 'spline'
        },
        title: {
            text: 'Monthly Average Temperature'
        },
        subtitle: {
            text: 'Source: WorldClimate.com'
        },
        xAxis: {
            categories: daysOfTheMonth
        },
        yAxis: {
            title: {
                text: 'Temperature'
            },
            labels: {
                formatter: function () {
                    return this.value + '°';
                }
            }
        },
        tooltip: {
            crosshairs: true,
            shared: true
        },
        plotOptions: {
            spline: {
                marker: {
                    radius: 4,
                    lineColor: '#666666',
                    lineWidth: 1
                }
            }
        },
        series: [{
            name: 'Room Weather',
            marker: {
                symbol: 'square'
            },
            data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, {
                y: 26.5,
                marker: {
                    symbol: 'url(https://www.highcharts.com/samples/graphics/sun.png)'
                }
            }, 23.3, 18.3, 13.9, 9.6, 5, 6, 8, 11, 14, 12, 11, 20, 21, 22, 23, 24, 11, 12, 27, 28, 29, 30]

        }, {
            name: 'Outside Weather',
            marker: {
                symbol: 'diamond'
            },
            data: [{
                y: 3.9,
                marker: {
                    symbol: 'url(https://www.highcharts.com/samples/graphics/snow.png)'
                }
            },12, 32, 23, 21, 15,15, 15, 12, 15, 7, 8 , 9, 11, 4, 6, 7, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8, 6, 8]
        }]
    });

    Highcharts.chart('stat2', {

        chart: {
            type: 'heatmap',
            marginTop: 40,
            marginBottom: 80,
            plotBorderWidth: 1
        },


        title: {
            text: 'AIRLab People Work Hours.'
        },

        xAxis: {
            categories: ['B. Rahmati', 'A. Rezaei', 'A. Shanechi', 'Dr. Masoudi', 'Dr. Nasihatkon', 'H. Aghaei', 'M. Kiani', 'V. Geraei', 'Z. Mousavi', 'A. Alamolhoda', 'P. Kasraie', 'Prof. Aghajan' , 'A. Alirezaei', 'IMX Team']
        },

        yAxis: {
            categories: ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'],
            title: null
        },

        colorAxis: {
            min: 0,
            minColor: '#FFFFFF',
            maxColor: Highcharts.getOptions().colors[0]
        },

        legend: {
            align: 'right',
            layout: 'vertical',
            margin: 0,
            verticalAlign: 'top',
            y: 25,
            symbolHeight: 280
        },

        tooltip: {
            formatter: function () {
                return '<b>' + this.series.xAxis.categories[this.point.x] + '</b> worked <br><b>' +
                    this.point.value + '</b> hours on <br><b>' + this.series.yAxis.categories[this.point.y] + '</b>';
            }
        },

        series: [{
            name: 'Hours of Work per member',
            borderWidth: 1,
            data: data_hourmap,
            dataLabels: {
                enabled: true,
                color: '#000000'
            }
        }]

    });


    // Radialize the colors
    Highcharts.getOptions().colors = Highcharts.map(Highcharts.getOptions().colors, function (color) {
        return {
            radialGradient: {
                cx: 0.5,
                cy: 0.3,
                r: 0.7
            },
            stops: [
                [0, color],
                [1, Highcharts.Color(color).brighten(-0.3).get('rgb')] // darken
            ]
        };
    });

    // Build the chart
    Highcharts.chart('stat1', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Door State Sensor'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    },
                    connectorColor: 'silver'
                }
            }
        },
        series: [{
            name: 'Brands',
            data: [
                { name: 'Open', y: dst.dst0 },
                {
                    name: 'Closed',
                    y: dst.dst1,
                    sliced: false,
                    selected: true
                }
            ]
        }]
    });

    $('#stat1').css("display", "none");
    $('#stat2').css("display", "none");

}

function statButtons(){
    $('#stat0Button').on('click', function(){
        if(statDisplayedID != '#stat0') {
            $(this).addClass("active");
            $(statDisplayedID+'Button').removeClass("active");

            $(statDisplayedID).hide("fast", function(){
                $("#stat0").show("fast");
                 statDisplayedID = '#stat0';
            });

        }

    });

    $('#stat1Button').on('click', function(){
        if(statDisplayedID != '#stat1') {
            $(this).addClass("active");
            $(statDisplayedID+'Button').removeClass("active");

            $(statDisplayedID).hide("fast", function(){
                $("#stat1").show("fast");
                 statDisplayedID = '#stat1';
            });

        }

    });

    $('#stat2Button').on('click', function(){
        if(statDisplayedID != '#stat2') {
            $(this).addClass("active");
            $(statDisplayedID+'Button').removeClass("active");

            $(statDisplayedID).hide("fast", function(){
                $("#stat2").show("fast");
                 statDisplayedID = '#stat2';
            });
        }

    });
}

$(function() {
    $('a[href*=#]:not([href=#])').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {

            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
            if (target.length) {
                $('html,body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });
});

function changeNumber(){
    var num = $('.numberChange').val();
    console.log(num);
    $.ajax({
        type: 'post',
        url: '/sensors/change_number/' //+ num.toString()
    });
}

function load_realtime_data(){
    $.ajax({
        url:'/sensors/load_realtime/',
        type: 'post',
        dataType: 'json',
        cache: false,
        success: function (data) {
            $("#temp").html(data['TMP']+' °C');
            $("#hum").html(data['HUM']);
            $("#number").html(data['NUM']);
            $("#door_status").html(((parseInt(data['DST']))?("Open"):("Closed")));
            $("#light").html(data['LUM']);
            $("#pir").html(((data['PIR'])?("Someone in the room."):("The room is empty.")));
        },
    });
    setTimeout(load_realtime_data, 1000);
};

function test_query() {
    $.ajax({
        url:'/sensors/query/',
        type: 'post',
        dataType: 'json',
        cache: false,
        success: function (data) {
            console.log(data);
            dst_data = data;
            highcharts_draw(dst_data);
        }
    });
}

$(document).ready( function() {
    load_realtime_data();
    test_query();
    statButtons();
    // $('.numberChangeButton').on('click', changeNumber);

    $('.subMenu').smint({
        'scrollSpeed' : 1000
    });

    // var dd = $('.vticker').easyTicker({
    //     direction: 'up',
    //     easing: 'easeInOutBack',
    //     speed: 'slow',
    //     interval: 4000,
    //     height: 'auto',
    //     visible: 1,
    //     mousePause: 0,
    //     controls: {
    //         up: '.up',
    //         down: '.down',
    //         toggle: '.toggle',
    //         stopText: 'Stop !!!'
    //     }
    // }).data('easyTicker');



    $(function () { $('.tooltip-hide').tooltip('hide');});



// Portfolio
    var data = {
        labels: [
            "23-24°C",
            "24-25°C",
            "25-26°C"
        ],
        datasets: [
            {
                data: [33, 45, 22],
                backgroundColor: [
                    "#FF6384",
                    "#36A2EB",
                    "#FFCE56"
                ],
                hoverBackgroundColor: [
                    "#FF6384",
                    "#36A2EB",
                    "#FFCE56"
                ]
            }]
    };

    var ctx = document.getElementById("myChart");

    var myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        animation:{
            animateScale:true
        }
    });

    var $container = $('.portfolioContainer');
    $container.isotope({
        filter: '*',
        animationOptions: {
            duration: 750,
            easing: 'linear',
            queue: false
        }
    });

    $('.portfolioFilter a').click(function(){
        $('.portfolioFilter .current').removeClass('current');
        $(this).addClass('current');

        var selector = $(this).attr('data-filter');
        $container.isotope({
            filter: selector,
            animationOptions: {
                duration: 750,
                easing: 'linear',
                queue: false
            }
        });
        return false;

    });

    $(".group2").colorbox({rel:'group2', transition:"fade"});


    $('.carousel').carousel();



});

