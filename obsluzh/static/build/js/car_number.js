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

function getMobileOperatingSystem() {
    var userAgent = navigator.userAgent || navigator.vendor || window.opera;

    // Windows Phone must come first because its UA also contains "Android"
    // if (/windows phone/i.test(userAgent)) {
    //     return "Windows Phone";
    // }

    if (/android/i.test(userAgent)) {
        return "Android";
    }

    if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
        return "iOS";
    }

    return "unknown";
}

$(document).ready(function() {
    var phone = getMobileOperatingSystem();
    console.log(phone);
    if (phone === 'Android' || phone === 'unknown') {
        console.log('Вошел в андр');
        $("#id_phone_number").inputmask("+7(999) 999-9999");
        $("#id_number").inputmask("a999aa_9_");
    } else if (phone === 'iOS') {
        console.log('Вошел в айос');
        $("#id_phone_number").mask("+7(999) 999-9999", {autoclear: false});
        $("#id_number").mask("a999aa_9_", {autoclear: false});
    }
});

$("#msg").hide()
$("img").click(function () {
    var id = $(this).attr("id")
    console.log(id)
    if (id === 'ru') {
        console.log('Вошел в ру');
        $("#msg").hide()
        $("#" + id).addClass("shadow p-3 bg-white rounded");
        $("#by").removeClass("shadow p-3 bg-white rounded");
        $("#no").removeClass("shadow p-3 bg-white rounded");
        $('input#id_number').attr('placeholder', 'А000АА000');
        var phone = getMobileOperatingSystem();
        console.log(phone);
        if (phone === 'Android' || phone === 'unknown') {
            console.log('Вошел в андр');
            $("#id_phone_number").inputmask("+7(999) 999-9999");
            $("#id_number").inputmask("a999aa_9_");
        } else if (phone === 'iOS') {
            console.log('Вошел в айос');
            $("#id_phone_number").mask("+7(999) 999-9999", {autoclear: false});
            $("#id_number").mask("a999aa_9_", {autoclear: false});
        }
    }
    // if (id == 'by') {
    //     $("#msg").show()
    //     $("#" + id).addClass("shadow p-3 bg-white rounded");
    //     $("#ru").removeClass("shadow p-3 bg-white rounded");
    //     $("#no").removeClass("shadow p-3 bg-white rounded");
    //     $('input#id_number').attr('placeholder', '0000AA-00');
    // }
});
$('#no').click(function () {
    console.log('Вошел в ноу');
    $("#msg").hide()
    $(this).addClass("shadow p-3 bg-white rounded");
    $("#by").removeClass("shadow p-3 bg-white rounded");
    $("#ru").removeClass("shadow p-3 bg-white rounded");
    $('input#id_number').attr('placeholder', '');
    var phone = getMobileOperatingSystem();
    console.log(phone);
    if (phone === 'Android' || phone === 'unknown') {
        console.log('Вошел в андр');
        $("#id_number").inputmask("*********");
        $("#id_phone_number").inputmask("+7(999) 999-9999");
    } else if (phone === 'iOS') {
        console.log('Вошел в айос');
        $("#id_phone_number").mask("+7(999) 999-9999", {autoclear: false});
        $("#id_number").mask("*********", {autoclear: false});
    }
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
$("#id_phone_number").click(function () {
    var text = $(this).val();
    len = text.replace(/[_| |)|-]/gi, '');
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
$("#id_number").click(function () {
    var text = $(this).val();
    len = text.replace(/[_]/gi, '');
    var score = len.length;
    $(this).setCursorPosition(score);  // set position number
});