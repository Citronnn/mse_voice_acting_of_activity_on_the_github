var filter_flags = [];
function filterChange(id){
    filter_flags=[];
    let button = $('#filt_' + id);
    if (button.hasClass('w3-white')) {
        button.removeClass('w3-white').addClass('black');
    }
    else {
        button.removeClass('black').addClass('w3-white');
    }

    let filter_json = {type: 'filter_types'};
    for (let i = 1; i <= 9; i++) {
        let button = $('#filt_' + i);
        if (button.hasClass('w3-white'))
            filter_json[button.val()] = !isLight;
        else
            filter_json[button.val()] = isLight;
        if(filter_json[button.val()]===true) {
            filter_flags.push(button.val());
        }
    }
    button = $('#filt_0');
    if(filter_flags.length===9) {
        button = $('#filt_0');
        if (button.hasClass('w3-white') && isLight) {
            button.removeClass('w3-white').addClass('black');
        }
        else if (button.hasClass('black') )
            button.removeClass('black').addClass('w3-white');
    }
    else if (filter_flags.length!==9){
        if(button.hasClass('w3-white') && !isLight){
            button.removeClass('w3-white').addClass('black');
        }
        else if(button.hasClass('black') && isLight)
            button.removeClass('black').addClass('w3-white');
    }
    filterChoose(filter_json);
}

function use_all_filters_flags() {
    let filter_json = {type:'filter_types'};
    filter_flags=[];
    if($('#filt_0').hasClass('w3-white')){
        $('#filt_0').removeClass('w3-white').addClass('black');
    }
    else if($('#filt_0').hasClass('black'))
        $('#filt_0').removeClass('black').addClass('w3-white');
    for (let i = 1; i <= 9; i++){
        let button = $('#filt_' + i);
        if($('#filt_0').hasClass('w3-white')!==isLight) {
            filter_flags.push(button.val());
            if (button.hasClass('w3-white') && !isLight) {
                button.removeClass('w3-white').addClass('black');
            }
            else if (button.hasClass('black') && isLight) {
                button.removeClass('black').addClass('w3-white');
            }
        }
        if (button.hasClass('w3-white')) {
            button.removeClass('w3-white').addClass('black');
        }
        else {
            button.removeClass('black').addClass('w3-white');
        }
        filter_json[button.val()] = true;
    }
    filterChoose(filter_json);
}


$(document).ready(function () {
    $(document).on('input', '#organization', function(){
        orgChoose();
        $('#organization').removeClass('error_filter_org')
    });
    $(document).on('input', '#repos', function(){
        orgChoose();
        $('#repos').removeClass('error_filter_org')
    });
    orgChoose();
});