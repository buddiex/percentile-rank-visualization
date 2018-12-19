function directedit() {
	 if (document.getElementById('de') !=null) 
	{
		var link = document.getElementById("de").parentNode.innerHTML;
		document.getElementById("de").parentNode.innerHTML = "";
	}
	document.getElementById("directedit").innerHTML = link;
}
function curryear() {
	var currentYear = (new Date).getFullYear();
	$("#year").text( (new Date).getFullYear() );
}
function emailob() {
	$('.email_link').each(function(){
		var text = $(this).html();
		var final_text = text.replace("AT_ETSU", "@etsu.edu");
		$(this).html(final_text);
		var href = $(this).attr('href');
		var next = href.replace("SPECIAL_LINK", "mailto:");
		var final = next.replace("AT_ETSU", "@etsu.edu");
		$(this).attr('href',final);
	});
	$('.email_link_goldmail').each(function(){
		var text = $(this).html();
		var final_text = text.replace("AT_ETSU", "@goldmail.etsu.edu");
		$(this).html(final_text);
		var href = $(this).attr('href');
		var next = href.replace("SPECIAL_LINK", "mailto:");
		var final = next.replace("AT_ETSU", "@goldmail.etsu.edu");
		$(this).attr('href',final);
	});
}
