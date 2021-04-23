jQuery(function(){
    $("#order #head").hide()
    $("#order #body tr").hide()
    var delta = []
//    $(".form-check-input").change(function(){
//        if ($(this).checked)
//            {
//                $("label").text("Выбор заказов за месяц")
//            }
//           else{
//                $("label").text("Выбор заказов за все время")
//           }
//
//    });
        $("#sort").click(function(){
            let start_price = 0;
            let end_price = 0;
            $("#order #head").hide();
            $("#order #body tr").hide();
           var start = $("#start").val();
           var end = $("#end").val();
           var start_date = new Date(start);
           var end_date = new Date(end);
           $("#order #head").show();
           $("#order #body tr").each(function(){
                var date = new Date($(this).attr("id"));
                var id = $(this).attr("class");
                if (date >= start_date && date <=end_date){
                    $(this).show();
                    $("#order #body #itogo").show();
                    // console.log($("."+id+" .start_price").text());
                    start_price += parseInt($("."+id+" .start_price").text());
                    end_price += parseInt($("."+id+" .end_price").text());
                }
           });
            $("#order #body #itogo #start").text(start_price);
            $("#order #body #itogo #end").text(end_price);
        });
//    $("#calen .den").click(function(){
//    if (delta.length == 2) {
//        for (let i=delta[0];i<=delta[1];i++){
//                var value = "#calen #"+i;
//                $(value).removeClass("bg-primary text-light").addClass("bg-light");
//            };
//        $("#order #head").hide()
//        $("#order #body tr").hide()
//        delta = []
//    }
//        delta.push(parseInt($(this).attr('name')));
//
//        $(this).removeClass("bg-light").addClass("bg-primary text-light");
//        if (delta.length == 2){
//            if (delta[0]>delta[1]){
//                delta = delta.reverse();
//            }
//            $("#order #head").show();
//            for (let i=delta[0];i<=delta[1];i++){
//                var value = "#calen #"+i;
//                $(value).removeClass("bg-light").addClass("bg-primary text-light");
//                var table = "#order #body #"+i
//                $(table).show();
//
//            };
//
//            }
//            });
    });