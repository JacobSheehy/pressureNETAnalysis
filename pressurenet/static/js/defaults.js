	$(document).ready(function() {
      

	  // Show Live Stream page, hide other pages
		$( ".page-link" ).click(function() {
		  if($(this).hasClass('off')) {
		    var page = $( this ).attr( "data-page" );
		    $( ".page-link" ).removeClass( "on" ).addClass( "off" );
		    $( this ).removeClass( "off" ).addClass( "on" );
		    $( "#screen" ).fadeIn( "fast" );
		    $( "#close" ).fadeOut( "fast" );
		    $( ".page" ).slideUp( "fast" );
		    $( "#" + page ).slideDown( "slow" );
		    $( "#close" ).fadeIn( "fast" );
		  } else {
		  	$( this ).removeClass( "on" ).addClass( "off" );
			  $( ".page" ).slideUp( "fast" );
			  $( "#screen, #close" ).fadeOut( "fast" );
		  }
		});
		
	
		

	  // Close pages, fade out screen.
		$( "#close, #screen" ).click(function() {
			$( ".page-link" ).removeClass( "on" ).addClass( "off" );
			$( ".page" ).slideUp( "fast" );
			$( "#screen, #close" ).fadeOut( "fast" );
		});      
      
      
      
 });


	
