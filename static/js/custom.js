// base/nav.js
$(window).scroll(function (event) {
    var scroll = $(window).scrollTop();
    // Do something
    if (scroll==0){
    	$('.navi-bg').css('background', 'rgba(255,255,255,0)');
    	
    }
    else{
    	$('.navi-bg').css('background', 'rgb(255, 255, 255)');
    }
});
$(".navbar-toggler.menu").click(function(){
	var toggle_val = $('.navi-bg').css('background').slice(0,4);
	if ($('#navbarsExample06').hasClass('show') && $(window).scrollTop()==0){
		$('.navi-bg').css( 'background', 'rgba(255, 255, 255, 0)' );
	}
	else{
		$('.navi-bg').css( 'background', 'rgb(255, 255, 255)');
	}

});	