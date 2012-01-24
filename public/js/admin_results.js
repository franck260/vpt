$(document).ready(function() {
	
    // Binds a click event to the unlock link
    $("#admin_results_link").click(function() {
    	
        // Reads some information in the link itself
        var tournament_id = $(this).attr("data-tournament-id");
    	
        // Hides the administration link
        $(this).hide();
        
        // Displays the animated image
        $("#results_ajax_animation").show();

        // Triggers the server call 
        $("#results").load(/* url  */     "/admin/results?tournament_id=" + tournament_id,
                           /* callback */ function() {
                                              $("#results_ajax_animation").hide();
                                          });
        
        // Cancels the actual click action
        return false;

    });	
	
});

