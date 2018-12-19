
$(function(){

/* toggle nav */
	$("#menu-icon").on("click", function(){
		$(".sf-menu").slideToggle();
		$(this).toggleClass("active");
	});


//	$().UItoTop({ easingType: 'easeOutQuart' });


// IPad/IPhone
	var viewportmeta = document.querySelector && document.querySelector('meta[name="viewport"]'),
    ua = navigator.userAgent,
 
    gestureStart = function () {
        viewportmeta.content = "width=device-width, minimum-scale=0.25, maximum-scale=1.6";
    },
 
    scaleFix = function () {
      if (viewportmeta && /iPhone|iPad/.test(ua) && !/Opera Mini/.test(ua)) {
        viewportmeta.content = "width=device-width, minimum-scale=1.0, maximum-scale=1.0";
        document.addEventListener("gesturestart", gestureStart, false);
      }
    };
scaleFix();
// Menu Android, REMOVE 1/31/17  to fix homepage on android mobile.  MDL
//	var userag = navigator.userAgent.toLowerCase();
//	var isAndroid = userag.indexOf("android") > -1; 
//	if(isAndroid) {
	//	$('.sf-menu').responsiveMenu({autoArrows:true});
//	}
});

// ************accordion content ******************
function start_accord () {
    $(".accordion_list").smk_Accordion({
				closeAble: true, //boolean
			});
	
}
// ************modal box ******************
function start_modals () {
  $('#basic-modal #staff-link1').click(function (e) {
		$('#faculty-1').modal();
	 	return false;
	});
	$('#basic-modal #staff-link2').click(function (e) {
		$('#faculty-2').modal();
	 	return false;
	});
	$('#basic-modal #staff-link3').click(function (e) {
		$('#faculty-3').modal();
	 	return false;
	});
	$('#basic-modal #staff-link4').click(function (e) {
		$('#faculty-4').modal();
	 	return false;
	});
	$('#basic-modal #staff-link5').click(function (e) {
		$('#faculty-5').modal();
	 	return false;
	});
	$('#basic-modal #staff-link6').click(function (e) {
		$('#faculty-6').modal();
	 	return false;
	});
	$('#basic-modal #staff-link7').click(function (e) {
		$('#faculty-7').modal();
	 	return false;
	});
	$('#basic-modal #staff-link8').click(function (e) {
		$('#faculty-8').modal();
	 	return false;
	});
	$('#basic-modal #staff-link9').click(function (e) {
		$('#faculty-9').modal();
	 	return false;
	});
	$('#basic-modal #staff-link10').click(function (e) {
		$('#faculty-10').modal();
	 	return false;
	});
	$('#basic-modal #staff-link11').click(function (e) {
		$('#faculty-11').modal();
	 	return false;
	});
	$('#basic-modal #staff-link12').click(function (e) {
		$('#faculty-12').modal();
	 	return false;
	});
	$('#basic-modal #staff-link13').click(function (e) {
		$('#faculty-13').modal();
	 	return false;
	});
	$('#basic-modal #staff-link14').click(function (e) {
		$('#faculty-14').modal();
	 	return false;
	});
	$('#basic-modal #staff-link15').click(function (e) {
		$('#faculty-15').modal();
	 	return false;
	});
	$('#basic-modal #staff-link16').click(function (e) {
		$('#faculty-16').modal();
	 	return false;
	});
	$('#basic-modal #staff-link17').click(function (e) {
		$('#faculty-17').modal();
	 	return false;
	});
	$('#basic-modal #staff-link18').click(function (e) {
		$('#faculty-18').modal();
	 	return false;
	});
	$('#basic-modal #staff-link19').click(function (e) {
		$('#faculty-19').modal();
	 	return false;
	});
	$('#basic-modal #staff-link20').click(function (e) {
		$('#faculty-20').modal();
	 	return false;
	});
	
}
// ************ tabbed content ******************
function start_tabs () {
	
	 $('#horizontalTab').responsiveTabs({
                rotate: false,
                startCollapsed: 'accordion',
                collapsible: 'accordion',
                setHash: true,
               <!-- disabled: [3,4], -->
                activate: function(e, tab) {
                    $('.info').html('Tab <strong>' + tab.id + '</strong> activated!');
                },
                activateState: function(e, state) {
                    //console.log(state);
                    $('.info').html('Switched from <strong>' + state.oldState + '</strong> state to <strong>' + state.newState + '</strong> state!');
                }
            });

            $('#start-rotation').on('click', function() {
                $('#horizontalTab').responsiveTabs('active');
            });
            $('#stop-rotation').on('click', function() {
                $('#horizontalTab').responsiveTabs('stopRotation');
            });
            $('#start-rotation').on('click', function() {
                $('#horizontalTab').responsiveTabs('active');
            });
            $('.select-tab').on('click', function() {
                $('#horizontalTab').responsiveTabs('activate', $(this).val());
            });
	
}
// ***************** Filter FAQ content ***************
 function setup_faq_filter()
{
	$("#filter").keyup(function(){
 		
		// hide the list of faq's at the top of the page
		$(".faqlist").fadeOut();
		
		// Retrieve the input field text and reset the count to zero
        var search_text = $('#filter').val();
		var rg = new RegExp(search_text,'i');
		var count= 0;
		
		
        // Loop through the comment list
        $(".faqset").each(function(){
 			
		// If the list item does not contain the text phrase fade it out
			if($.trim($(this).text()).search(rg) == -1) {
            
                $(this).fadeOut();
 
            // Show the list item if the phrase matches and increase the count by 1
            } else {
                $(this).show();
                count++;
            }
        }); // end foreach loop
 
        // Update the count
        var numberItems = count;
		$("#filter-count").text("Number of results returned: "+count);
		if ($('#filter').val().length == 0)
			$(".faqlist").show();
		
 	 });// end keyup function
	
} // end function setup_faq_filter

function clear_filter() 
{
	$('#filter').val('');	
 
	$(".faqset").each(function(){
		$(".faqlist").show();
		$("#filter-count").text("");
		$(this).show();
	});  // end each function
} // end clear filter function


