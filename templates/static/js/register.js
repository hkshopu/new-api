function register() {
    $.ajax({
        url: '/user/registerProcess/', 
        method: 'POST', 
        data: {
            account_name: $('#account-name').val(), 
            email: $('#email').val(), 
            password: $('#password').val(), 
            confirm_password: $('#confirm-password').val(), 
            first_name: $('#first-name').val(), 
            last_name: $('#last-name').val(), 
            phone: $('#phone').val(), 
            gender: $('#gender').val(), 
            birthday: $('#birthday').val(), 
            address: $('#address').val()
        }, 
        dataType: 'JSON', 
        success: function(res) {
            alert(res.ret_val);
            if (res.status == 0) {
                location.reload();
            }
        }
    });
}