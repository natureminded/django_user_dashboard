$( document ).ready(function() {

    $( '.index_msg, .success' ).fadeOut(3000);

    $( '#remove' ).click(function() {
        console.log("CLICKED")
        return confirm("Are you sure (cannot be undone)?");
    });

});
