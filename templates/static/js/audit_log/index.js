let xhr = new XMLHttpRequest();
xhr.open('GET', '/serback/get_all_audit_logs/');
xhr.onreadystatechange = () => {
    if (this.readyState == 4 && this.status == 200) {
        let res = JSON.parse(this.responseText);
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
        document.getElementById('main-content').innerHTML = txt;
    }
};
xhr.send();