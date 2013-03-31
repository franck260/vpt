$(document).ready(function() {

    // Binds a click event to all calendar links
    $("#poll_vote_form .cal_icon").click(function(event) {

        // Reads the actual date in the neighbor node & opens a dialog datepicker
        $(this).datepicker("dialog", $(this).prev().html(), null, null, event);

        // Cancels the actual click action
        return false;
    });

    // Binds a submit event to the results administration form
    $("#poll_vote_form").submit(function() {

        var that = this;

        // Reads the user id in the link itself
        var user_id = $(that).attr("data-user-id");

        // Serializes the form data
        var data = $(that).serialize();

        // Disables input components
        $(":input", that).attr("disabled", true);
        $("#poll_vote_unit_ajax_output").empty();

        // Displays the animated images
        $("#poll_vote_unit_ajax_animation").show();
        $("#poll_votes_ajax_animation").show();

        // Triggers the server call 
        $.post(/* url  */     "/poll/vote",
               /* data */     data,
               /* callback */ function(response) {

                                  var refresh_output = function(callback) {
                                      $("#poll_vote_unit_ajax_output").attr("class", "poll_success").hide().html("Vote pris en compte").fadeIn("slow", callback);
                                  };

                                  var user_row_selector = "#poll_votes_table tr[data-user-id='" + user_id + "']";

                                  if(response.partial) {

                                      var $current_user_row = $(user_row_selector);
                                      $current_user_row.find("td").html("&nbsp;");

                                      refresh_output(function() {

                                          if ($current_user_row.length) {
                                              $current_user_row.html($(response.data).html()).hide().fadeIn("slow"); 
                                          } else {
                                              $(response.data).appendTo($("#poll_votes_table")).hide().fadeIn("slow");
                                          }

                                      });

                                  } else {

                                      $("#poll_votes").html(response.data);
                                      var $new_user_row = $(user_row_selector).hide();

                                      refresh_output(function() {
                                          $new_user_row.fadeIn("slow");
                                      });        

                                  }

                              })
        .error(function(response) {
            $("#poll_vote_unit_ajax_output").attr("class", "poll_error").hide().html(response.responseText).fadeIn("slow");
        })
        .complete(function() {
            $("#poll_votes_ajax_animation").hide();
            $("#poll_vote_unit_ajax_animation").hide();
            $(":input", that).attr("disabled", false);       
        });

        // Cancels the actual submit action
        return false;

    });

});
