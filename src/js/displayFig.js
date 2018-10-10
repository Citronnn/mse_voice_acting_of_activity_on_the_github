$(document).ready(function(){

    setInterval(function(){
        if($(window).height()>$('#displaydiv').height())
            $('#displaydiv').css('min-height',$(window).height()-20+'px');
        if($(window).width()>$('#displaydiv').width())
            $('#displaydiv').css('min-width',$(window).width()-20+'px');
    },0);

    setInterval(function () {
        $("#a_figure").fadeOut(2000, function(){ $(this).remove(); });
    },0);

    setInterval(function(){
        let type = Math.floor(Math.random() * (3));
        $("#back_figure").remove();
        createFig(type);
    },1400);

    function createFig(type) {
        let rand_array = rands();
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
            transform: rotate(${rot}deg);">
            <p id ="text_figure" style="transform: rotate(${-rot}deg)">kek</p></div></a>`);
        $("#back_figure").animate({
            "width": "+=50px",
            "margin-left":"-25px",
            "margin-top":"-25px",
            "border-radius":"+50px",
            "height":"+=50px",
            "opacity":"0"
        },1000);
    }

    function rands(){
        let rands_array=[];
        rands_array.push(Math.floor(Math.random() * ($('#displaydiv').width() - 370)+100));
        rands_array.push(Math.floor(Math.random() * ($('#displaydiv').height() - 370)+100));
        rands_array.push(Math.floor(Math.random() * (150 - 40 + 1)+40));
        return rands_array;
    }
});