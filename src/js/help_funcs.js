function changecolrs() {
    if(isLight) {
        $('body').css('background-color','#292929');
        $('#displaydiv').css('background-color','#363535');
        $('#VA').css('color', '#ffffff');
        $('#IE').css('color', '#ffffff');
        $('#bar').css('color', '#ffffff');
        $('#OR').css('color', '#ffffff');
        $('#slash').css('color', '#ffffff');
        $('#changecolors').html("Go to Light");
        $('#soundslabel').css('color', '#ffffff');
        $('#selectsound').css('border', '3px solid white');
        $('#selectsound').css('color', '#ffffff');
        $('#selectsound').css('background-color', '#000000');
        $('.optS').css('background-color', '#292929');
        $('#back_figure').css('background-color','#87918F');
        $('#changecolors').removeClass('w3-black').addClass('w3-white');
        $('#navbar').removeClass('navbar-light').addClass('navbar-dark');
        $('#navbar').css('background-color', '#000000');
        $('#eventfield').css('color', '#ffffff');
        isLight = false;
    }
    else{
        $('body').css('background-color','white');
        $('#displaydiv').css('background-color', '#e8e8e7');
        $('#back_figure').css('background-color','#F5F5DC');
        $('#selectsound').css('border', '3px solid black');
        $('#selectsound').css('color', '#000000');
        $('#selectsound').css('background-color', '#ffffff');
        $('.optS').css('background-color', '#ffffff' );
        $('#OR').css('color', '#000000');
        $('#slash').css('color', '#000000');
        $('#VA').css('color', '#000000');
        $('#IE').css('color', '#000000');
        $('#bar').css('color', '#000000');
        $('#soundslabel').css('color', '#000000');
        $('#changecolors').html("Go to Dark");
        $('#changecolors').removeClass('w3-white').addClass('w3-black');
        $('#navbar').removeClass('navbar-dark').addClass('navbar-light');
        $('#navbar').css('background-color', '#ffffff');
        $('#eventfield').css('color', '#000000');
        isLight = true;
    }
    for (let i=0; i<11; i++){
        let button = $('#filt_' + i);
        if (button.hasClass('w3-white'))
            button.removeClass('w3-white').addClass('black');
        else
            button.removeClass('black').addClass('w3-white');
    }
}


setInterval(function(){
    if($(window).width()*0.96>$('#displaydiv').width())
        $('#displaydiv').css('min-width',$(window).width()*0.96);
    if($(window).height()*0.95>$('#displaydiv').height())
        $('#displaydiv').css('min-height',$(window).height()*0.95);
},0);

// for calculating lag
setInterval(() => {
    if(last_events_count > lag_figures_per_second) {
        animation_flag = false;
    }
    else if(last_events_count < lag_figures_per_second) {
        animation_flag = true;
    }
    last_events_count = 0;
}, 1000);

$(document).ready(function () {
    getStateFromCookies();
    $('#displaydiv').css('min-height',$('#displaydiv').height());
    let for_comfort_scroll = 60;
    $('#eventfield').scroll(function(){
        scrolledDown = $(this).scrollTop() >= $('#eventfield')[0].scrollHeight - $('#eventfield').height() - for_comfort_scroll;
    });
});

function changehovercolor(clas){
    if(!isLight)
        $(`.${clas}`).css('background-color','#333333')
    else
        $(`.${clas}`).css('background-color','#f2f2f2')
}
function changeunhovercolor(clas){
    $(`.${clas}`).css('background-color','inherit')
}