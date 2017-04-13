$(function() {
	
	$(".btn-del").click(function() {
		var suggestion_id = $(this).attr("href").substring(1);
		var suggestion_name = $(this).parent().siblings("th").text();
		var this_row = $(this);
		this_row.hide();
		this_row.next().show();
		console.log("Deleting " + suggestion_id + ":" + suggestion_name)
		$.ajax({
            url : "remove_suggestion", // the endpoint
            type : "POST", // http method
            data : { 
				name : suggestion_name,
				pk : suggestion_id
				},

            // handle a successful response
            success : function(json) {
				console.log(json);
				if (json.result == 'Success') {
					this_row.parent().parent().remove();
				} else {
					this_row.show();
					this_row.next().hide();
				}
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                //$('#msg-box').html(errmsg);
				//$('#msg-box').show();
				this_row.parent().parent().remove();
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
	});

	// AJAX for posting
    function create_post() {
        console.log("Submitting suggestion") // sanity check
        
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