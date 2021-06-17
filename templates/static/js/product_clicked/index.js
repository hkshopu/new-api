$(function() {
    $.ajax({
        url: '/serback/get_all_product_clicked/', 
        method: 'GET', 
        dataType: 'JSON', 
        success: function(res) {
            var txt = '';
            txt += '<table class="table table-striped">';
            txt += '<thead>';
            txt += '<tr>';
            txt += '<th>id</th><th>shop_id</th><th>user_id</th><th>created_at</th><th>updated_at</th>';
            txt += '<tbody>';
            if (res.status == 0) {
                for (var i in res.data) {
                    txt += '<tr>';
                    txt += '<td>' + res.data[i].id + '</td>';
                    txt += '<td>' + res.data[i].product_id + '</td>';
                    txt += '<td>' + res.data[i].user_id + '</td>';
                    txt += '<td>' + res.data[i].created_at + '</td>';
                    txt += '<td>' + res.data[i].updated_at + '</td>';
                    txt += '</tr>';
                }
            }

            if (res.status == -1) {
                txt += '<tr>';
                txt += '<td colspan="5">' + res.ret_val + '</td>';
                txt += '</tr>';
            }
            txt += '</tbody>';
            txt += '</thead>';
            txt += '</table>';
            $('#main-content').html(txt);
        }
    });
});