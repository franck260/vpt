$(document).ready(function() {

    $("#nav-wrap").prepend("<div id='menu-icon'>Menu</div>");

    $("#menu-icon").on("click", function(){
        $("#nav").slideToggle();
        $(this).toggleClass("active");
    });

});