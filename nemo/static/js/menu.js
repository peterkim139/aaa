var btnStatus = false;
$(document).ready(function(){
	addMobileMenu();
	$(window).on('resize', addMobileMenu);
	$('.hamburgerBtn').on('click', menuToggle)
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