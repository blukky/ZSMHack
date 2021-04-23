jQuery(function () {
    $('#select_region').change(function () {
        $('#region h5').text('Вы выбрали');

        $.ajax({
            url: 'region/',
            type: 'POST',
            data: {'region': $(this).val()},
            success: function (data) {
                var size = Object.keys(myObj).length;

                Object.keys(data).forEach(function (key){

                });
            }
        });
    });
});