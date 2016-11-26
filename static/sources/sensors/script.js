var staticAddr = "http://172.20.27.94:8000/"


$('.collapse').collapse();



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
      $("#temp").html(data['TMP']);
      $("#hum").html(data['HUM']);
      $("#number").html(data['NUM']);
      $("#door_status").html(((data['DST'])?("Open"):("Closed")));
      $("#light").html(data['LUM']);
    },
  });
  setTimeout(load_realtime_data, 1000);
};


$(document).ready( function() {
  load_realtime_data();
  $('.numberChangeButton').on('click', changeNumber);

  $('.subMenu').smint({
    'scrollSpeed' : 1000
  });

  var dd = $('.vticker').easyTicker({
    direction: 'up',
    easing: 'easeInOutBack',
    speed: 'slow',
    interval: 4000,
    height: 'auto',
    visible: 1,
    mousePause: 0,
    controls: {
      up: '.up',
      down: '.down',
      toggle: '.toggle',
      stopText: 'Stop !!!'
    }
  }).data('easyTicker');



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

