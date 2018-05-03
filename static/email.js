function myFunction() {
    url = "{{url_for('check')}}"
    $.ajax({
    url: url,
    type: "get", 
    data: {  
        EmailAddress: $("#email").val()
    },
    success: function(response) {
        $("#mybox").removeClass('error')
        $("#mybox").addClass("success");
        $("#mybox").html("Username already exists")
        $("#submit").prop( "disabled", true )
    },
    error: function(xhr) {
        $("#mybox").removeClass('success')
        $("#mybox").addClass("error")
        $("#mybox").html("Good to go")
        $("#submit").prop( "disabled", false )
    }
    });
}
