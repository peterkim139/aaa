$(function(){

	/* Start  */

	function checkWidth() {
        var windowSize = $(window).width();

        if (windowSize <= 880) {
        	$(".headerNav").css("display","none");
            $("body").removeClass("over-hide");
        	if($("body").hasClass("over-hide")){
				$("#showMenu i").removeClass("icon-bars").addClass("icon-cancel");
			}else {
				$("#showMenu i").removeClass("icon-cancel").addClass("icon-bars");
			}
        }
        else{
            $(".headerNav").css("display","block");
            $("body").removeClass("over-hide");
        }
    }
    checkWidth();
    $(window).resize(function(){
        checkWidth();
    });

	/* End  */
	/* Start Animate.css */

	$(window).bind("scroll", function() {

		var scrollOff = $(".wrapper").offset().top + 85;
		var stHeader = $(".sticky");

		if ($(window).scrollTop() > scrollOff) {
			stHeader.addClass("animated fadeInDown");
			stHeader.css("background-color","#fff");
			stHeader.parents(".homeTop").removeClass("trHeader");
		}
		else {
			stHeader.parents(".homeTop").addClass("trHeader");
			stHeader.css("background-color","transparent");
			stHeader.addClass("fadeInUp").removeClass("fadeInDown");
		}
	});

	/* End Animate.css */

	/* Start Responsive Menu Js */

	$("#showMenu").click(function(){
		$(".headerNav").slideToggle();
	}, function(){
		$(".sticky").removeClass("animated");
		$(".headerNav").slideToggle();
		$("body").toggleClass("over-hide");
		$(".menuToggle i").toggleClass("fa-bars");
		if($("body").hasClass("over-hide")){
			$("#showMenu i").removeClass("icon-bars").addClass("icon-cancel");
		}else {
			$("#showMenu i").removeClass("icon-cancel").addClass("icon-bars");
		}
	});

	/* End Responsive Menu Js */

	/* Start Custom Scroll Js */

	$(".tableScroll").mCustomScrollbar({
		axis:"x",
		scrollButtons:{
			enable:false
		}
	});

	/* End Custom Scroll Js */

});