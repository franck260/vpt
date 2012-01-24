$(document).ready(function() {
    
    // Gives the focus to the email field
    $("#email").focus();
	
    // Binds a click event to the recovery link
    $("#display_recover_password").click(function() {
    	
        $(this).hide();
        $("#recover_password").fadeIn("slow");
        $("#recover_password_email").focus();
        
        // Cancels the actual click action
        return false;

    });
	
    // Binds a submit event to the recovery form
    $("#recover_password_form").submit(function() {
        
    	var that = this;
        var email = $("#recover_password_email").val();
        
        if ($.trim(email).length) {
            
            // Disables input components
            $(":input", that).attr("disabled", true);
            $("#recover_password_ajax_output").empty();
            
            // Displays the animated image
            $("#recover_password_ajax_animation").show();
            
            // Triggers the server call
            $.post(/* url  */     "/recover/password",
                   /* data */     {"email" : email},
                   /* callback */ function() {
                                      $("#recover_password_ajax_output").attr("class", "login_success");
                                  })
           .error(function() {
                      $("#recover_password_ajax_output").attr("class", "login_error");
                  })
           .complete(function(response) {
                         $("#recover_password_ajax_animation").hide();
                         $("#recover_password_ajax_output").html(response.responseText).hide().fadeIn("slow");
                         $(":input", that).attr("disabled", false);
                     });
       
        }
        
        // Cancels the actual submit action
        return false;

    });

});