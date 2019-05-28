function onClickLoadForm() {
    var form = document.getElementById('form_load');
    var formData = new FormData();
    var xhr = new XMLHttpRequest();
    var token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    formData.append('data', form);
    formData.append('csrfmiddlewaretoken', token);
    xhr.open('POST', '#', false);
    xhr.send(formData);

};
function showDoc() {
    var doc = document.getElementById('table1');
    doc.hidden = false;

}