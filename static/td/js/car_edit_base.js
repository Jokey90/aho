var url = document.location.toString();
if (url.match('#')) {
    $('.nav-tabs a[href="#'+url.split('#')[1]+'"]').tab('show') ;
}
var form_data = $('#car').serialize();
var saving = false;

$(window).bind('beforeunload', function() {
    if ($('#car').serialize() != form_data && !saving) {
        return true;
    } else {
        e = null;
    }
});

/*// With HTML5 history API, we can easily prevent scrolling!
$('.nav-tabs a').on('shown.bs.tab', function (e) {
    if(history.pushState) {
        history.pushState(null, null, e.target.hash);
    } else {
        window.location.hash = e.target.hash; //Polyfill for old browsers
    }
})

$(window).on('hashchange', function() {
    if (location.hash!='') {
        $('.nav-tabs a[href="'+location.hash+'"]').tab('show') ;
    } else {
        $('.nav-tabs a[href="#main"]').tab('show') ;
    }
});*/