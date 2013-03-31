$(document).ready(function() {

    // Binds a click event to all subscription links
    $("#tournament_statistics").on("click", "a[id^='subscribtion_link']", function() {

        // Reads some information in the link itself
        var tournament_id = $(this).attr("data-tournament-id");
        var status = $(this).attr("data-status");

        // Disables all subscription links
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

                                  var fade_in_changes = function(current_section, new_section_html) {
                                      var changes_selector = $(new_section_html).find("[id^='mutable_']").filter(function() {
                                          return $(this).html() !== $("#" + this.id, current_section).html();
                                      }).map(function() {
                                          return "#" + this.id;
                                      }).get().join(", ");

                                      current_section.html(new_section_html).find(changes_selector).hide().fadeIn("slow");
                                  };

                                  var fade_out_changes = function(current_section, new_section_html) {
                                      current_section.find("[id^='mutable_']").filter(function() {
                                          return $(this).html() !== $("#" + this.id, new_section_html).html();
                                      }).fadeOut("slow");
                                  };

                                  $("#results_ajax_animation").hide();
                                  $("#admin_results_link").show();

                                  $.when(fade_in_changes($("#tournament_statistics"), response.statistics)).done(function() {
                                      $.when (fade_out_changes($("#tournament_results"), response.results)).done(function() {
                                          fade_in_changes($("#tournament_results"), response.results);
                                      });
                                  });

                              });

        // Cancels the actual submit action
        return false;

    });

});

