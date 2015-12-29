$(document).ready(function() {
	// iCheck
	$('input').iCheck({
		checkboxClass: 'icheckbox_square-green',
	    radioClass: 'iradio_square'
	});


	// button click effect
	var parent, ink, d, x, y;
	$(".btn").click(function(e){
		parent = $(this);
		//create .ink element if it doesn't exist
		if(parent.find(".ink").length == 0)
			parent.prepend("<span class='ink'></span>");
		ink = parent.find(".ink");
		//incase of quick double clicks stop the previous animation
		ink.removeClass("animate");
		//set size of .ink
		if(!ink.height() && !ink.width())
		{
			//use parent's width or height whichever is larger for the diameter to make a circle which can cover the entire element.
			d = Math.max(parent.outerWidth(), parent.outerHeight());
			ink.css({height: d, width: d});
		}
		//get click coordinates
		//logic = click coordinates relative to page - parent's position relative to page - half of self height/width to make it controllable from the center;
		x = e.pageX - parent.offset().left - ink.width()/2;
		y = e.pageY - parent.offset().top - ink.height()/2;
		
		//set the position and add class .animate
		ink.css({top: y+'px', left: x+'px'}).addClass("animate");
	});


	// wow js
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
	})

	// sticky
	var options = {
	  offset: 300
	}
	var header = new Headhesive('.sticky', options);

}); /* end of document ready */

$(window).load(function() {
	// isotope
	$('.grid').isotope({
		itemSelector: '.grid-item',
		percentPosition: true,
		masonry: {
			columnWidth: '.grid-sizer'
		}
	});
	

	// owl carouserl
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

}); /* end of window load */