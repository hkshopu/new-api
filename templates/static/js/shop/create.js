$('#create-form').on('submit', function(e) {
    e.preventDefault();
    $.ajax({
        url: '/shop/save/', 
        method: 'POST', 
        data: new FormData(this), 
        cache: false, 
        contentType: false, 
        processData: false, 
        dataType: 'JSON', 
        success: function(res) {
            alert(res.ret_val);
            if (res.status == 0) {
                location.reload();
            }
        }
    });
});