
//////////////////////           datepicker  range dates            //////////////////////////////

function validateDateRange() {

    var txtStartDate = $("#id_start_date");
    var txtEndDate = $("#id_rent_date");
    var startDate;
    var endDate;
    var tempDate;
    startDate = new Date(txtStartDate.val());
    endDate = new Date(txtEndDate.val());
    for (i = 0; i < dateRange.length; i++) {
        var temp = dateRange[i].split("-");
        tempDate = new Date(temp[0], temp[1]-1, temp[2]);
        if (startDate < tempDate && endDate > tempDate) {
            $("#id_start_date").val('');
            $("#id_rent_date").val('');
            alert("Invalid Date Range");
            return false;
        }
    }

}
$(document).ready(function(){

////////////////////////////////////////////////  datepicker validation ////////////////////////////////////

    $("#id_start_date").blur(function(){
        val = $(this).val();
        val1 = Date.parse(val);
        if (isNaN(val1)==true && val!==''){
            $(this).val("")
        }
    });

    $("#id_rent_date").blur(function(){
        val = $(this).val();
        val1 = Date.parse(val);
        if (isNaN(val1)==true && val!==''){
            $(this).val("")
        }
    });

///////////////////////////////////////////// seller cancel transaction after approving ///////////////////////////////

    $("#cancel_rent").validate({
        rules: {

            'card_number': {
                required: true,
                digits: true,
                minlength: 15,
                minlength: 16,
            },
            'cvv': {
                required: true,
                digits: true,
                minlength: 4,
                minlength: 3,
            },
            'month': {
                required: true,
                digits: true,
                minlength: 2,
                minlength: 2,
            },
            'year':{
                required: true,
                digits: true,
                minlength: 4,
                minlength: 4,
            },

        },
        messages: {

            'card_number': {
                required: "Enter your card number"
            },
            'cvv': {
                required: "Enter your card cvv"
            },
            'month': {
                required: "Enter your card expired month"
            },
            'year':{
                required: "Enter your card expired year"
            },

        },
        errorClass: "help-inline",
            errorElement: "span",
            highlight: function(element, errorClass, validClass){
                $(element).parents('.control-group').addClass('error');
                $(element).parents('.control-group').removeClass('success');
            },
            unhighlight: function(element, errorClass, validClass){
                $(element).parents('.control-group').removeClass('error');
                $(element).parents('.control-group').addClass('success');
            }
    });

    $("#cancel_request").on('click',function (e) {
        e.preventDefault();
        var src = '';
        amount == '2' ? src = '#cancel_request_popup_2' : src = '#cancel_request_popup_5';
        $.magnificPopup.open({
            items: {
                src: src,
            },
            showCloseBtn: false,
        });

    })

    $(".cancel_request_yes").on('click',function(){
         $( "#cancel_rent" ).submit();
         $.magnificPopup.close();
    })

    $(".cancel_request_no").on('click',function(){
         $.magnificPopup.close();
    })

    $(".approve").on('click',function(){
        var type = $(this).val();
        $('.action').val(type);
    })
    //////////////////////////////////////////// Validate only letters /////////////////////////////////////

    $.validator.addMethod("only_letters",
        function(value, element) {
        value = value.match(/^[a-zA-Z\s]+$/)
        value == null ? value = false : value = true;
        return value;
    }, "Please enter only letters");

    ///////////////////////////////////// Registr form validation //////////////////////////////////////////////



    $("#registration").validate({
        rules: {
            'email': {
                required: true,
                email: true
            },
            'phone_number': {
                required: true,
                digits: true,
            },
            'first_name': {
                required: true,
                only_letters: true
            },
            'last_name':{
                required: true,
                only_letters: true
            },
            'password':{
                required: true,
            },
            'confirmpassword':{
                required: true,
                equalTo: "#id_password",
            }

        },
        messages: {
            'email': {
                required: "This field is required."
            },
            'phone_number': {
                required: "This field is required."
            },
            'first_name': {
                required: "This field is required.",
            },
            'last_name':{
                required: "This field is required.",
            },
            'password':{
                required: "This field is required."
            },
            'confirmpassword':{
                required: "This field is required.",
                equalTo: "Password and Confirm Password must match"
            }

        },
        errorClass: "help-inline",
            errorElement: "span",
            highlight: function(element, errorClass, validClass){
                $(element).parents('.control-group').addClass('error');
                $(element).parents('.control-group').removeClass('success');
            },
            unhighlight: function(element, errorClass, validClass){
                $(element).parents('.control-group').removeClass('error');
                $(element).parents('.control-group').addClass('success');
            }
    });
})