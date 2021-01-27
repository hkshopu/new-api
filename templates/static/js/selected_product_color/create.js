function create() {
    var xhr = new XMLHttpRequest();
    var productId = document.getElementById('product_id');
    var productColors = document.querySelectorAll('input[name="color_id"]:checked');
    var sendDataStr = '';

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var resText = JSON.parse(this.responseText);
            alert(resText.ret_val);
            if (resText.status == 0) {
                location.reload();
            }
        }
    };
    xhr.open('POST', '/selected_product_color/save/');
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    sendDataStr += 'product_id=' + productId.value;
    for (var i = 0; i < productColors.length; i++) {
        sendDataStr += '&color_id=' + productColors[i].value;
    }
    xhr.send(sendDataStr);
}