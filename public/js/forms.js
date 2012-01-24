$(document).ready(function() {
    
    // Binds a submit event to all forms
    $("form").submit(function() {
        
        $("button[type=submit]", this).each(function() {
            $(this).attr("disabled", true);
            $(this).html("En cours...");
        });

    });
    
});