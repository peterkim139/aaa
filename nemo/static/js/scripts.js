
////////////////////////  datepicker range dates  //////////////////////////////

function validateDateRange() {
    var txtStartDate = $("#id_start_date");
    var txtEndDate = $("#id_rent_date");
    var startDate;
    var endDate;
    var tempDate;
    var error  = false
    startDate = new Date(txtStartDate.val());
    endDate = new Date(txtEndDate.val());
    for (i = 0; i < dateRange.length; i++) {
        var temp = dateRange[i].split("-");
        tempDate = new Date(temp[0], temp[1]-1, temp[2]);
        if (startDate < tempDate && endDate > tempDate) {
            txtStartDate.val('');
            txtEndDate.val('');
            return false;
        }else{
            error = true;
        }
    }
    return true;
}

$(document).ready(function(){

    $('.loader').hide();

    if(document.referrer.indexOf("payment/rent/") === -1){
        delCookie('to_billing');
    }


///////////////////////////////// to open login popup //////////////////////////////////////

    var N_login_form = $('#login_form');

    $('#contact_owner').on("click",function(){
        var link = window.location.pathname;
        N_login_form.attr('action','/login/?next='+link);
    })

    $('#request_item').on("click",function(){
        var link = window.location.pathname;
        N_login_form.attr('action','/login/?next='+link);
    })

    $('#support_redirect').on("click",function(){
        var link = window.location.pathname;
        N_login_form.attr('action','/login/?next='+link);
    })

    $('.add_listing_popup').on("click",function(){
        N_login_form.attr('action','/login/?next=/listings');
    })

    $(".login_tab").on('click', function() {
        N_login_form.attr("action", "/login/");
    });

    var login_req =  window.location.href;
    next = '/login/?'+login_req.split('?')[1]
    if(window.location.pathname == '/login_req/'){
        $('.login_tab').click()
        if ( next.indexOf('undefined') === -1 ){
            $('#login_form').attr('action',next);
        }
    }

////////////////////////////////////////////////// check cookie //////////////////////////////////////////////

    if(getCookie('exist') != ''){
        if(getCookie('exist') == 'error'){
            $('#login_password').after('<span class="incorectUP">Incorrect Email or Password</span>');
        }
        $('.popupBtn')[0].click();
        var next = getCookie('next');
        if(next != ''){
        next  = next.replace(/['"]/gi, '');
        var action = "login/?next="+next;
            N_login_form.attr('action',action);
            delCookie('next')
        }
    }
    delCookie('exist')
///////////////////////////////////////////// login form validation ///////////////////////////////////////////

    N_login_form.validate({
        rules: {
            'username': {
                required: true,
                customemail: true
            },
            'password':{
                required: true,
            },
        },
        messages: {
            'username': {
                required: "This field is required."
            },
            'password': {
                required: "This field is required."
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

    var N_cancel_rent = $("#cancel_rent");

    N_cancel_rent.validate({
        rules: {
            'card_number': {
                required: true,
                digits: true,
                minlength: 15,
                maxlength: 16,
            },
            'cvv': {
                required: true,
                digits: true,
                maxlength: 4,
                minlength: 3,
            },
            'month': {
                required: true,
                digits: true,
                minlength: 2,
                maxlength: 2,
                valid_month: true,
                month_check: true
            },
            'year':{
                required: true,
                digits: true,
                minlength: 4,
                maxlength: 4,
                valid_year: true
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

    $.validator.addMethod("valid_year", function(value, element) {
       var result
       if(value >= (new Date).getFullYear() && value <= 2050){
           result = true;
       }else{
           result = false;
       }
       return result;
    }, "Please enter a correct year.");

    $.validator.addMethod("valid_month", function(value, element) {
       var result
       if (value != 10){value = value.replace(/0/g,'')}
       if(value >= 1 && value <= 12){
           result = true;
       }else{
           result = false;
       }
       return result;
    }, "Month field can accept values from 01 to 12");

    $.validator.addMethod("month_check",
        function(value, element) {
           var dt = new Date();
           var current_month = dt.getMonth()+1;
           var current_year = dt.getFullYear();
           if(value < current_month && $('#id_year').val() == current_year){
                return false;
           }else{
                return true;
           }
        },
        "Please enter valid month");

    $("#cancel_request").on('click',function (e) {
        if(N_cancel_rent.valid()){
            var tax = $("input[name='rent']").val();
            var amount = $('tr[rent='+tax+']').attr('amount');
            var src = '';
            amount == '2' ? src = '#cancel_request_popup_2' : src = '#cancel_request_popup_5';
            $.magnificPopup.open({
                items: {
                    src: src,
                },
                showCloseBtn: false,
            });
            return false;
        }
    })
    $('#edit_user_profile').on('click',function(e){
        e.preventDefault();
        if($('#edit_profile_form').valid()){
            var latitude = parseFloat($('#latitudes').val())
            var longitude = parseFloat($('#longitudes').val())
            if(!isNaN(latitude) && !isNaN(longitude)){
                var cvalue = [latitude,longitude]
//                setCookie('lat_lng',cvalue,365)
//                setCookie('address',$('#change_address').val(),365)
            }
           $('#edit_profile_form').submit();
        }
    })

    $(".cancel_request_yes").on('click',function(){
         N_cancel_rent.submit();
         $.magnificPopup.close();
    })

    $(".cancel_request_no").on('click',function(){
         $.magnificPopup.close();
         return false;
    })

    $(".approve").on('click',function(){
        var type = $(this).val();
        $('.action').val(type);
    })
    //////////////////////////////////////////// Validate only letters /////////////////////////////////////

    $.validator.addMethod("only_letters",
        function(value, element) {
        value = value.match(/^[a-z ,.'-]+$/i)
        value == null ? value = false : value = true;
        return value;
    }, "Please enter only letters");


    //////////////////////////////////////////// Validate E-mail /////////////////

    $.validator.addMethod("customemail",
        function(value, element) {
            return /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/.test(value);
        },
        "Please enter correct email address");


    ///////////////////////////////////// Register popup //////////////////////////////////////////////

    $('#registration .birthDate label').html('BIRTHDATE:<span>(To verify you are over 18 years old)</span>')

    if(getCookie('registr_error') != ''){
        $('.registr_tab').click();
    }

    delCookie('registr_error')


    ///////////////////////////////////  forgot password ///////////////////////////////////////////////////

    var forgot = getCookie('forgot_error');
    if(forgot != '' && forgot != 'invalid_key'){
        $('.forgot_tub').click();
    }else{
        if(forgot == 'invalid_key'){
            $('.forgot_tub').click();
        }
    }
    delCookie('forgot_error')

    $('#forgot_form').validate({
        rules: {
            'email': {
                required: true,
                customemail: true
            },
        },
        messages: {
            'email': {
                required: "This field is required."
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
    })

    $('.chatWrapper').hide();
    ///////////////////////////////////// Register form validation //////////////////////////////////////////////

    $.validator.addMethod("birthday",
        function(value, element) {
            if($('#id_birthdate_month').val() == '' || $('#id_birthdate_year').val() == '' || $('#id_birthdate_day').val() == ''){
                return false;
            }else{
                return true;
            }
        },
        "All fields are required.");

    $("#registration").validate({
        rules: {
            'email': {
                required: true,
                customemail: true
            },
            'phone_number': {
                required: true,
                digits: true,
                minlength:10,
                maxlength:10,
            },
            'zip_code': {
                required: true,
                digits: true,
                minlength:5,
                maxlength:5,
            },
            'first_name': {
                required: true,
                only_letters: true,
                minlength:2,
            },
            'last_name':{
                required: true,
                only_letters: true,
                minlength:2,
            },
            'password':{
                required: true,
            },
            'birthdate_year':{
                birthday: true
            }
        },
        messages: {
            'email': {
                required: "This field is required."
            },
            'phone_number': {
                required: "This field is required.",
                minlength: jQuery.validator.format("Please enter a valid 10-digit phone number."),
                maxlength: jQuery.validator.format("Please enter a valid 10-digit phone number."),
            },
            'zip_code': {
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

    $("#image-uploader").each(function(){
               var id = $(this).attr('id');
               imageUpload(id);
    });

    $(".loginPopup #id_birthdate_year").prepend("<option value=''>Year</option>").val('');
    $(".loginPopup #id_birthdate_day").prepend("<option value=''>Day</option>").val('');

    function imageUpload(id){
        return new qq.FileUploader({
            element: document.getElementById(id),
            'action': '/profile/upload_image/',
            'debug': false,
            multiple: false,
//            sizeLimit: 5 * 1024 * 1024, // max size
            minSizeLimit: 0, // min size
            allowedExtensions: ['jpg', 'jpeg', 'png', 'gif','tiff','bmp'],
            onSubmit: function(id, fileName){
                if ($('.qq-upload-list').has('li')) {
                    $('.qq-upload-list').html('');
                }
            },
            onProgress: function(id, fileName, responseJSON){
                $('.qq-upload-failed-text').text('');
            },
            onComplete: function(id, fileName, responseJSON){
                if(responseJSON.filename){
                    $('.qq-upload-file').append(" - ");
                    $('.qq-upload-failed-text').text('');
                    $('#filename').val(responseJSON.filename);
                    $('#preview_image').attr('src','/media/images/items/'+responseJSON.filename)
                }
            },
            onCancel: function(id, fileName){$('.qq-upload-button').removeClass('.qq-upload-button-visited')},
            messages: {
//                sizeError: "Your photo(s) couldn't be uploaded. Photos should be less than 2 MB and saved as JPG, JPEG, GIF or PNG files. ",
                typeError: 'Only .jpg/jpeg/png/gif/tiff/bmp files allowed.',
            },
            showMessage: function(message){
                $.jGrowl(message,{theme: 'jGrowlError'});
            }
        });
    }

    ///////////////////////////////////// Support form validation //////////////////////////////////////////////

    $("#support_form").validate({
        rules: {
            'email': {
                required: true,
                customemail: true
            },
            'name': {
                required: true,
                only_letters: true,
                minlength: 2,
            },
            'comments':{
                required: true,
            },
        },
        messages: {
            'email': {
                required: "This field is required."
            },
            'name': {
                required: "This field is required.",
            },
            'comments':{
                required: "This field is required.",
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

    ///////////////////////////////////////////// Deactivate account ////////////////

    $(".change_account_status_item").on('click',function(){
        var self = $(this)
        var status = self.attr("data-account-status");
        $.ajax({
            url:'/change_account_status/',
            type:'post',
            data:{
                status: status
            },
            success:function(response) {
                if(response && status == 0){
                    self.attr("data-account-status",1);
                    self.text("Activate");
                }else {
                    self.attr("data-account-status",0);
                    self.text("Deactivate");
                }
            },
        });
    });

    ///////////////////////////////////// Highlight menu links /////////////

    var site_pathname = window.location.pathname;
    site_pathname = site_pathname.substring(0, site_pathname.lastIndexOf('/')) + '/';
    var menu_link = $('a[href="'+site_pathname+'"]').parent('li');
    var list = ['/profile/out_transactions/', '/profile/in_transactions/', '/edit_profile/', '/payment/connect/','/billing/'];
    if(list.lastIndexOf(site_pathname) !== -1){
       $('.account').parent('li').addClass("active");
    }else{
        menu_link.addClass("active");
    }

    menu_link.addClass("active");
    if(site_pathname == '/profile/out_transactions/'){
        $('a[id="in_trans').parent('li').addClass("active");
    }

    ///////////////////////////////////// Edit profile form validation //////////////////////////////////////////////

    $("#edit_profile_form").validate({
        rules: {
            'address': {
                required: true,
                address_validated: true,
            },
            'email': {
                required: true,
                customemail: true
            },
            'phone_number': {
                required: true,
                digits: true,
                minlength:10,
                maxlength:10,
            },
            'zip_code': {
                required: true,
                digits: true,
                minlength:5,
                maxlength:5,
            },
            'first_name': {
                required: true,
                only_letters: true,
                minlength:2,
            },
            'last_name':{
                required: true,
                only_letters: true,
                minlength:2,
            },
        },
        messages: {
            'address': {
                required: "This field is required."
            },
            'email': {
                required: "This field is required."
            },
            'phone_number': {
                required: "This field is required.",
                minlength: jQuery.validator.format("Please enter a valid 10-digit phone number."),
                maxlength: jQuery.validator.format("Please enter a valid 10-digit phone number."),
            },
            'zip_code': {
                required: "This field is required."
            },
            'first_name': {
                required: "This field is required.",
            },
            'last_name':{
                required: "This field is required.",
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


    ///////////////////////////////////////////// Seller Cancel  or approve request ////////////////

    $(".seller_actions").on('click',function(){
        var self = $(this)
        $('.footable-visible button').prop('disabled', true);
        self.closest('td').find("div").show();
        var action = self.attr("action");
        var rent = self.closest('tr').attr('rent');
        $.ajax({
            url:'/profile/in_transactions/',
            type:'post',
            data:{
                action: action,
                rent: rent
            },
            success:function(response) {
                if(response.success){
                    if(action == 'Approve'){
                        self.closest('td').html('<button class="success expandBtn">Cancel</button>')
                    }else{
                        location.reload()
                    }
                    self.closest('td').find("div").hide();
                }else {
                    alert(response.message);
                }
                $('.footable-visible button').prop('disabled', false);
            },
        });
    });

    //////////////// edit listing /////////////

    $(".edit_listing_icon").on('click',function(){
        var item_id = $(this).attr('id');
        $('#item_id').val(item_id);
        $.ajax({
            url:'/edit_listing/',
            type:'post',
            async:false,
        data:{
            item_id: item_id
        },
        success:function(response) {
            response = $.parseJSON(response);
            $('#add_listing_title').text('Edit Listing')
            $('#street_address').val(response[0].fields.address)
            $('#city').val(response[0].fields.city)
            $('#street').val(response[0].fields.street)
            $('#postal_code').val(response[0].fields.postal_code)
            $('#name').val(response[0].fields.name)
            $('#description').val(response[0].fields.description)
            $('#price').val(response[0].fields.price)
            $('#latitudes').val(response[0].fields.latitude)
            $('#longitudes').val(response[0].fields.longitude)
            $('#filename').val(response[1].fields.image_name)
            $("#id_subcategory option[value="+response[0].fields.subcategory+"]").attr('selected','selected');
            $("#id_state option[value="+response[0].fields.state+"]").attr('selected','selected');
            $('#preview_image').attr('src','/media/images/items/'+response[1].fields.image_name)
        },
        });
    });

    ////////////////view more search results/////////////
    var N_viewMoreBtn = $(".viewMoreBtn");

    N_viewMoreBtn.on('click',function(){
        var url = window.location.pathname+window.location.search;
        $.ajax({
            url:url,
            type:'get',
            data:{
            },
            success:function(response) {
                response_items = $.parseJSON(response.items);
                item_div = '';
                $.each(response_items, function(index, element) {
                        item_div += '<div class="col6">'
                            +'<div class="item_details" data-id="'+element.pk+'" data-lat="'+element.fields.latitude+'" data-lng="'+element.fields.longitude+'">'
                                +'<div class="listingSingle" class="wow fadeInDown">'
                                    +'<figure class="fluidImage" style="background-image: url(/media/images/items/'+element.fields.address+');">'
                                        +'<img class="item_image" src="/media/images/items/'+element.fields.address+'">'
                                        +'<img class="imgBlock" src="/media/images/sizers/landscape-sizer.png">'
                                        +'<figcaption>Rent</figcaption>'
                                    +'</figure>'
                                    +'<div class="listingDets">'
                                        +'<div class="listDetsTop">'
                                            +'<div class="listDetsTopL">'
                                                +'<span href="#" class="listingName item_name">'+element.fields.name+'</span>'
                                                +'<div class="ownerWrap"><span class="listingBy">by '+element.fields.status+'</span><span class="stars"><img src="/media/images/rating-badges.png" alt=""></span></div>'
                                            +'</div>'
                                            +'<div class="listDetsTopR">'
                                                +'<div class="listPriceSect">'
                                                    +'<span class="listPrice item_price">$'+element.fields.price+'</span>'
                                                    +'<span class="listDuration">per day</span>'
                                                +'</div>'
                                                +'<em class="listingDist item_distance">'+element.fields.city.toFixed(2)+'<br>miles</em>'
                                            +'</div>'
                                        +'</div>'
                                        +'<a href="/payment/rent/'+element.pk+'" class="btn btnBorder btnBlock">Details</a>'
                                    +'</div>'
                                +'</div>'
                            +'</div>'
                        +'</div>';
                });
                $("#search_results_container").append(item_div);
                initMap(response.latitude,response.longitude);
                if (response.count < response.limit){
                    N_viewMoreBtn.hide();
                }
                $('.customScroll').mCustomScrollbar("scrollTo",'-=200');
            },
        });
    });

    ///////////////////////////////////////////// Customer Cancel  or approve request ////////////////

    $(".client_actions").on('click',function(){
        var self = $(this)
        var action = self.attr("action");
        var rent = self.closest('tr').attr('rent');
        $.ajax({
            url:'/profile/out_transactions/',
            type:'post',
            data:{
                action: action,
                rent: rent
            },
            success:function(response) {
                if(response.success){
                    alert(response.message);
                    self.closest('td').html('The request has been declined from your side.')
                }else {
                    alert(response.message);
                }
            },
        });
    });

    ////////////////////////////////////////// Change Billing status type////////////////

    $(".change_method_status").on('click',function(){
        var self = $(this)
        var method_id = self.attr('id');
        var status = self.attr("data-status-type");
        $.ajax({
            url:'/change_billing_status/',
            type:'post',
            data:{
                method_id: method_id,
                status: status
            },
            success:function(response) {
                if(response){
                    if (status == '1'){
                        $(".change_method_status").attr("data-status-type",'1').text("Make Default");
                        self.attr("data-status-type",'0');
                        self.text("Default Method");
                    }
                    else {
                        self.attr("data-status-type",'1');
                        self.text("Make Default");
                    }
                }
            },

        });
    });

    ////////////////////////////////////////// Delete Billing Method type////////////////

    $(".delete_billing_method").on('click',function(){
        var self = $(this)
        var method_id = self.attr('id');
        $.ajax({
            url:'/delete_billing/',
            type:'post',
            data:{
                method_id: method_id,
            },
            success:function(response) {
                if(response){
                   self.parents('li').remove();
                }
            },
        });
    });

    //////////////////////////////////////// Change listing status type////////////////

    $(".change_listing_status").on('click',function(){
        var self = $(this)
        var item_id = self.attr('id');
        var status = self.attr("data-status-type");
        $.ajax({
            url:'/profile/change_listing_status/',
            type:'post',
            data:{
                item_id: item_id,
                status: status
            },
            success:function(response) {
                if(response && status == 'deleted') {
                    self.parents('li.listing_li').remove();
                }else if(response && status == 'unpublished'){
                    self.attr("data-status-type",'published');
                    self.html("<i class='icon-play'></i>");
                    self.parents(".listingR").children(".listing_h3").find("a").attr("href", "#");
                }else {
                    self.attr("data-status-type",'unpublished');
                    self.html("<i class='icon-pause'></i>");
                    self.parents(".listingR").children(".listing_h3").find("a").attr("href", "/payment/rent/"+item_id);
                }
            },
        });
    });
    //////////////////////////////////////////// Check if address contains at least one digit /////////////////////////////////////

    $.validator.addMethod("address_validated",
        function(value, element) {
            var nemo = false;
            for (i=0;i<=9;i++){
                if (value.indexOf(i) === -1) {
                    nemo = false;
                }
                else {
                    nemo = true;
                    break;
                }
            }
            return nemo;
        },
    "This field should contain at least one digit");

    ///////////////////////////////////// Price validator for cents /////////////////////////////////////

    $.validator.addMethod("customprice", function(value, element) {
        var isValidMoney = /^\d{0,3}(\.\d{0,2})?$/.test(value);
        return this.optional(element) || isValidMoney;
    }, "Please specify a valid amount");

    ///////////////////////////////////// Validate if image is uploaded /////////////////////////////////////

    $.validator.addMethod("image_uploaded",
        function(value, element) {
            value == '' ? value = false : value = true;
            return value;
         },
    "This field is required");

    ///////////////////////////////////// Add Listing Fօrm Validation //////////////////////////////////////////////

    var N_add_listing_form = $("#add_listing_form");
    N_add_listing_form.validate({
        ignore:[], // to validate hidden fields
        rules: {
            'street_address': {
                required: true,
                address_validated: true,
            },
            'city': {
                required: true,
            },
            'state': {
                required: true,
            },
            'postal_code': {
                required: true,
                digits: true,
                maxlength: 5,
                minlength: 5,
            },
            'name':{
                required: true,
            },
            'subcategory':{
                required: true,
            },
            'description':{
                required: true,
            },
            'price':{
                required: true,
                customprice: true,
                range:[1,999.99]
            },
            'image_file':{
                image_uploaded: true,
            },
        },
        messages: {
            'street_address': {
                required: "This field is required."
            },
            'city': {
                required: "This field is required."
            },
            'state': {
                required: "This field is required."
            },
            'postal_code': {
                required: "This field is required."
            },
            'name':{
                required: "This field is required."
            },
            'subcategory':{
                required: "This field is required."
            },
            'description':{
                required: "This field is required."
            },
            'price':{
                required: "This field is required."
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

////////////////////////////////////////// reset popup /////////////////////////////////////////////////////////////

    $('#reset_form').validate({
        rules: {
            'password':{
                required: true,
                minlength: 6,
            },
            'password2':{
                required: true,
                equalTo: "#id_password_change",
            }
        },
        messages: {
            'password':{
                required: "This field is required."
            },
            'password2':{
                required: "This field is required.",
                equalTo: "Password and Repeat Password must match"
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
    })

    function openResetForm(){
        $.magnificPopup.open({
            items: {
                src: '#reset_popup',
            },
            showCloseBtn: true,
        });
    }

    if(getCookie('reset_error') != ''){
        openResetForm()
    }

    delCookie('reset_error')
    if(getCookie('reset_key_error') != ''){
        delCookie('reset_key_error')
    }

    var reset_key = getCookie('reset_key')
    if(reset_key != ''){
        $('#reset_form').attr('action','/change_password/'+reset_key+'/')
        openResetForm()
    }
    delCookie('reset_key')
    ///////////////////////  preview add listing form //////////////////////////

    $(".openSlideBtn").on('click',function(){
        var self = $(this);
        slideAnimation(self);
    });

    $(".rentSlideBtn").on('click',function(){
        var self = $(this);
        //if($(".datepicker").hasClass('not_valid') || $(this).hasClass('disableBtn') || $("#id_start_date").val() == '' || $("#id_rent_date").val()== ''){
         //   return false;
	   //}
        slideAnimation(self);
    });

    $("#preview_add_listing_form").on('click',function(e){
        var self = $(this);
        if(N_add_listing_form.valid()){
                e.preventDefault();
                slideAnimation(self);
                $("#preview_location").text($("#street_address").val())
                $("#preview_title").text($("#name").val());
                $("#preview_category").text($("#id_subcategory option:selected").text());
                $("#preview_description").text($("#description").val());
                $("#preview_price").text('$' + $("#price").val()+' per day');
        }
    })
    $("#submit_add_listing_form").on('click',function(e){
        N_add_listing_form.submit();
    })

    //////////////////////////////////////////////////////////////  change default address //////////////////////////////////////

    $('#change_default_address').on('click',function(e){
        if($('#defaul_address_form').valid()){
            e.preventDefault();
            var address = $('#default_address').val()
            var latitude = $('#default_latitudes').val()
            var longitude = $('#default_longitudes').val()
            var float_lat = parseFloat(latitude);
            var float_long = parseFloat(latitude);
            var cvalue = [latitude,longitude]
            if(longitude != ''  && longitude != '' && !isNaN(float_lat) && !isNaN(float_long)){
                setCookie('lat_lng',cvalue,365)
                setCookie('address',address,365)
                $('.valid_address').hide()
                $('#default_address').val('')
                $('#default_latitudes').val('')
                $('#default_longitudes').val('')
                initMap(latitude,longitude)
                var contents = $('.srchAddress p').contents();
                contents[contents.length - 1].nodeValue = address;
                $('.mfp-close').click()
            }else{
                $('.valid_address').show()
            }
        }
    })


    $('#defaul_address_form').validate({
        ignore:[],
        rules: {
            'default_address': {
                required: true,
            },
        },
        messages: {
            'default_address': {
                required: "This field is required."
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

})

/////////////////////////// CSRF code ///////////////////////

    function getCookie(name) {
        var cookieValue = '';
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

/////////////////////  set data in cookie /////////////////////////////////

    function setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays*24*60*60*1000));
        var expires = "expires="+d.toUTCString();
        document.cookie = cname+"="+cvalue+expires+"; path=/";
    }

    timezone = new Date().getTimezoneOffset()
    if(timezone > 0){
        timezone = -Math.abs(timezone/60)
    }else{
        timezone = Math.abs(timezone/60)
    }

    setCookie('timezone',timezone,365)

    function delCookie(name) {
        document.cookie = name + "=" + "; expires=Thu, 01 Jan 1970 00:00:01 GMT";
    }

/////////////////////// get user location ////////////////////////////

    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition);
        }
    }

    function showPosition(position) {
        $("#latitude").val(position.coords.latitude);
        $("#longitude").val(position.coords.longitude)
        var cvalue = [position.coords.latitude,position.coords.longitude]
        initMap(position.coords.latitude,position.coords.longitude)
        setCookie('lat_lng',cvalue,365)
        codeLatLng(position.coords.latitude, position.coords.longitude)
    }

    if(getCookie('address') == ''){
        getLocation();
    }

    var geocoder = new google.maps.Geocoder();

    function codeLatLng(lat, lng) {
        var latlng = new google.maps.LatLng(lat, lng);
        geocoder.geocode({'latLng': latlng}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[1]) {
                    var address =  results[0].formatted_address
                    setCookie('address',address,365)
                }
            }
        });
    }




 /////////////////////////  init map ,show items on map /////////////////////////

    function initMap(latitude,longitude) {

        window.pin = '/media/images/icons/map-pin.png';
        window.pun = '/media/images/icons/map-pun.png';
        window.user = '/media/images/icons/map-user.png'
        var markers = [];
        var latlngbounds = new google.maps.LatLngBounds();

        var map = new google.maps.Map(document.getElementById("map_canvas"), {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            frameborder: 0,
            scrollwheel: false,
            style: "border:0",
            allowfullscreen: true,
            zoom: 15,
            center: {lat: parseFloat(latitude), lng: parseFloat(longitude)},
        });

        var myLatLng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};

        var my_marker = new google.maps.Marker({
            position: myLatLng,
            map: map,
            icon: window.user,
            title: 'Your Location!'
        });

//        var circle = new google.maps.Circle({
//          map: map,
//          radius: 1600,
//          fillColor: '#AA0000'
//        });

 //       circle.bindTo('center', my_marker, 'position');

        var currentInfoWindow = null;
        var show = false;

        $('.item_details:visible').each(function(){

            var lat = $(this).attr('data-lat');
            var lng = $(this).attr('data-lng');

            if(lat && lng) {
                show = true;
                var id = $(this).attr('data-id');
                var latLng = new google.maps.LatLng(lat, lng);
                var marker = new google.maps.Marker({
                    position: latLng,
                    animation: google.maps.Animation.DROP,
                    title: $(this).children('.item_name').text(),
                    icon: window.pin,
                    map: map
                });

                markers[id] = marker;

                latlngbounds.extend(marker.position);

                $(".item_details").on('mouseenter', function () {
                    var id = $(this).attr('data-id');
                    if(typeof markers[id] != 'undefined' ) markers[id].setIcon(window.pun);
                }).on('mouseleave', function () {
                    var id = $(this).attr('data-id');
                    if(typeof markers[id] != 'undefined' ) markers[id].setIcon(window.pin);
                });

                var content = '<div class="listingOnMap listingSingle" style="width:100%;" data-id="'+id+'"><a href="/payment/rent/'+id+'">'+
                    '<figure class="fluidImage" style="background-image: url('+$(this).find('img.item_image').attr('src')+')">' +
                        '<img class="item_image" src="'+$(this).find('img.item_image').attr('src')+'"/>' +
                        '<img class="imgSizer" src="/media/images/sizers/landscape-sizer.png" />' +
                    '</figure>' +
                    '<div class="listingDets"><div class="listDetsTop">' +
                        '<div class="listDetsTopL"><span class="listingName">'+ $(this).find('span.item_name').text() + '</span></div>' +
                        '<div class="listDetsTopR"><span class="listPrice ">'+ $(this).find('span.item_price').text() + '</span></div>' +
                    '</div>' +
                '</a></div>';
                var infowindow = new google.maps.InfoWindow();

                google.maps.event.addListener(marker,'click', function(){
                    if (currentInfoWindow != null) {
                        currentInfoWindow.close();
                    }
                    infowindow.setContent(content);
                    infowindow.open(map,marker);
                    currentInfoWindow = infowindow;
                });

                google.maps.event.addListener(map, "click", function(event) {
                    infowindow.close();
                });
            }
        });
    }
    /////////////////////////////////  message sound //////////////////////////////////////
    
    function playSound(){
        document.getElementById("sound").innerHTML=
            '<audio autoplay="autoplay"><source src="/media/sounds/pling.mp3" type="audio/mpeg" />'
            + '<source src="/media/sounds/pling.ogg" type="audio/ogg" />'
            + '<embed hidden="true" autostart="true" loop="false" src="/media/sounds/pling.mp3" /></audio>';
    }
