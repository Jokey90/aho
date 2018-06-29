$(function() {
    $('.file-upload input[type="file"]').change(function(e){
        if (this.value != '') {
            $(e.target.parentNode).addClass('selected');
        } else {
            $(e.target.parentNode).removeClass('selected');
        }
    });
});
