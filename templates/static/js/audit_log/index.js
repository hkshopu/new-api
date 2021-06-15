$.ajax({
    url: '/serback/get_all_audit_logs/', 
    method: 'GET', 
    dataType: 'JSON', 
    success: function(res) {
        let txt = '<table>';
        txt += '<thead>';
        txt += '<tr>';
        txt += '<th>id</th><th>user_id</th><th>action</th><th>parameter_in</th><th>parameter_out</th><th>created_at</th><th>updated_at</th>';
        txt += '</tr>';
        txt += '</thead>';
        txt += '<tbody>';
        if (res.status == 0) {
            for (let i in res.data) {
                txt += '<tr>';
                txt += '<td>' + res.data[i].id + '</td>';
                txt += '<td>' + res.data[i].user_id + '</td>';
                txt += '<td>' + res.data[i].action + '</td>';
                txt += '<td>' + res.data[i].parameter_in + '</td>';
                txt += '<td>' + res.data[i].parameter_out + '</td>';
                txt += '<td>' + res.data[i].created_at + '</td>';
                txt += '<td>' + res.data[i].updated_at + '</td>';
                txt += '</tr>';
            }
        }
        
        if (res.status == -1) {
            txt += '<tr>';
            txt += '<td colspan="7">' + res.ret_val + '</td>';
            txt += '</tr>';
        }
        txt += '</tbody>';
        txt += '</table>';
        $('#main-content').html(txt);
    }
});