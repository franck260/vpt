function postComment(tournament_id) {
	
    var commentaire = $('#commentaire')[0].value;
    
    $.post(/* url  */     "/addComment",
    	   /* data */     {tournament_id: tournament_id, comment:escape(commentaire) },
    	   /* callback */ function(data) {
                              $("#comments").load("/comments/" + tournament_id);
                          });
    
}


function updateStatus(tournament_id, statut) {

    $.post(/* url  */     "/updateStatus",
     	   /* data */     {tournament_id: tournament_id, statut:statut },
     	   /* callback */ function(data) {
                               $("#statistics").load("/statistics/" + tournament_id);
                               $("#results").load("/results/" + tournament_id);                             
                           });

    
}
