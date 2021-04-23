jQuery(function () {

    $('#status').hide();
    $('#div_country h5').hide();
    $('#country').hide();
    $('.country').each(function (){
        $(this).hide();
    });


    $('#select_region').change(function () {
        $('#region h5').text('Вы выбрали');
        var value = $('input').val();
        var data = {
            'csrfmiddlewaretoken': value,
            'region': $(this).val()
        }
        $.ajax({
            url: 'region/',
            type: 'POST',
            data: data,
            success: function (data) {
                var size = Object.keys(data).length;
                if (size == 1){
                    var findpos = 'найден';
                    var pos = 'поселок';
                }
                else if (size == 2 || size == 3 || size == 4)
                {
                    var findpos = 'найдено';
                    var pos = 'поселка';
                }
                else
                    {
                    var findpos = 'найдено ';
                    var pos = ' поселков';
                }
                    $('#div_country h5').text('В данном регионе '+ findpos+ size + pos);
                if (size != 0 ) {
                    $('#country').show();
                    $('#div_country h5').show();
                    Object.keys(data).forEach(function (key) {
                        $('.country').each(function () {
                            if ($(this).val() == data[key]) {
                                $(this).show();
                            }
                        });

                    });
                    $('#country').change(function () {
                        $('#status').show();
                    });
                }else{
                    var text = $('#div_country h5').text();
                    $('#div_country h5').text(text +' Выберите соседние регионы');
                }
            }
        });
    });
});