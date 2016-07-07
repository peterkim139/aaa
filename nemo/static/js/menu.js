var btnStatus = false;
$(document).ready(function(){
	addMobileMenu();
	$(window).on('resize', addMobileMenu);
	$('.hamburgerBtn').on('click', menuToggle)
});

$(window).on("scroll", function() {
	var scrollOff = $(".wrapper").offset().top + 85;
	var stHeader = $(".sticky");

	if ($(window).scrollTop() > scrollOff) {
		stHeader.addClass("animated fadeInDown");
		stHeader.css("background-color","#fff");
		stHeader.parents(".homeTop").removeClass("trHeader");
		$('.headerNav').css('margin-top', '0');
	}
	else {
		stHeader.parents(".homeTop").addClass("trHeader");
		stHeader.css("background-color","transparent");
		stHeader.addClass("fadeInUp").removeClass("fadeInDown");
		$('.headerNav').css('margin-top', '10px');
	}
});


function addMobileMenu(){
	var menuStatus = !!$('.headerNavMobile').length;
	if (($(window).width()<880) && menuStatus==false) {
		$('.headerNav').clone().addClass('headerNavMobile').appendTo('body');
		$('.hamburgerBtn').appendTo('body');
	} else if ($(window).width()>=880) {
		$('.headerNavMobile').remove();
	}
	$('.popupBtn').magnificPopup();
}

function menuToggle(){
	if (!btnStatus) {
		$('body').css('overflow', 'hidden');
		$("#showMenu i").removeClass("icon-bars").addClass("icon-cancel");
		$('.headerNavMobile').show();
		btnStatus = true;
	} else {
		$('body').css('overflow', 'auto');
		$("#showMenu i").removeClass("icon-cancel").addClass("icon-bars");
		$('.headerNavMobile').hide();
		btnStatus = false;
	}
}



