$(document).ready(function() {
	
    // Binds a click event to all subscribtion links
    $("#statistics").on("click", "a[id^='subscribtion_link']", function() {
		
        // Reads some information in the link itself
        var tournament_id = $(this).attr("data-tournament-id");
        var status = $(this).attr("data-status");
		
        // Disables all subscribtion links
        $("a[id^='subscribtion_link']").each(function() {
            $(this).removeAttr("href");
            $(this).css({"text-decoration" : "none", "color" : "grey"});
        });
		
        // Hides the administration link
        $("#admin_results_link").hide(); 
		
        // Highlights the selected link
        $(this).css({"font-style" : "italic", "color" : "black"});
	    
        // Displays the animated images
        $("#subscribtion_ajax_animation").show();
        $("#results_ajax_animation").show();
	    
        // Triggers the server call 
        $.post(/* url  */     "/update/status",
               /* data */     {"tournament_id" : tournament_id, "status" : status},
               /* callback */ function(response) {
	                               $("#statistics").html(response.statistics);
	                               $("#results").html(response.results);
	                               $("#results_ajax_animation").hide();
	                               $("#admin_results_link").show(); 
	                               // No need to reset the other altered components since they get refreshed as well
	                          });	   	    
		
        // Cancels the actual click action
        return false;		
    });
    
});

