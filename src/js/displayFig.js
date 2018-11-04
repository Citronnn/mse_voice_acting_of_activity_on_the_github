$(document).ready(function(){
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
    let isLight = true;

    let music=["A1","A3","A4","A5","A6","B0","B4","B8","C0","C3","C4","D8",
        "D9","E3","E7","F0","F6","F7","G4","G5","G7","G8"];
    let audio = [];
    for(let i=0;i<music.length;i++){
        audio.push(new Audio("audio/"+music[i]+".mp3"));
    }
    $('#changecolors').click(function () {
        if(isLight) {
            $('body').css('background-color','#292929');
            $('#displaydiv').css('background-color','#363535');
            $('#VA').css('color', '#ffffff');
            $('#IE').css('color', '#ffffff');
            $('#bar').css('color', '#ffffff');
            $('#changecolors').html("Go to Light");
            isLight = false;
        }
        else{
            $('body').css('background-color','white');
            $('#displaydiv').css('background-color', '#e8e8e7');
            $('#VA').css('color', '#000000');
            $('#IE').css('color', '#000000');
            $('#bar').css('color', '#000000');
            $('#changecolors').html("Go to Dark");
            isLight = true;
        }
    });

    setInterval(function(){
        if($(window).width()>$('#displaydiv').width())
            $('#displaydiv').css('min-width',$(window).width()*0.96);
        if($(window).height()>$('#displaydiv').height())
            $('#displaydiv').css('min-height',$(window).height()-55+'px');
    },0);

    setInterval(function () {
        $("#a_figure").animate({
            "opacity":"0"
        },1500);
    },0);


    setInterval(function(){
        let type = Math.floor(Math.random() * (3));
        $("#back_figure").remove();
        createFig(type);
    },1400);

    let next_m=Math.floor(Math.random() * (music.length));
    function createFig(type) {
        let rand_array = rands();
        audio[(next_m++) % music.length].play();
        let br = 0;
        let rot = 0;
        if(type === 0){
            br = rand_array[2]/2;
        }
        else if(type === 1){
            rot = 45;
        }
        $("#displaydiv").append(`<div id="back_figure" style="width:${rand_array[2]}px;
            height:${rand_array[2]}px;border-radius:${br}px;left:${rand_array[0]}px;top:${rand_array[1]}px;
            transform: rotate(${rot}deg);"></div>
            <a href="#" id="a_figure"><div id ="main_figure" style="width:${rand_array[2]}px;
            height:${rand_array[2]}px;border-radius:${br}px;left:${rand_array[0]}px;top:${rand_array[1]}px;
            transform: rotate(${rot}deg);background-color: ${colors[rand_array[3]]};opacity: 0.9;">
            <p id ="text_figure" style="transform: rotate(${-rot}deg)">kek</p></div></a>`);
        $("#back_figure").animate({
            "width": "+=50px",
            "margin-left":"-25px",
            "margin-top":"-25px",
            "border-radius":"+50px",
            "height":"+=50px",
            "opacity":"0"
        },1000);
        life_of_fig();
    }
    function life_of_fig() {
        setTimeout(delFig,27000);
    }
    function delFig() {
        $("#a_figure").remove();
    }

    function rands(){
        let rands_array=[];
        rands_array.push(Math.floor(Math.random() * ($('#displaydiv').width() - 250)+100));
        rands_array.push(Math.floor(Math.random() * ($('#displaydiv').height() - 250)+100));
        rands_array.push(Math.floor(Math.random() * (150 - 40 + 1)+40));
        rands_array.push(Math.floor(Math.random() * (colors.length)));

        return rands_array;
    }
});