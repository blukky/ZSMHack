jQuery(function () {
    // $('#hints_number').hide();
    // var tk = ['csrfmiddlewaretoken', $('input[type="hidden"]').val()];
    $('#id_number').keyup(function () {
        if ($(this).val().replace(/[_]/gi, '').length >= 2) {
            var data = {
                'csrfmiddlewaretoken': $('input[type="hidden"]').val(),
                'num': $(this).val().replace(/[_]/gi, '')
            };
            $.ajax({
                type: "POST",
                url: "filter/",
                data: data,
                success: function (data) {
                    // $('#hints_number').show();
                        if (document.getElementById('hints_number')){
                            $('#hints_number').remove();
                        }
                        let html = '<div class="list-group" style="z-index: 100; position: absolute" id="hints_number">';
                        for (var item in data) {
                            html += '<a href="#" class="list-group-item list-group-item-action" id="' + item + '">' + data[item] + '</a>';
                        }
                        ;
                        html += '</div>';
                        // console.log(html);
                        $('#id_number').after(html);
                        if (document.getElementById('hints_number')){
                            $('#hints_number a').click(function () {
                               var value = $(this).attr('id');
                               $('#id_number').val(value);
                               $('#hints_number').remove();
                            });
                        }
                }
            });
        } else {
            $('#hints_number').remove();
        }
    });

    $('#id_phone_number').keyup(function () {
        if ($(this).val().replace(/[_| |)|-]/gi, '').length >= 4) {
            console.log($(this).val());
            var data = {
                'csrfmiddlewaretoken': $('input[type="hidden"]').val(),
                'num': $(this).val().replace(/[_| |)|-]/gi, ''),
            };
            $.ajax({
                type: "POST",
                url: "filter_phone/",
                data: data,
                success: function (data) {
                    // $('#hints_number').show();
                        if (document.getElementById('hints_number_phone')){
                            $('#hints_number_phone').remove();
                        }
                        let html = '<div class="list-group" style="z-index: 100; position: absolute" id="hints_number_phone">';
                        for (var item in data) {
                            html += '<a href="#" class="list-group-item list-group-item-action" id="' + item + '">' + data[item] + '</a>';
                        }
                        ;
                        html += '</div>';
                        console.log(html);
                        $('#id_phone_number').after(html);
                        if (document.getElementById('hints_number_phone')){
                            $('#hints_number_phone a').click(function () {
                               var value = $(this).attr('id');
                               $('#id_phone_number').val(value);
                               $('#hints_number_phone').remove();
                            });
                        }
                }
            });
        } else {
            $('#hints_number_phone').remove();
        }
    });

});