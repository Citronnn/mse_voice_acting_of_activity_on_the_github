window.onunload = function(){
    saveStateInCookies();
};

function setCookie(name,value,days = 1) {
    let expires = '';
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = '; expires='+ date.toUTCString();
    }
    document.cookie = name + '=' + value + expires + '; path=/';
}

function getCookie(name) {
    let nameEQ = name + '=';
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0)=== ' '){
            c = c.substring(1, c.length);
        }
        if (c.indexOf(nameEQ) === 0) {
            return c.substring(nameEQ.length, c.length);
        }
    }
    return null;
}

function  deleteCookie(name) {
    setCookie(name, '', -1);
}

function saveStateInCookies() {
    setCookie("isLight", isLight);
    setCookie("volume", $("#volinp").val());
    setCookie("organization", $("#organization").val());
    setCookie("repos", $("#repos").val());
    let tmp_mass =  $("input:image");

    for ( let key in tmp_mass){
        let black = $( "#"+tmp_mass[key].id ).hasClass( "black" );
        let white = $( "#"+tmp_mass[key].id ).hasClass( "w3-white" );
        let checked = isLight ? black : white;

        setCookie(tmp_mass[key].id, checked);
    }
}

function getStateFromCookies() {


    let isL = getCookie("isLight");
    let vol = getCookie('volume');
    let organization = getCookie('organization');
    let repos = getCookie('repos');
    let tmp_mass = $("input:image");

    if(isL == "false") {
        $('body').css('background-color','#292929');
        $('#displaydiv').css('background-color','#363535');
        $('#VA').css('color', '#ffffff');
        $('#OR').css('color', '#ffffff');
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
        for (let i=0; i<11; i++){
            let button = $('#filt_' + i);
            if (button.hasClass('w3-white'))
                button.removeClass('w3-white').addClass('black');
            else
                button.removeClass('black').addClass('w3-white');
        }
    }
    else{
        $('body').css('background-color','white');
        $('#displaydiv').css('background-color', '#e8e8e7');
        $('#back_figure').css('background-color','#F5F5DC');
        $('#selectsound').css('border', '3px solid black');
        $('#selectsound').css('color', '#000000');
        $('#selectsound').css('background-color', '#ffffff');
        $('.optS').css('background-color', '#ffffff' );
        $('#VA').css('color', '#000000');
        $('#OR').css('color', '#000000');
        $('#IE').css('color', '#000000');
        $('#bar').css('color', '#000000');
        $('#OR').css('color', '#000000');
        $('#slash').css('color', '#000000');
        $('#soundslabel').css('color', '#000000');
        $('#changecolors').html("Go to Dark");
        $('#changecolors').removeClass('w3-white').addClass('w3-black');
        $('#navbar').removeClass('navbar-dark').addClass('navbar-light');
        $('#navbar').css('background-color', '#ffffff');
        $('#eventfield').css('color', '#000000');

        isLight = true;
    }


    let numVol = Number(vol) >= 0;

    if(vol !== undefined && numVol >= 0 && numVol<=100 ) {
        $("#volinp").val(vol);
    }

    else{
        removeCookiesWithSettings();
        return;
    }

    if(organization !== undefined && repos !== undefined) {
        $("#organization").val(organization);
        $("#repos").val(repos);
    }
    let checkCounter = 0;
    if(getCookie("filt_0") == "true") {
        use_all_filters_flags();

        if (isL == "true") {
            $('#filt_0').removeClass('w3-white').addClass('black');
        }
        else {
            $('#filt_0').removeClass('black').addClass('w3-white');
        }
        return;
    }

    for ( let key in tmp_mass){
        let state = getCookie(tmp_mass[key].id+"");

        if(state !== undefined ){
            if (state == "true" ) {
                filterChange(tmp_mass[key].id[5]);
                if(tmp_mass[key].id[5] == "1") {
                    filterChange(tmp_mass[key].id[5]);
                }
                checkCounter++;
            }
            else{
                $("#" + tmp_mass[key].id).prop('checked', false);
            }
        }
    }

    if(checkCounter == 0) {
        filterChange();
        removeCookiesWithSettings()
    }
}

function removeCookiesWithSettings() {
    deleteCookie("isLight");
    deleteCookie('volume');
    deleteCookie('organization');
    deleteCookie('repos');
    let tmp_mass = $("input:image");

    for (let key in tmp_mass) {
        deleteCookie(tmp_mass[key].id + "");
    }

    $("#volinp").val(20);
    $("#1").prop('checked', true);
}
