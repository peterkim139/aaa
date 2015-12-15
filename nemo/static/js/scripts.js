$(document).ready(function() {


     //////////////////////           Rent date datepicker               //////////////////////////////

    var dateToday = new Date();
    $('#id_rent_date').datepicker({
             dateFormat: "yy-mm-dd",
             minDate: dateToday
    });

})
