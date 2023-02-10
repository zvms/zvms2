$(document).ready(function() {
  "use strict";

  PageLoad();

  $('.chat-list-item .avatar,.chat-list-item .chat-bttn').on('click', function() {
      $('.chat-content').addClass('mobile-active');
      return false;
    });

  $('.back-chat-div').on('click', function() {
    $('.chat-content').removeClass('mobile-active');
    return false;
  });

  $('.fab').on('click', function() {
    $(this).toggleClass('open');
    $('.option').toggleClass('open');
    $('.close').toggleClass('open');
  })

  $('#floating-button').on('click', function() {
    $(this).closest('#container-floating').toggleClass('is-opened');
    $('.nds').removeClass('is-opened');
    $('body').toggleClass('is-blur');
  })

    $('.nds').on('click', function() {
      $('.nds').not(this).removeClass('is-opened');
      $(this).toggleClass('is-opened');
    })

  $('.emoji-bttn').on('click', function() {
      $('.emoji-wrap').toggleClass('active');
      return false;
  });

  $('#sidebar-right').on('click', function() {
      $('.perspective').addClass('animate');
      return false;
  });
  $('#close-sidebar').on('click', function() {
      $('.perspective').removeClass('animate');
      return false;
  });

  $('.add').on('click', function() {
      if ($(this).prev().val() < 3) {
        $(this).prev().val(+$(this).prev().val() + 1);
      }
  });
  $('.sub').on('click', function() {
      if ($(this).next().val() > 1) {
        if ($(this).next().val() > 1) $(this).next().val(+$(this).next().val() - 1);
      }
  });

  $('[data-toggle="tooltip"]').tooltip()

  
  $('.shop-categoris').owlCarousel({
      loop:false,
      margin:0,
      nav:false,
      autoplay:false,  
      dots:false,
      items:5
  })

  $('.special-slider').owlCarousel({
      loop:true,
      margin:10,
      nav:false,
      autoplay:false,  
      dots:false,
      items:2
    })
  $('.food-cat').owlCarousel({
      loop:true,
      margin:10,
      nav:false,
      autoplay:false,  
      dots:false,
      items:3  
  })
 

  var $owl = $('.item-category-link')

  $owl.children().each( function( index ) {
    $(this).attr( 'data-position', index ); // NB: .attr() instead of .data()
  });

  $owl.owlCarousel({
    center: true,
    loop: true,
    items: 4,
    autoWidth:true,
    dots:false,
  });

  $(document).on('click', '.owl-item>div.item.text-left', function() {
    var data_tab = $(this).find('h4').attr('data-profile');
     
        $('.profile-content-tab').removeClass('active-tab');
        $('#'+data_tab).addClass('active-tab');
    
    var $speed = 300; 
    $owl.trigger('to.owl.carousel', [$(this).data( 'position' ), $speed] );
  });

  $('.travel-slider').owlCarousel({
      loop:true,
      margin:10,
      nav:false,
      autoplay:false,  
      dots:false,
      items:2
       
  })
  $('.single-product').owlCarousel({
      loop:true,
      margin:0,
      nav:true,
      autoplay:false,  
      dots:true,
      items:1       
  })
  $('.item-banner').owlCarousel({
      loop:false,
      margin:10,
      nav:false,
      autoplay:false,  
      dots:false,
      items:2
       
    })

  $('.slider-0').owlCarousel({
      loop:false,
      margin:5,
      nav:false,
      autoplay:false,  
      dots:false,
      responsive:{
          0:{
              items:6
          },
          600:{
              items:6
          },
          1000:{
              items:6
          },
          1400:{
              items:3
          }
      }
  })

  var owlslide_1 = $('.slider-1')
    owlslide_1.owlCarousel({
      loop:false,
      margin:0,
      nav:false,
      autoplay:false,  
      mouseDrag:true,  
      touchDrag:true,  
      dots:true,
      responsive:{
          0:{
              items:1
          },
          600:{
              items:1
          },
          1000:{
              items:1
          }
      }
    })

    $('.start-tour,.next-tour').on('click', function() {
      owlslide_1.trigger('next.owl.carousel');
    });
  
  
  
});

function PageLoad() {
  jQuery(window).on("load", function(){
        setInterval(function(){ 
            $('.preloader-wrap').fadeOut(300);
        }, 400);
        setInterval(function(){ 
            $('body').addClass('loaded');
        }, 600); 
  });
}

 
 

