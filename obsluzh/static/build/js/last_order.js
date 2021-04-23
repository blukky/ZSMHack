jQuery(function(){

    function clear(){
        $("table tbody td h5").each(function(){
            $(this).hide();
            });
        }

        function set_price() {
        let start_price = 0
        let end_price = 0
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
                var id = $("#id_car").data('value');
                var perem = "h5#"+key+"."+id;
                if ($(perem).data('value') == "Д/ц"){
                    if ($(perem).text() != "Д/ц"){
                        var value = $(perem).text()
                        start_price += parseInt(value)
                    }
                }
                else{
                start_price += $(perem).data('value')
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
                var id = $("#id_car").data('value');
                var perem = "h5#"+key+"."+id;
                if ($(perem).data('value') == "Д/ц"){
                    if ($(perem).text() != "Д/ц"){
                        var value = $(perem).text()
                        end_price += parseInt(value)
                    }
                }
                else{
                end_price += $(perem).data('value')
                }
            }
        });
        $("#predvar_price").text(start_price);
        $("#fakt_price").text(end_price);
   }

        function set_price_servise() {
        var value = $("#id_car").data('value')
        if (value != ""){
            var coin = "."+value;
            $(coin).each(function(){
                $(this).show()
                });
                }
                }
    clear()
    set_price_servise()
    set_price()

    $('input[type="checkbox"]').click(function(){
        set_price()
        });

});