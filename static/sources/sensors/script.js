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

function changeNumber(num){
  $.ajax({
    url: staticAddr + "change/" + num.toString(),
    success: function (data) {
      console.log("Change was successful");
    },
  });
}

function doStuff(){
  //var currentdate = new Date();
  //var time = currentdate.getHours() + ":"
  //+ currentdate.getMinutes() + ":"
  //+ currentdate.getSeconds();
  //var date = currentdate.getDate() + "/"
  //+ (currentdate.getMonth()+1)  + "/"
  //+ currentdate.getFullYear();

  //$("#cal").html('<img src="images/cal.png" id="calImg">'+date);
  //$("#clock").html('<img src="images/clock.png" id="clockImg">'+time);
  $.ajax({
    url:"http://172.20.27.94:8000/api/detail",
    dataType: 'json',
    cache: false,
    success: function (data) {
      $("#temp").html(data['temp']);
      $("#hum").html(data['hum']);
      $("#number").html(data['number']);
      $("#door_status").html(((data['door_state'])?("Open"):("Closed")));
      $("#light").html(data['light']);
    },
  });
  setTimeout(doStuff, 1000);
};


$(document).ready( function() {
  doStuff();

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

});

$(function () { $('.tooltip-hide').tooltip('hide');});



// $(document).ready(function(){
//   $('.changeNumberButton').on('click', );


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