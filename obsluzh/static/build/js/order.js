jQuery(function(){
console.log($("#id_phone_number").val());
   function clear(){

   $("table tbody td h5").each(function(){
            $(this).hide();
        });
   $('table tbody td input[type="text"]').each(function(){
            $(this).remove();
        });

   }

   function validnos(){

   if ($("#id_number").val() == '' || ($("#predvar_price").text() == '0' && $("#fakt_price").text() == '0' ) || $("#id_phone_number").val() == '' ){
       $("#submit").addClass("disabled");
       $("#submit").attr('disabled', 'disabled');
   }
   else {
       $("#submit").removeClass("disabled");
       $("#submit").removeAttr("disabled");
   }


   if ($("#id_number").val() == ''){
       $("#id_phone_number").addClass('disabled');
       $("#id_phone_number").attr('disabled', 'disabled');

       $("#id_car").addClass('disabled');
       $("#id_car").attr('disabled', 'disabled');

       $('input[type="checkbox"]').addClass('disabled');
       $('input[type="checkbox"]').attr('disabled', 'disabled');

       $("#id_status").addClass('disabled');
       $("#id_status").attr('disabled', 'disabled');

       $("#id_comment").addClass('disabled');
       $("#id_comment").attr('disabled', 'disabled');
   }
   else{
       $("#id_phone_number").removeClass("disabled");
       $("#id_phone_number").removeAttr("disabled");
   }
   if ($("#id_phone_number").val() === ''){
       $("#id_car").addClass('disabled');
       $("#id_car").attr('disabled', 'disabled');
       $('input[type="checkbox"]').addClass('disabled');
       $('input[type="checkbox"]').attr('disabled', 'disabled');
   }
   else{
       $("#id_car").removeClass("disabled");
       $("#id_car").removeAttr("disabled");
       $('input[type="checkbox"]').removeClass('disabled');
       $('input[type="checkbox"]').removeAttr('disabled');
       $("#id_status").removeClass('disabled');
       $("#id_status").removeAttr('disabled', 'disabled');
       $("#id_comment").removeClass('disabled');
       $("#id_comment").removeAttr('disabled', 'disabled');
   }

   }



   function set_price() {
        let start_price = 0;
        let end_price = 0;
        $("input:checkbox:checked").each(function(){
            var key = $(this).attr('name');
            key = key.split('_');
            if (key[key.length - 1] == 'start'){
                key.pop();
                if (key.length > 1){
                    key = key.join('_');
                }
                else{
                    key = key[0];
                }
                var id = $("#id_car").val();
                var perem = "h5#"+key+"."+id;
                if ($(perem).data('value') == "Д/ц"){
                    if ($(perem).text() != "Д/ц"){
                        var value = $(perem).text();
                        start_price += parseInt(value);
                    }
                }
                else{
                start_price += $(perem).data('value');
                }
            }
            else{
                key.pop();
                if (key.length > 1){
                    key = key.join('_');
                }
                else{
                    key = key[0];
                }
                var id = $("#id_car").val();
                var perem = "h5#"+key+"."+id;
                if ($(perem).data('value') == "Д/ц"){
                    if ($(perem).text() != "Д/ц"){
                        var value = $(perem).text();
                        end_price += parseInt(value);
                    }
                }
                else{
                end_price += $(perem).data('value');
                }
            }
        });
        $("#predvar_price").text(start_price);
        $("#fakt_price").text(end_price);
        validnos()
   }

   function set_price_servise() {
        var value = $("#id_car").val();
        // console.log(value);
        if (value != ""){
            var coin = "."+value;
            $(coin).each(function(){
                $(this).show();
                var dc = $(this).data('value');
                dc = String(dc).split("_")[0];
                if (dc == "Д/ц"){
                        if ($(this).text() != "Д/ц"){
                            var price = $(this).text()
                        }
                        else{ var price = "0"; }
                    var id = $(this).attr('id');
                    var clas = $(this).attr('class');
                    $(this).after('<input type="text" id="'+id+'" class="'+clas+'" name="dogprice_'+id+'_'+clas+'" >');
                    $(this).hide();
                    $('table tbody td input[name="dogprice_'+id+'_'+clas+'" ]').val(price);
                }
            });
            $('table tbody td input[type="text"]').keyup(function(){
                        var value = $(this).val();
                        var id1 = $(this).attr('id');
                        var clas1 = $(this).attr('class');
                        if (value == ""){ $('table tbody td h5#'+id1+'.'+clas1).text("0");}
                        else{
                        $('table tbody td h5#'+id1+'.'+clas1).text(value);
                        }
                        set_price();
                        validnos()
                        });
        };
        set_price();
   }

   $('input[type="checkbox"]').click(function(){
        set_price()
       validnos()
        });
    $("#id_phone_number").change(function () {
       validnos()
   })
    $("#id_number").change(function () {
       validnos()
   })
//   $('table tbody td input[type="text"]').keyup(function(){
//                        var id = $(this).attr('id')
//                        var clas = $(this).attr('class')
//                        var value = $(this).val();
//                        $('table tbody td h5#'+id+'.'+clas).text(value);
//                        set_price()
//                           });


   clear()
   set_price_servise()
   set_price()
    validnos()
   $("#id_car").change(function(){
        clear()
        var value = $(this).val();
        if (value != ""){
            var coin = "h5."+value;
            $(coin).each(function(){
                $(this).show()
                var dc = $(this).data('value')
                if (dc == "Д/ц"){
                    if ($(this).text() != "Д/ц") {var price = $(this).text()} else {var price = "0"}
                    var id = $(this).attr('id')
                    var clas = $(this).attr('class')
                    $(this).after('<input type="text" id="'+id+'" class="'+clas+'" name="dogprice_'+id+'_'+clas+'" >')
                    $(this).hide()
                    $('table tbody td input[name="dogprice_'+id+'_'+clas+'" ]').val(price)
                   }
            });
            $('table tbody td input[type="text"]').keyup(function(){
                        var value = $(this).val();
                        var id1 = $(this).attr('id')
                        var clas1 = $(this).attr('class')
                        if (value == ""){ $('table tbody td h5#'+id1+'.'+clas1).text("0");}
                        else{
                        $('table tbody td h5#'+id1+'.'+clas1).text(value);
                        }
                        set_price()
                        validnos()
            });
        }
        set_price()
       validnos()
   });


});