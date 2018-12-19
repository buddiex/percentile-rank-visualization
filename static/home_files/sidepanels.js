function activate_sidepanels() {
	
// clone a copy of the left nav for the site
   		var $menu = $("#cssmenu").clone();
		$menu.attr( "id", "mobilenavpanel" );
		$menu.mmenu({
			onClick: { close: false},
			offCanvas: {zposition: "front"},
   			// options
			slidingSubmenus:false
		});
		// change the ID of the form inside the mobilemainpanel, so that it will not be duplicating items in left nav 
		$('div#mobilenavpanel ul li form#deptsearch').attr("id","mobile_dsearch");
		$('div#mobilenavpanel ul li form#mobile_dsearch').attr("name","mobile_dsearch");
		// change ID and name for input text search box and for label tag
		$('div#mobilenavpanel ul li form label:first-child').attr("for","q_mob");	
		$('div#mobilenavpanel ul li form input#q').attr("id","q_mob");	
		$('div#mobilenavpanel ul li form input#q_mob').attr("name","q_mob");	
		// change ID and nae for submit button and label tab
		//$('div#mobilenavpanel ul li form label:nth-child(2)').attr("for","sitesrchbtn_mob");	
	//	$('div#mobilenavpanel ul li form input#sitesrchbtn').attr("id","sitesrchbtn_mob");	
//		$('div#mobilenavpanel ul li form input#sitesrchbtn_mob').attr("name","sitesrchbtn_mob");	
		
	
	
		// instantiate 2nd menu to slide from right 
		// if there is a horizontal nav on this site....
		if ($('nav#horizontalnav').length > 0)
		{
			// clone a copy of the horizontal nav for the site
			var $menu = $("#horizontalnav").clone();
			// give this cloned hnav an ID of mobilemainpanel
			$menu.attr( "id", "mobilemainpanel" );
			
			$menu.mmenu({
				onClick: { close: false},
				offCanvas: {position: "right", zposition: "front"},
	         	// options
				slidingSubmenus:false
			});
			
			// change the ID of the ul inside the mobilemainpanel, so that it will function 
			// like the leftnav and not like the superfish dropdown on desktop size
			$('nav#mobilemainpanel ul#example').attr("id","mobilehnav");
			// remove sf class names from the ul inside the mobilemainpanel
			$('nav#mobilemainpanel ul#mobilehnav').removeClass("sf-menu responsive-menu sf-js-enabled sf-arrows");
			// remove sf class names from the li inside the mobilemainpanel
			$('nav#mobilemainpanel ul#mobilehnav li').removeClass("first-item");
			// remove sf class names from the a inside the mobilemainpanel
			$('nav#mobilemainpanel ul#mobilehnav li a').removeClass("sf-with-ul");
			// remove all inline styles from within the hnav ul
			$('nav#mobilemainpanel ul#mobilehnav ul').removeAttr("style");
			
			// ************************************************************
			// add a horizontal rule between horizontal nav and top ETSU nav
			
			$('nav#mobilemainpanel ul#mobilehnav').append('<li class="mrnavbreak">&nbsp;</li>');
			
			// ************************************************************
			// copy top ETSU search bar into mobilmainpanel div tag
			
			$('nav#mobilemainpanel ul#mobilehnav').append($('div#search').html());
			$('#imgetsusrch').attr("src","/cmsroot/menu_images/search_button.png");
			
			
			// ************************************************************
			// add a horizontal rule between ETSU search and top ETSU nav
			
			$('nav#mobilemainpanel ul#mobilehnav').append('<li class="mrnavbreak">&nbsp;</li>');
			// ************************************************************
			// copy top ETSU global navigation into mobilmainpanel div tag
			
			$('nav#mobilemainpanel ul#mobilehnav').append($('div#top_nav ul').html());
			
		
		} // end if
		else 	// if there is no hnav for this site
		{
			// clone a copy of the ETSU top nav for the site
			var $menu = $("#top_nav").clone();
			// give this cloned hnav an ID of mobilemainpanel
			$menu.attr( "id", "mobilemainpanel" );
			
			$menu.mmenu({
				onClick: { close: false},
				offCanvas: {position: "right", zposition: "front"},
	         	// options
				slidingSubmenus:false
			});
		}
		// add class name of mm-fullsubopen to each menu with dropdown, so that entire text will be clickable to dropdown 
		$('.mm-subopen').addClass('mm-fullsubopen');
			
}
