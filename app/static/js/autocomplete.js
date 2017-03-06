/**
 * Created by raeste on 06.03.17.
 */
$(function () {
    $.post('/get-category').done(function (category) {
        $("#category").autocomplete({
            source: category['category']
        });
    })
});