$(document).ready(function() {

    // Binds a submit event to the comment form
    $("#comment_form").submit(function() {

        var that = this;

        if ($.trim($("#comment").val()).length) {
         
            // Serializes the form data
            var data = $(that).serialize();
     
            // Disables input components
            $(":input", that).attr("disabled", true);
            
            // Displays the animated image
            $("#comment_ajax_animation").show();
            
            // Triggers the server call
            $.post(/* url  */      $(that).attr("action"),
                   /* data */      data,
                   /* callback */  function(response) {
                                        $(response).hide().appendTo($("#comments_list")).fadeIn("slow");
                                        $("#nb_comments").hide().html($(".comment_wrapper").length).fadeIn("slow");
                                        $("#comment_ajax_animation").hide();
                                        $("#comment").val("");
                                        $(":input", that).attr("disabled", false);
                                    });              

        }
        
        // Cancels the actual submit action
        return false;

    });
   
});

