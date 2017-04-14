$(function() {
	var suggestion_type_value = "0";
	var gender_value = "0";

    // Submit post on submit
    $('#post-form').on('submit', function(event){
        event.preventDefault();
		$('#msg-box').hide();
        console.log("Form submitted")  // sanity check
        create_post();
    });
	
	$( "#btn-yes" ).click(function() {
	  $( "#btn-yes" ).addClass("active");
	  $( "#btn-maybe" ).removeClass("active");
	  $( "#btn-no" ).removeClass("active");	
	  suggestion_type_value = "0";	  
	});
	
	$( "#btn-no" ).click(function() {
	  $( "#btn-yes" ).removeClass("active");
	  $( "#btn-maybe" ).removeClass("active");
	  $( "#btn-no" ).addClass("active");
	  suggestion_type_value = "2";
	});
	
	$( "#btn-maybe" ).click(function() {
	  $( "#btn-yes" ).removeClass("active");
	  $( "#btn-maybe" ).addClass("active");
	  $( "#btn-no" ).removeClass("active");	
	  suggestion_type_value = "1";
	});
	
	$( "#btn-girl" ).click(function() {
	  $( "#btn-girl" ).addClass("active");
	  $( "#btn-boy" ).removeClass("active");
	  gender_value = "0";	  
	});
	
	$( "#btn-boy" ).click(function() {
	  $( "#btn-boy" ).addClass("active");
	  $( "#btn-girl" ).removeClass("active");
	  gender_value = "1";	  
	});

    // AJAX for posting
    function create_post() {
        console.log("Submitting suggestion") // sanity check
        $.ajax({
            url : "submit_suggestion", // the endpoint
            type : "POST", // http method
            data : { 
				name : $('#id_name.form-control').val(),
				suggestion_type : suggestion_type_value,
				gender : gender_value
				},

            // handle a successful response
            success : function(json) {
				console.log(json);
				$('#id_name.form-control').val(json.new_value);
				$('#msg-box').html(json.html_message);
				$('#msg-box').show();			
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#msg-box').html(errmsg);
				$('#msg-box').show();
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});