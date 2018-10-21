$(document).ready(function(){
    let colors=[];
    let colors_white=[];
    let colors_black=[];

    $('#changecolors').click(function () {
        if( $('body').css('background-color') == 'rgb(255, 255, 255)') {
            $('body').css('background-color', '#292929');
            $('#displaydiv').css('background-color', '#363535');
        }
        else{
            $('body').css('background-color','white');
            $('#displaydiv').css('background-color', '#e8e8e7');
        }
    });
    setInterval(function(){
        if($(window).height()>$('#displaydiv').height())
            $('#displaydiv').css('min-height',$(window).height()-55+'px');
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
            transform: rotate(${rot}deg);background-color: ${colors[rand_array[3]]};">
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
        rands_array.push(Math.floor(Math.random() * ($('#displaydiv').width() - 250)+100));
        rands_array.push(Math.floor(Math.random() * ($('#displaydiv').height() - 250)+100));
        rands_array.push(Math.floor(Math.random() * (150 - 40 + 1)+40));
        rands_array.push(Math.floor(Math.random() * (50)));
        return rands_array;
    }
});