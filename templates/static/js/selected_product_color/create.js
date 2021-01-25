function create() {
    productColors = document.querySelectorAll('input[id^="product-color"]:checked');
    productColorArr = [];
    for (var i = 0; i < productColors.length; i++) {
        productColorArr.push(productColors[i].value);
    }

    $.ajax({
        url: '/selected_product_color/save/', 
        method: 'POST', 
        data: {
            product_id: $('#product-id').val(), 
            color_id: productColorArr
        }, 
        dataType: 'JSON', 
        success: function(res) {
            alert(res.ret_val);
        }
    });
}