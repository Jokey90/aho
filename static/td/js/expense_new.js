$('#id_car').on('change', function(){
    var selected_car = $('#id_car').val();
    var temp = '<option value selected="selected">---------</option>';
    var used = [];
    for (var i=0; i<drivers.length;i++){
        if (drivers[i].car_id == selected_car || selected_car == '') {
            if (used.indexOf(drivers[i].car_id)<0) {
                temp += '<option value="' + drivers[i].driver_id + '">' + drivers[i].driver_name + '</option>';
                used.push(drivers[i].car_id);
            }
        }
    }
    $('#id_driver').html(temp);
});

$('#id_budget_subitem').html(budget_selector);