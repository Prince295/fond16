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
        if (this.parentNode.id.split(/\s+/).length > 1) {
            var parentElemsToHide = document.getElementsByClassName(this.parentNode.id.split(/\s+/)[0] + 'parent');
        }
        else {
            var parentElemsToHide = new Array();
        }

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
              var items = document.getElementsByClassName('_numheader2');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
        };
        if (this.parentNode.id == 'all_cases') {
              var items = document.getElementsByClassName('_numheader3');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
              document.getElementById('amp_header').style.display = 'none';
              var items = document.getElementsByClassName('_numheader4');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
              document.getElementById('smp_header').style.display = 'none';
              var items = document.getElementsByClassName('_numheader5');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
              document.getElementById('statzam_header').style.display = 'none';
              var items = document.getElementsByClassName('_numheader6');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
              document.getElementById('smp_out_header').style.display = 'none';
        };
        if (this.parentNode.id == 'string_code_header') {
              document.getElementById('illness_header').colSpan = document.getElementById('illness_header').colSpan - 1;
              var items = document.getElementsByClassName('_numheader0');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
        };
        if (this.parentNode.id == 'nosologies_header') {
             document.getElementById('illness_header').colSpan = document.getElementById('illness_header').colSpan - 1;
             var items = document.getElementsByClassName('_numheader1');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
        };
        if (this.parentNode.id == 'amp_header') {
             var items = document.getElementsByClassName('_numheader3');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan - 1;

        };
        if (this.parentNode.id == 'smp_header') {
              var items = document.getElementsByClassName('_numheader4');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan - 1;
        };
        if (this.parentNode.id == 'statzam_header') {
              var items = document.getElementsByClassName('_numheader5');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan - 1;
        };
        if (this.parentNode.id == 'smp_out_header') {
              var items = document.getElementsByClassName('_numheader6');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'none';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan - 1;
        };
        var count_rows = 0;
        for (let i = 0, len = elemsToHide.length; i < len; i++)
         {
             if (elemsToHide[i].style.display != 'none') {
                count_rows ++;
             };
            elemsToHide[i].style.display = 'none';

            }

        for (let i = 0, len = parentElemsToHide.length; i < len; i++) {
            parentElemsToHide[i].rowSpan -= count_rows;
        };
        if (parentElemsToHide.length == 0) {
            var notHided = document.getElementsByClassName(this.parentNode.id+'child');
            if (notHided.length > 0) {
                for (let j = 0, len_0 = notHided.length; j < len_0; j++) {
                    notHided[j].style.display = 'none';
                };
            };
        }
    }
    else {
        $(this.firstChild).addClass('icon-circle-minus');
        $(this.firstChild).removeClass('icon-circle-plus');
        var elemsToDisplay = document.getElementsByClassName(this.parentNode.id);
        for (let i = 0, len = elemsToDisplay.length; i < len; i++){
          elemsToDisplay[i].style.display = 'table-row';

        };
        alert(elemsToDisplay.length);

        document.getElementById(this.parentNode.id.split(/\s+/)[0]).rowSpan +=elemsToDisplay.length;
        document.getElementById(this.parentNode.id.split(/\s+/)[0] + ' ' + this.parentNode.id.split(/\s+/)[1]).rowSpan +=elemsToDisplay.length;

    }
});

});


