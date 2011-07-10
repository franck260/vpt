function disableLink(linkId) {
    
    $(linkId).removeAttr("href");
    $(linkId).css( {"text-decoration": "none",
                    "color": "grey"} );
    
}

function highlightSelectedLink(linkId) {
    
    $(linkId).css( {"font-style": "italic",
                    "color": "black"} );
    
}


function updateStatus(tournament_id, status) {

    // Disables all subscribtion links
    disableLink("#subscribtion_link_A");
    disableLink("#subscribtion_link_P");
    disableLink("#subscribtion_link_M");
    
    // Highlights the selected link
    highlightSelectedLink("#subscribtion_link_" + status);
    
    // Displays the animated image
    $("#subscribtion_ajax_animation").show();
    
    // Triggers the server call 
    $.post(/* url  */     "/updateStatus",
           /* data */     {tournament_id: tournament_id, status:status },
           /* callback */ function(data) {
                               $("#statistics").load("/statistics/" + tournament_id);
                               $("#results").load("/results/" + tournament_id);
                               // No need to reset the altered components since they get refreshed as well
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
        $.post(/* url  */     "/addComment",
               /* data */     {tournament_id: tournament_id, comment:comment },
               /* callback */ function(data) {
                                  $("#comments").load(/* url  */     "/comments/" + tournament_id,
                                                      /* callback */ function(data) {
                                                                         $("#comment_ajax_animation").hide();
                                                                         $("#comment_textarea")[0].value = "";
                                                                         $("#comment_textarea").attr("disabled", false);
                                                                         $("#comment_button").attr("disabled", false);
                                                                     });
                              });    
    }
    
}

