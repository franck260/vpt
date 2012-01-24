$(document).ready(function() {

    // Binds a submit event to the results administration form
    $("#admin_results_form").submit(function() {
    	
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
