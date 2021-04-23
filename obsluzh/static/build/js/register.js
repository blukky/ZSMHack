Inputmask.extendDefinitions({
    'a': {
        "validator": "[а|в|е|к|м|н|о|р|с|т|у|х|А|В|Е|К|М|Н|О|Р|С|Т|У|Х]"
    },
    '_': {
        "validator": "[ |0-9]"
    },
    '*': {
        "validator": "[A-Z|a-z|0-9|А-Я|а-я| |-]",
    },
});
$.mask.definitions['a'] = "[а|в|е|к|м|н|о|р|с|т|у|х|А|В|Е|К|М|Н|О|Р|С|Т|У|Х]";
$.mask.definitions['_'] = "[ |0-9]";
$.mask.definitions['*'] = "[A-Z|a-z|0-9|А-Я|а-я| |-]";

$(document).ready(function() {
    $("#id_phone").inputmask("+7(999) 999-99-99");
});


$.fn.setCursorPosition = function (pos) {
    if ($(this).get(0).setSelectionRange) {
        $(this).get(0).setSelectionRange(pos, pos);
    } else if ($(this).get(0).createTextRange) {
        var range = $(this).get(0).createTextRange();
        range.collapse(true);
        range.moveEnd('character', pos);
        range.moveStart('character', pos);
        range.select();
    }
};
$("#id_phone").click(function () {
    var text = $(this).val();
    var len = text.replace(/[_| |)|-]/gi, '');
    var score = len.length;
    if (score > 5) {
        len = text.replace(/[_|-]/gi, '');
        score = len.length;
    }
    if (score > 8) {
        len = text.replace(/[_]/gi, '');
        score = len.length;
    }
    $(this).setCursorPosition(score);  // set position number
});

$('#id_password2').change(function () {
   if ($(this).val() == $('#id_password1').val()){

   }
});