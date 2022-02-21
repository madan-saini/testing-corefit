
    $("#loginForm").validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
            }
        },
        messages: {
            password: {
                required: "Password field is required",
            },
            email: {
                required: "Email address field is required",
                email: "Please enter a valid email address"
            },
            
        },
        submitHandler: function (form) {
            var emailVal = $('#email').val()
            var passwordVal = $('#password').val()
            var token = $("[name=csrfmiddlewaretoken]").val();

            $.ajax({
                type: 'POST',
                url: 'login',
                data: { 'email': emailVal,'password': passwordVal,  csrfmiddlewaretoken: token },
                beforeSend: function () {
                    $('#payloader').show();
                },
                success: function (response) {
                    $('#payloader').hide();
                    console.log('hey',response)
                    if (response == 0) {
                        location.href="login" 
                    }else if(response=='False'){
                        location.href="login" 
                    }else {
                        location.href="/"
                    }
                },
                error: function (response) {
                    $('#payloader').hide();
                    console.log('error', response)
                }
            })
            return false;
        }
    });

    $("#forgotForm").validate({
        rules: {
            email: {
                required: true,
                email: true
            }
        },
        messages: {
            email: {
                required: "Email address field is required",
                email: "Please enter a valid email address"
            }
            
        },
        submitHandler: function (form) {
            var emailVal = $('#email').val()
            var token = $("[name=csrfmiddlewaretoken]").val();

            $.ajax({
                type: 'POST',
                url: 'forgotPassword',
                data: { 'email': emailVal,  csrfmiddlewaretoken: token },
                beforeSend: function () {
                    $('#payloader').show();
                },
                success: function (response) {
                    $('#payloader').hide();
                    console.log('hey',response)
                    if (response == 0) {
                        location.href="login" 
                    }else if(response=='False'){
                        location.href="login" 
                    }else {
                        location.href="/"
                    }
                },
                error: function (response) {
                    $('#payloader').hide();
                    console.log('error', response)
                }
            })
            return false;
        }
    });