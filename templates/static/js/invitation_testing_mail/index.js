$(function() {
    var confirm = confirm('確定要寄出邀請信嗎?');
    if (confirm) {
        $('#send-invitation-testing-mail-form').on('submit', function(e) {
            e.preventDefault();
            $.post('/user/send_invitation_testing_mail/', {email: $('textarea[name="email"]').val()}, function(res) {
                alert(res.ret_val);
            }, 'JSON');
        });
    }
});