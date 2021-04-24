jQuery(function () {

    function filter() {
        var reg = $('#select_region').val();
    var cat = $('#cat').val();
    var who = $('#who').val();
    var min_price = parseInt($('#min_price').val());
    var max_price = parseInt($('#max_price').val());
    $('div.prod').each(function () {
        if ($(this).data('value') == who && $(this).data('action') == reg && $(this).data('parent') == cat && parseInt($(this).data('dismiss')) >= min_price && parseInt($(this).data('dismiss')) <= max_price){
            $(this).show();
        }
        else{
            $(this).hide();
        }
    });
    };
    filter();
    $('#select_region').change(function () {
        filter();
    });
    $('#cat').change(function () {
        filter();
    });
    $('#who').change(function () {
        filter();
    });
    $('#min_price').change(function () {
        filter();
    });
    $('#max_price').change(function () {
        filter();
    });
});