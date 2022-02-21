var error = false;
$('.continuebutton').click(function () {

    if ($('.registerhome').hasClass('selected')) {
        if ($('#one').hasClass('active')) {
            $('.registerhome').hide();
            $('#one').removeClass('active');
            $('#two').addClass('active');
            $('.gymstudio-step-one').show();
            $('.backbutton').show();
            return error;

        } else if ($('#two').hasClass('active')) {
            $("#registeration_form").validate({
                // Specify validation rules
                rules: {
                    facility_name: "required",
                    first_name: "required",
                    last_name: "required",
                    country: "required",
                    brand_name: "required",
                    associate_brand: "required",
                    lastname: "required",
                    email: {
                        required: true,
                        email: true
                    },
                    password: {
                        required: true,
                        minlength: 5
                    }
                },
                messages: {
                    facility_name: "Please enter your facility name",
                    country: "Please enter your country",
                    associate_brand: "Please enter your associate brand",
                    firstname: "Please enter your first name",
                    brand_name: "Please enter your brand name",
                    lastname: "Please enter your last name",
                    password: {
                        required: "Please provide a password",
                        minlength: "Your password must be at least 5 characters long"
                    },
                    email: "Please enter a valid email address"
                },
                submitHandler: function (form) {
                    var emailVal = $('#email').val()
                    var token = $("[name=csrfmiddlewaretoken]").val();

                    $.ajax({
                        type: 'POST',
                        url: 'otp_send',
                        data: { 'emailVal': emailVal, csrfmiddlewaretoken: token },
                        beforeSend: function () {
                            // setting a timeout

                            $('#payloader').show();
                        },
                        success: function (response) {
                            $('#payloader').hide();

                            if (response == 'True') {
                                alert('user exist')
                                $('#email').focus()
                                console.log('user exist', response)
                            } else {
                                $('.gymstudio-step-one').hide();
                                $('.gymstudio-step-two').show();
                                $('#btn_dv').hide();
                                $('#finl_dv').show();
                                $('#two').removeClass('active');
                                $('#three').addClass('active');
                            }

                        },
                        error: function (response) {
                            $('#payloader').hide();
                            console.log('error', response)
                        }
                    })
                    return error;
                }
            });
        }
    } else {
        alert('You must have to select type of registration');
        return error;
    }
});
$('.backbutton').click(function () {

    if ($('#two').hasClass('active')) {
        $('.registerhome').removeClass('selected');
        $('#registrationtype').val('');
        $('.registerhome').show();
        $('.gymstudio-step-one').hide();
        $('#one').addClass('active');
        $('#two').removeClass('active');
        $('.backbutton').hide();

    } else if ($('#three').hasClass('active')) {

        $('#finl_dv').hide();
        $('#btn_dv').show();
        $('.gymstudio-step-one').show();
        $('.gymstudio-step-two').hide();
        $('#three').removeClass('active');
        $('#two').addClass('active');

    } else if ($('#four').hasClass('active')) {
        $('.gymstudio-step-two').show();
        $('.gymstudio-step-three').hide();
        $('#three').addClass('active');
        $('#four').removeClass('active');

    }
});

$('.gymStudio').click(function () {
    $('.registerhome').addClass('selected');
    $('#registrationtype').val('Gym&Studio');

});
$('.sportsCoach').click(function () {
    $('#registrationtype').val('Sports&Coach');
});
$('.resendbutton').click(function () {
    var emailVal = $('#email').val()
    var token = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        type: 'POST',
        url: 'otp_send',
        data: { 'emailVal': emailVal, csrfmiddlewaretoken: token },
        beforeSend: function () {
            $('#payloader').show();
        },
        success: function (response) {

            $('#payloader').hide();
            if (response == 'True') {
                alert('user already exist')
                // console.log('user already exist')
            } else {
                // console.log('success1', response)
            }

        },
        error: function (response) {
            $('#payloader').hide();
            // console.log('error', response)
        }
    })
    return error;
});

$('.submitbutton').click(function () {

    $('#otp1').valid()
    $('#otp2').valid()
    $('#otp3').valid()
    $('#otp4').valid()
    var getotp1 = $('#otp1').val()
    var getotp2 = $('#otp2').val()
    var getotp3 = $('#otp3').val()
    var getotp4 = $('#otp4').val()
    var token = $("[name=csrfmiddlewaretoken]").val();

    if ($('#otp1').valid() && $('#otp2').valid() && $('#otp3').valid() && $('#otp4').valid()) {
        $.ajax({
            type: 'POST',
            url: 'otp_verify',
            data: { 'getotp1': getotp1, 'getotp2': getotp2, 'getotp3': getotp3, 'getotp4': getotp4, csrfmiddlewaretoken: token },
            success: function (response) {
                console.log('success', response)
                if (response == 1) {
                    // console.log('if', response)
                    // $("#registeration_form").submit(function (e) {
                    var form = $("#registeration_form");
                    // console.log('if form', response)
                    // preventing from page reload and default actions
                    // e.preventDefault();
                    // // serialize the data for sending the form data
                    // var serializedData = JSON.stringify(form.serializeArray());
                    // var serializedData = form.serializeObject();
                    // JSON.stringify(o);
                    var serializedData = form.serializeArray().reduce(function (obj, item) {
                        obj[item.name] = item.value;
                        return obj;
                    }, {});
                    // console.log('form datas', serializedData);
                    // make POST ajax call
                    $.ajax({
                        type: 'POST',
                        url: "register",
                        data: { 'serializedData': serializedData, csrfmiddlewaretoken: token },
                        success: function (json) {
                            location.href="login" 
                            // on successfull creating object
                            // 1. clear the form.
                            // console.log('success test', json)
                        },
                        error: function (response) {
                        }
                    })
                } else {
                    alert('please enter valid otp')
                    // console.log('else', response)
                }
            },
            error: function (response) {
                // console.log('error', response)
            }
        })
    } else {

    }
    return false
});




