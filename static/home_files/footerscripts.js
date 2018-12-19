$("ul#sidesearch").each(function(){
	$('ul#sidenav').children('li').appendTo('ul#sidesearch'); // move all LIs to the sidesearch UL
	$('#sidenav').remove(); // delete the sidenav UL
});
/*$('nav a').each(function (index) {
    if (this.href.trim() == window.location) {
        $(this).parent('li').addClass("current");
    }
});*/
