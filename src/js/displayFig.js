const max_count_of_figures = 50;
const animation_time = 2000;
var animation_flag = true;
var last_events_count = 0;
const lag_figures_per_second = 8;

let colors=["#FFFFCC","#FFFF99","#FFFF66","#FFFF33","#FFFF00","#CCCC00","#FFCC66","#FFCC00","#FFCC33",
    "#CC9933","#996600","#FF9900","#FF9933","#CC9966","#CC6600","#FFCC99","#FF9966","#FF6600",
    "#CC6633","#993300","#FF6633","#CC3300","#FF3300","#FF0000","#CC0000","#990000","#FFCCCC","#FF9999",
    "#FF6666","#FF3333","#FF0033","#CC0033","#CC9999","#CC6666","#CC3333","#993333","#990033","#FF6699",
    "#FF3366","#FF0066","#CC3366","#996666","#663333","#FF99CC","#FF3399","#FF0099","#CC0066","#993366","#660033",
    "#FF66CC","#FF00CC","#FF33CC","#CC6699","#CC0099","#990066","#FFCCFF","#FF99FF","#FF66FF","#FF33FF","#FF00FF",
    "#CC3399","#CC99CC","#CC66CC","#CC00CC","#CC33CC","#990099","#993399","#CC66FF","#CC33FF","#CC00FF","#9900CC",
    "#996699","#660066","#CC99FF","#9933CC","#9933FF","#9900FF","#660099","#663366","#9966CC","#9966FF","#6600CC",
    "#6633CC","#663399","#CCCCFF","#9999FF","#6633FF","#6600FF","#9999CC","#6666FF",
    "#6666CC","#666699","#333399","#333366","#3333FF","#3300FF","#3300CC","#3333CC","#6699FF",
    "#3366FF","#0000FF","#0000CC","#0033CC","#0066FF","#0066CC","#3366CC","#0033FF",
    "#99CCFF","#3399FF","#0099FF","#6699CC","#336699","#006699","#66CCFF","#33CCFF","#00CCFF","#3399CC","#0099CC",
    "#99CCCC","#66CCCC","#339999","#669999","#006666","#336666","#CCFFFF","#99FFFF","#66FFFF","#33FFFF",
    "#00FFFF","#00CCCC","#99FFCC","#66FFCC","#33FFCC","#00FFCC","#33CCCC","#009999","#66CC99","#33CC99","#00CC99",
    "#339966","#009966","#006633","#66FF99","#33FF99","#00FF99","#33CC66","#00CC66","#009933","#99FF99","#66FF66",
    "#33FF66","#00FF66","#339933","#006600","#CCFFCC","#99CC99","#66CC66","#669966","#336633","#33FF33",
    "#00FF33","#00FF00","#00CC00","#33CC33","#00CC33","#66FF00","#66FF33","#33FF00","#33CC00","#339900","#009900",
    "#CCFF99","#99FF66","#66CC00","#66CC33","#669933","#336600","#99FF00","#99FF33","#99CC66","#99CC00","#99CC33",
    "#669900","#CCFF66","#CCFF00","#CCFF33","#CCCC99","#CCCC66","#CCCC33","#999933",
    "#999900"];

var isLight = true;
let show_icons_on_figures = false;
let infoCount = 0;
let scrolledDown = false;
let id=0;
function createFig(type,info) {
    if(audio_files == null) {
        return;
    }
    last_events_count++;

    let rand_array = rands(info);

    playSound(rand_array[4], $('#volinp').val()/100);

    let idl=id++;
    let br = 0;
    let rot = 0;
    if(type === 0){
        br = rand_array[2]/2;
    }
    else if(type === 1){
        rot = 45;
    }
    $("#id01").css('z-index',`${idl+2}`);
    $("#navbar").css('z-index',`${idl+1}`);
    if (show_icons_on_figures)
        $("#displaydiv").prepend(`<div id="back_figure" class="box" style="z-index: ${idl};width:${rand_array[2]}px;
            height:${rand_array[2]}px;border-radius:${br}px;left:${rand_array[0]}px;top:${rand_array[1]}px;
            transform: rotate(${rot}deg);"></div>
            <a href="${info["url"]}" target="_blank" id="${idl}" class="a_figure"  style="z-index: ${idl};width:${rand_array[2]}px;
            height:${rand_array[2]}px;border-radius:${br}px;left:${rand_array[0]}px;top:${rand_array[1]}px;
            transform: rotate(${rot}deg);background-color: ${colors[rand_array[3]]};opacity: 0.9;">
            <p id ="text_figure" style="transform: rotate(${-rot}deg); word-wrap: break-word;
             overflow: hidden;width:${rand_array[2]-10}px;
             max-height:${rand_array[2]-10}px " ><b><img src="../icons/${info['type']}.png" width="25px" height="25px"><br> ${info["repo"]}</b></p></a>`);
    else
        $("#displaydiv").prepend(`<div id="back_figure" class="box" style="z-index: ${idl};width:${rand_array[2]}px;
            height:${rand_array[2]}px;border-radius:${br}px;left:${rand_array[0]}px;top:${rand_array[1]}px;
            transform: rotate(${rot}deg);"></div>
            <a href="${info["url"]}" target="_blank" id="${idl}" class="a_figure"  style="z-index: ${idl};width:${rand_array[2]}px;
            height:${rand_array[2]}px;border-radius:${br}px;left:${rand_array[0]}px;top:${rand_array[1]}px;
            transform: rotate(${rot}deg);background-color: ${colors[rand_array[3]]};opacity: 0.9;">
            <p id ="text_figure" style="transform: rotate(${-rot}deg); word-wrap: break-word;
             overflow: hidden;width:${rand_array[2]-10}px;
             max-height:${rand_array[2]-10}px " ><b>${info["repo"]}</b></p></a>`);
    let animate_time_with_flag = animation_time;
    if(!animation_flag){
        animate_time_with_flag=0;
    }
    let color_obv=increase_brightness(colors[rand_array[3]],50);
    document.getElementById('text_figure').style.color = `${hexToComplimentary(color_obv)}`
    $(`#back_figure`).animate({
        "width": "+=50px",
        "margin-left": "-25px",
        "margin-top": "-25px",
        "border-radius": "+50px",
        "height": "+=50px",
        "opacity": "0"
    }, animate_time_with_flag);
    let id_to_remove = idl - max_count_of_figures;
    setTimeout(()=>{$("#displaydiv  div:last").remove();},animate_time_with_flag);
    $(`#${id_to_remove}`).animate({"opacity": "0"}, animate_time_with_flag);
    setTimeout(() => {
        $(`#${id_to_remove}`).remove()
    }, animate_time_with_flag);
}

