$(document).ready(function() {

	// iCheck init
	$('.chboxRadio').iCheck({
		checkboxClass: 'icheckbox_square-green',
		radioClass: 'iradio_square'
	});


	// button click effect
	var parent, ink, d, x, y;
	$(".btn").click(function(e){
		parent = $(this);
		if(parent.find(".ink").length == 0)
			parent.prepend("<span class='ink'></span>");
		ink = parent.find(".ink");
		ink.removeClass("animate");
		if(!ink.height() && !ink.width())
		{
			d = Math.max(parent.outerWidth(), parent.outerHeight());
			ink.css({height: d, width: d});
		}
		x = e.pageX - parent.offset().left - ink.width()/2;
		y = e.pageY - parent.offset().top - ink.height()/2;
		
		ink.css({top: y+'px', left: x+'px'}).addClass("animate");
	});


	// wow js init
	new WOW().init();


	// smooth scroll to href
	$('.scrollToHref').on('click', function(){
	    var href = $(this).attr("href");
	    var offsetTop = $(href).offset().top;
	    $('html, body').animate({
	      scrollTop: offsetTop
	    }, 1000);
	    return false;
	});


	// checkboxes and radios
	var elemGroup = $('.checkbox, .radio');
	elemGroup.each(function() {
		var elem = $(this);
		if (elem.children('input').prop('checked')) {
			elem.addClass('active')
		}
		elem.children('input').change(function() {
			elem.toggleClass('active');
		});
	});


	// scroll to top
	$('.scrollToTop').on('click', function(){
		$('html, body').animate({
	      scrollTop: 0
	    }, 1000);
	    return false;
	});
	$(window).on('scroll', function(){
		if ($(window).scrollTop() > 120) {
			$('.scrollToTop').fadeIn();
		} else {
			$('.scrollToTop').fadeOut();
		}
	});


	// magnific popup init
	$('.popupBtn').magnificPopup({
		type: 'inline',
		preloader: false
	});


	// sticky init
//	var options = {
//	  offset: 350
//	}
//	var header = new Headhesive('.sticky', options);


	// jquery ui tabs init
	$('.tabsWrap').tabs({
		activate: function( event, ui ) {
			$('.footable').trigger('footable_initialize');
			// tabActiveEffect();
		},
		hide: { 
			effect: "fade", 
			duration: 300 
		},
		show: { 
			effect: "fade", 
			duration: 300 
		}
	});


	// foo table init
	$('.footable').footable({
		breakpoints: {
			xs: 480,
			sm: 540,
			md: 768,
			lg: 1024,
		}
	});



	// dropdown 
	$('.drDnBtn').on('click', function(){
		var thisDrDn = $(this);
		var thisDrDnCont = $(this).next('.drDnCont');
		$('.drDnCont').not(thisDrDnCont).fadeOut()
		thisDrDn.next('.drDnCont').fadeToggle();
	});
	$('.drDnWrap').on('click', function(e){
		e.stopPropagation();
	})
	$('body').on('click', function(){
		$('.drDnCont').fadeOut();
	});


	// custom scroll bar init
	$(".customScroll").mCustomScrollbar({
		scrollbarPosition: "outside"
	});


	// datepicker 
	$(".datepicker").datepicker({
		nextText: "",
		prevText: "",
		showOtherMonths: true,
        selectOtherMonths: true
	});




	// image fill container
	$('.imgCover').each(function(){
		var src = $(this).find('img').attr('src');
		$(this).css('background-image', 'url(' + src +')');
		$(this).find('img').hide();
	})



	
	homeSrchPosition();
	equalHeight();


	$(window).on('resize', function(){
		stickyFooter();
		// searchWrapperHeight(768);
		homeSrchPosition();
		equalHeight();
	});

	// expend up slider
	$('.expandBtn').on('click', function(){
		var wrap = $('.expandWrap');
		wrap.hide();
		wrap.slideDown();
	});
	$('.closeExpandWrap').on('click', function(){
		$('.expandWrap').slideUp();
	})
	

}); /* end of document ready */

$(window).load(function() {

	// isotope init
	$('.grid').isotope({
		itemSelector: '.grid-item',
		percentPosition: true,
		masonry: {
			columnWidth: '.grid-sizer'
		}
	});
	

	// owl carouserl init
	$(".owlSingle").owlCarousel({
		navigation : true,
		slideSpeed : 300,
		paginationSpeed : 400,
		singleItem: true,
		navigationText: ["<i class='icon-arrow-1-square-left'></i>","<i class='icon-arrow-1-square-right'></i>"]
	});
	$(".owlSlider").owlCarousel({
		autoPlay: 3000,
		items : 3,
		itemsDesktop : false,
		itemsDesktopSmall : false,
		itemsTablet: [768,2],
  		itemsMobile : [520,1],
		navigation : true,
		navigationText: ["<i class='icon-arrow-1-square-left'></i>","<i class='icon-arrow-1-square-right'></i>"]
	});


	// tabActiveEffect();
	// searchWrapperHeight(768);
	stickyFooter();
	

}); /* end of window load */





// active tab slide effect
function tabActiveEffect(){
	if($('.tabsStyle1').length>0) {
		var activeEl = $('.tabsStyle1 .ui-tabs-active');
		var activeW = activeEl.width();
		var offset = activeEl.position().left;
		$('.activeIndicator').css('left', offset + 'px');
		$('.activeIndicator').css('width', activeW + 'px');
	}
}

// sticky footer dynamic height
function stickyFooter(){
	var footerH = $('footer').outerHeight();
	$('.mainWrap').css('padding-bottom', footerH);
	$('footer').css('margin-top', (0-footerH));
}

// set searchWrapper height
function searchWrapperHeight(breakpoint){
	if ($(window).width() > breakpoint) {
		var avlblHeight = $(window).height() - $('header').height() - $('.topDarkLine').height();
		$('.searchWrap').height(avlblHeight);
		$('.searchWrap .customScroll').mCustomScrollbar({
			scrollbarPosition: "outside"
		});
	} else {
		$('.searchWrap').height('');
		$('.searchWrap .customScroll').mCustomScrollbar("destroy");
	}
}

// keep home searchbar at bottom
function homeSrchPosition(){
	var windowH, srchH;
	windowH = $(window).height();
	srchH = $('.homeSrch').outerHeight();
	$('.homeTop').height(windowH - srchH);
}


// equal height
function equalHeight(){
	$('.equalWrap').each(function(index){
		var items = $(this).find('.equalItem');
		var len = items.length;
		var maxHeight = items[0].offsetHeight;
		for (var i = 0; i < len; i++) {
			if (items[i].offsetHeight > maxHeight) {
				maxHeight = items[i].offsetHeight;
			}
		}
		items.height(maxHeight);
	});
}

	// slide animation
function slideAnimation(self){
   // var self = $(this);
    var targetID = self.attr('href');
    var wrap = $('.sideSlideWrap');
    if (targetID.slice(1) == $('.prevSlide').attr('id')) {
        $('.prevSlide').removeClass('prevSlide');
        wrap.find('.active').fadeOut(1000);
        wrap.find('.active').removeClass('active');
        setTimeout(function(){
            $(targetID).show("slide", { direction: "left" }, 800);
            $(targetID).addClass('active');
        },500);
    } else {
        $('.prevSlide').removeClass('prevSlide');
        wrap.find('.active').hide("slide", { direction: "left" }, 800);
        wrap.find('.active').removeClass('active').addClass('prevSlide');
        setTimeout(function(){
            $(targetID).fadeIn(1000);
            $(targetID).addClass('active');
        },500);
    }
    wrap.css('min-height',$(targetID).height());
}


