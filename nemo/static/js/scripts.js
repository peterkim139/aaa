
//////////////////////  datepicker  range dates  //////////////////////////////

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
                valid_month: true
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

    $("#cancel_request").on('click',function (e) {
        if($("#cancel_rent").valid()){
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

    $(".cancel_request_yes").on('click',function(){
         $( "#cancel_rent" ).submit();
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
            'zip_code': {
                required: true,
                digits: true,
            },
            'first_name': {
                required: true,
                only_letters: true,
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


    $("#image-uploader").each(function(){
               var id = $(this).attr('id');
               imageUpload(id);
    });

    function imageUpload(id){
        return new qq.FileUploader({
            element: document.getElementById(id),
            'action': '/profile/upload_image/',
            'debug': false,
            multiple: false,
            sizeLimit: 2 * 1024 * 1024, // max size
            minSizeLimit: 0, // min size
            allowedExtensions: ['jpg', 'jpeg', 'png', 'gif'],
            onSubmit: function(id, fileName){
                if ($('.qq-upload-list').has('li')) {
                    $('.qq-upload-list').html('');
                }
            },
            onProgress: function(id, fileName, responseJSON){

            },
            onComplete: function(id, fileName, responseJSON){
                if(responseJSON.filename){
                    $('.qq-upload-file').append(" - "),
                    $('.qq-upload-failed-text').text(''),
                    $('#filename').val(responseJSON.filename),
                    $('#preview_image').attr('src','/media/images/items/'+responseJSON.filename)
                }
            },
            onCancel: function(id, fileName){$('.qq-upload-button').removeClass('.qq-upload-button-visited')},
            messages: {
                sizeError: "Your photo(s) couldn't be uploaded. Photos should be less than 2 MB and saved as JPG, JPEG, GIF or PNG files. ",
                typeError: "Your photo(s) couldn't be uploaded. Photos should be less than 2 MB and saved as JPG, JPEG, GIF or PNG files. ",
            },
            showMessage: function(message){
                $.jGrowl(message,{theme: 'jGrowlError'});
            }
        });
    }

    //////////////////////////////////////////// Validate if image is uploaded /////////////////////////////////////

    $.validator.addMethod("image_uploaded",
        function(value, element) {
            value == '' ? value = false : value = true;
            return value;
         },
    "This field is required");

    ///////////////////////////////////// Add Listing Fօrm Validation //////////////////////////////////////////////

    $("#add_listing_form").validate({

        ignore:[], // to validate hidden fields
        rules: {
            'street_address': {
                required: true,
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
                digits: true,
                maxlength: 3,
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

    ///////////////////////  preview add listing form //////////////////////////

    $('#add_listing_form_preview').hide();
    $("#preview_add_listing_form").on('click',function(e){
        if($("#add_listing_form").valid()){
                e.preventDefault();
                $("#add_listing_form_preview").show();
                $("#preview_location").text($("#street_address").val())
                $("#preview_title").text($("#name").val());
                $("#preview_category").text($("#id_subcategory option:selected").text());
                $("#preview_description").text($("#description").val());
                $("#preview_price").text($("#price").val());
                $("#add_listing_form").hide();
        }
    })

    $("#edit_add_listing_form").on('click',function(e){
        $("#add_listing_form_preview").hide();
        $("#add_listing_form").show();
    })

    $("#submit_add_listing_form").on('click',function(e){
        $( "#add_listing_form" ).submit();
    })
})

/////////////////////  set data in cookie /////////////////////////////////

     function setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays*24*60*60*1000));
        var expires = "expires="+d.toUTCString();
        document.cookie = cname + "=" + cvalue + "; " + expires;
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
        setCookie('lat_lng',cvalue,30)
    }

 /////////////////////////     init map ,show items on map /////////////////////////

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
        zoom: 8,
        center: {lat: parseFloat(latitude), lng: parseFloat(longitude)},
    });

    var myLatLng = {lat: parseFloat(latitude), lng: parseFloat(longitude)};

    var my_marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        icon: window.user,
        title: 'Your Location!'
    });

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


            var content = '<div class="singleMapVendor" style="width:100%;" data-id="'+id+'"><p>'+
            $(this).children('.item_name').text()+'</p><p>'+
            $(this).children('.item_description').text()+'</p><p>'+
            $(this).children('.item_price').text()+
            '</p><img class="item_image" src="'+$(this).children('.item_image').attr('src')+'"/></div>';

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

