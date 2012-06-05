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
    
    // Binds a submit event to the results administration form
    $("#results").on("submit", "#admin_results_form", function() {
        
        // Serializes the form data
        var data = $(this).serialize();
        
        // Disables input components
        $(":input", this).attr("disabled", true);       
        
        // Displays the animated images
        $("#results_ajax_animation").show();
        $("#statistics_ajax_animation").show();
        
        // Triggers the server call 
        $.post(/* url  */     "/admin/results",
               /* data */     data,
               /* callback */ function(response) {
            
                                   $("#results").empty().append(response.results);
                                   $("#statistics_ajax_animation").hide();
                                   $("#results_ajax_animation").hide();
                                   
                                   if (response.statistics) {
                                       // Statistics in the response mean that the UPDATE is successful
                                       $("#statistics").empty().append(response.statistics);
                                       $("#admin_results_link").show();
                                   }
                                   
                              });    
        
        // Cancels the actual submit action
        return false;

    });    
	
});

