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
    $("#id_phone").inputmask("+7(999) 999-9999");
});