function get_curr_category() {
    let select = document.getElementById("selectsound");
    return select.options[select.selectedIndex].value;
}

function rands(info){
    let length = info["repo"].length;
    if (length >= 17)
        length = 17;
    length /= Math.sqrt(2)*0.75;
    let audio_size = audio_files[get_curr_category()];
    let rands_array=[];
    rands_array.push(Math.floor(Math.random() * ($('#displaydiv').width() - 280)+100));
    rands_array.push(Math.floor(Math.random() * ($('#displaydiv').height() - 280)+100));
    rands_array.push(Math.floor(length*6/100 * (180 - 70 + 1)+70));
    rands_array.push(Math.floor(Math.random() * (colors.length)));
    rands_array.push(Math.floor(Math.random() * audio_size));
    return rands_array;
}

function add_event(type, jsinfo) {
    let date = new Date();
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    let day = date.getDate();
    let hours = date.getHours();
    let minutes = date.getMinutes();
    if (minutes < 10)
        minutes = '0' + minutes;
    let seconds = date.getSeconds();
    if (seconds < 10)
        seconds = '0' + seconds;
    let date_string = year + '-' + month + '-' + day + '  ' + hours + ':' + minutes + ':' + seconds + ' - ';
    $("#eventfield").append(`<div id="one_event" class="${id}" onmouseout="changeunhovercolor(${id});" onmousemove="changehovercolor(${id});"><img src="../icons/${jsinfo['type']}.png" width="25px" height="25px"> 
        ${date_string} <a href="${jsinfo["url"]}" 
    target="_blank">${jsinfo["owner"]} / ${jsinfo["repo"]}</div>`);
    if (scrolledDown)
        $("#eventfield").scrollTop($("#eventfield")[0].scrollHeight);
    createFig(type, jsinfo);
}

function infoonFig(info) {
    let type = Math.floor(Math.random() * (3));
   // $("#back_figure").remove();
   // alert(info +' '+ filter_flags);
    let jsinfo = JSON.parse(info);

    if(jsinfo['type'] === 'init') {
        audio_files = JSON.parse(jsinfo['categories']);
        for (let i in audio_files) {
            $('#selectsound').append(`<option class=\"optS\" value=\"${i}\">${i}</option>`);
        }
    }
    else if(jsinfo['type'] === 'error') {
        if(jsinfo['where'] === 'owner') {
            document.getElementById('organization').classList.add('error_filter_org');
        }
        else if (jsinfo['where'] === 'repo') {
            document.getElementById('repos').classList.add('error_filter_org');
        }
    }
    else if(filter_flags.indexOf(`${jsinfo['type']}`) > -1)  {
        if (infoCount <= 50) {
            infoCount++;
        } else {
            $("#one_event").remove();
        }

        add_event(type, jsinfo);
    }
}

let cached_sounds = {};
function playSound(index, volume) {
    let category = get_curr_category();
    let file = "audio/" + category + '/' + index + ".mp3";
    if(file in cached_sounds){
        cached_sounds[file].volume(volume);
        cached_sounds[file].play();
    }
    else{
        let a = new Howl({
            src: [file],
            volume: volume
        });
        a.play();
        cached_sounds[file] = a;
    }
}