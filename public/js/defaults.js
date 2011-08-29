function disableLink(linkId) {
    
    $(linkId).removeAttr("href");
    $(linkId).css( {"text-decoration": "none",
                    "color": "grey"} );
    
}

function highlightSelectedLink(linkId) {
    
    $(linkId).css( {"font-style": "italic",
                    "color": "black"} );
    
}

function unlockResults(tournament_id) {
    
    // Hides the administration link
    $("#admin_results_link").hide();
    
    // Displays the animated image
    $("#results_ajax_animation").show();

    // Triggers the server call 
    $("#results").load(/* url  */     "/admin/results/" + tournament_id,
                       /* callback */ function(data) {
                                          $("#results_ajax_animation").hide();
                                      });      
    
}

function updateResults(tournament_id) {
    
    // Displays the animated images
    $("#results_ajax_animation").show();
    $("#statistics_ajax_animation").show();

    // Triggers the server call 
    $.post(/* url  */     "/admin/results/" + tournament_id,
           /* data */     $("#admin_results_form").serialize(),
           /* callback */ function(data) {
        
                               $("#results").empty().append(data.results);
                               $("#statistics_ajax_animation").hide();
                               $("#results_ajax_animation").hide();
                               
                               if (data.statistics) {
                                   // Statistics in the response mean that the UPDATE is successful
                                   $("#statistics").empty().append(data.statistics);
                                   $("#admin_results_link").show();
                               }
                               
                          });          
}


function updateStatus(tournament_id, status) {

    // Disables all subscribtion links
    disableLink("#subscribtion_link_A");
    disableLink("#subscribtion_link_P");
    disableLink("#subscribtion_link_M");

    // Hides the administration link
    $("#admin_results_link").hide();    
    
    // Highlights the selected link
    highlightSelectedLink("#subscribtion_link_" + status);
    
    // Displays the animated images
    $("#subscribtion_ajax_animation").show();
    $("#results_ajax_animation").show();
    
    // Triggers the server call 
    $.post(/* url  */     "/update/status",
           /* data */     {tournament_id: tournament_id, status:status },
           /* callback */ function(data) {
                               $("#statistics").empty().append(data.statistics);
                               $("#results").empty().append(data.results);
                               $("#results_ajax_animation").hide();
                               $("#admin_results_link").show(); 
                               // No need to reset the other altered components since they get refreshed as well
                          });	    
	    
}

function postComment(tournament_id) {
    
    var comment = $("#comment_textarea")[0].value;
    
    if (comment) {
        
        // Disable the commenting components
        $("#comment_button").attr("disabled", true);
        $("#comment_textarea").attr("disabled", true);
        
        // Displays the animated image
        $("#comment_ajax_animation").show();
        
        // Triggers the server call
        $.post(/* url  */     "/add/comment",
               /* data */     {tournament_id: tournament_id, comment:comment},
               /* callback */ function(data) {
                                  $("#comments").empty().append(data.comments);
                                  $("#comment_ajax_animation").hide();
                                  $("#comment_textarea")[0].value = "";
                                  $("#comment_textarea").attr("disabled", false);
                                  $("#comment_button").attr("disabled", false);
                              });    
    }
    
}

