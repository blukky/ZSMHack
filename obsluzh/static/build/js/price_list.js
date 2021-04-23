jQuery(function () {
    let header = $("#header");
    header.hide();
    const width = $('#vid_vid').width();
    $('#vid').css({'width':width});
    let height = $("#header_vid").offset()['top'];
    $(window).scroll(function () {
        let ScrollPos = $(this).scrollTop();
        const widthTable = $('table').innerWidth();
        const width = $('#vid_vid').innerWidth();
        $('#vid').css({'width':width});
        header.css({'width':widthTable});
        if (ScrollPos>=height){
            header.show();

        }
        else{
            header.hide();
        }
    });
});