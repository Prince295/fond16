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

$(document).ready(function(){
$(".auth").click(function () {
$("#auth_form").addClass("form--active");

});
$(".cancel-auth").click(function () {
$("#auth_form").removeClass("form--active");
});
$(".logout").click(function () {
$.ajax({url: '/fond16/logout/'}).done( function () {
 location.reload();
});
});
$('.hideelembtn').click(function(){
    var _list = this.firstChild.className;
    var table = document.getElementById('table_illness');
    if ( _list.indexOf("icon-circle-minus") != -1 ){
        $(this.firstChild).removeClass('icon-circle-minus');
        $(this.firstChild).addClass('icon-circle-plus');
        this.parentNode.style.display = 'none';
        var elemsToHide = document.getElementsByClassName(this.parentNode.id);
        if (this.parentNode.id == 'smo_header') {

           var items = document.getElementsByClassName('numheader0');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              }
        };
        if (this.parentNode.id == 'mo_header') {
              var items = document.getElementsByClassName('numheader1');

              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              }
        };
        if (this.parentNode.id == 'illness_header') {

              document.getElementById('string_code_header').style.display = 'none';
              document.getElementById('nosologies_header').style.display = 'none';
              var items = document.getElementsByClassName('_numheader0');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
              var items = document.getElementsByClassName('_numheader1');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
        };
        if (this.parentNode.id == 'mkb_header') {
              var index_delete = this.parentNode.cellIndex;
              var table_rows = table.rows;
              for ( let i = 0, len=table_rows.length; i < len; i++) {
                  table_rows[i].cells[index_delete].style.display = 'none';

                }
        };
        if (this.parentNode.id == 'all_header') {
              var index_delete = this.parentNode.cellIndex;
              var table_rows = table.rows;
              for ( let i = 0, len=table_rows.length; i < len; i++) {
                  table_rows[i].cells[index_delete].style.display = 'none';
                  table_rows[i].cells[index_delete + 1].style.display = 'none';
                  table_rows[i].cells[index_delete + 2].style.display = 'none';
                  table_rows[i].cells[index_delete + 3].style.display = 'none';
                }
        };
        if (this.parentNode.id == 'string_code_header') {
              var index_delete = this.parentNode.cellIndex;
              var table_rows = table.rows;
              for ( let i = 0, len=table_rows.length; i < len; i++) {
                  table_rows[i].cells[index_delete].style.display = 'none';

                }
        };
        if (this.parentNode.id == 'nosologies_header') {
              var index_delete = this.parentNode.cellIndex;
              var table_rows = table.rows;
              for ( let i = 0, len=table_rows.length; i < len; i++) {
                  table_rows[i].cells[index_delete].style.display = 'none';

                }
        };
        if (this.parentNode.id == 'amp_header') {
              var index_delete = this.parentNode.cellIndex;
              var table_rows = table.rows;
              for ( let i = 0, len=table_rows.length; i < len; i++) {
                  table_rows[i].cells[index_delete].style.display = 'none';

                }
        };
        if (this.parentNode.id == 'smp_header') {
              var index_delete = this.parentNode.cellIndex;
              var table_rows = table.rows;
              for ( let i = 0, len=table_rows.length; i < len; i++) {
                  table_rows[i].cells[index_delete].style.display = 'none';

                }
        };
        if (this.parentNode.id == 'statzam_header') {
              var index_delete = this.parentNode.cellIndex;
              var table_rows = table.rows;
              for ( let i = 0, len=table_rows.length; i < len; i++) {
                  table_rows[i].cells[index_delete].style.display = 'none';

                }
        };
        if (this.parentNode.id == 'smp_out_header') {
              var index_delete = this.parentNode.cellIndex;
              var table_rows = table.rows;
              for ( let i = 0, len=table_rows.length; i < len; i++) {
                  table_rows[i].cells[index_delete].style.display = 'none';

                }
        };
        for (let i = 0, len = elemsToHide.length; i < len; i++)
         {
            elemsToHide[i].style.display = 'none';
            if (i == 0 ) {
                var curRow = table.rows;
                table.rows[elemsToHide[i].rowIndex - 1].cells[0].rowSpan = table.rows[elemsToHide[i].rowIndex - 1].cells[0].rowSpan - table.rows[elemsToHide[i].rowIndex - 1].cells[1].rowSpan + 1;
            };
         };
    }
    else {
        $(this.firstChild).addClass('icon-circle-minus');
        $(this.firstChild).removeClass('icon-circle-plus');
        this.parentNode.style.display = 'block';
    }
});

});


