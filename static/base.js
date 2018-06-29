function close_message(elem){
    $(elem).fadeOut();
}

function keep_session(e){
    return false;
}

$(function(){
    setTimeout(function(){
        $('div.messages-container div.card').each(function(){
            $(this).fadeOut();
        });
    }, 5000);
    setInterval(function(){
        $.get('/aho/keep_session?'+Math.random()*10000, null, keep_session);
    }, 600000);
});

function confirm_delete(url){
    if (confirm('Подтвердите удаление объекта')){
        location.href = url;
    }
}