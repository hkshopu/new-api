$(function() {
    $.confirm({
        title: '確定寄出邀請信', 
        content: '確定要寄出邀請信嗎?', 
        buttons: {
            '取消': function() {}, 
            '確定': {
                action: function() {
                    $('#send-invitation-testing-mail-form').on('submit', function(e) {
                        e.preventDefault();
                        $.post('/user/send_invitation_testing_mail/', {email: $('textarea[name="email"]').val()}, function(res) {
                            alert(res.ret_val);
                        }, 'JSON');
                    });
                }
            }
        }
    });
});