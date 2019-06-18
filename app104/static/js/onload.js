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

        var newItem = document.createElement('a');
        newItem.id = this.parentNode.id +'hidden';
        document.getElementById('hiddenColumns').appendChild(newItem);
        newItem.style.display = 'block';
        newItem.addEventListener('click', function () {
            showElems(newItem)
        });
        newItem.href = '#';
        newItem.className = 'btn btn-success showelembtn';
        newItem.innerText = this.parentNode.innerText + '  (вернуть)';
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


        document.getElementById(this.parentNode.id.split(/\s+/)[0]).rowSpan +=elemsToDisplay.length - 1;
        document.getElementById(this.parentNode.id.split(/\s+/)[0] + ' ' + this.parentNode.id.split(/\s+/)[1]).rowSpan +=elemsToDisplay.length - 1;

    }
});

$('.hideelembtnnoz').click(function () {
    var _list = this.firstChild.className;
    var table = document.getElementById('table_illness');
    if ( _list.indexOf("icon-circle-minus") != -1 ) {
        $(this.firstChild).removeClass('icon-circle-minus');
        $(this.firstChild).addClass('icon-circle-plus');
        var elemsToDisplay = document.getElementsByClassName(this.parentNode.id);
        for (let i = 0, len = elemsToDisplay.length; i < len; i++){
          elemsToDisplay[i].style.display = 'none';
        };
        this.parentNode.parentNode.style.display = 'table-row';
        document.getElementById(this.parentNode.id.split(/\s+/)[0]).rowSpan -=elemsToDisplay.length - 1;
        document.getElementById(this.parentNode.id.split(/\s+/)[0] + ' ' + this.parentNode.id.split(/\s+/)[1]).rowSpan -=elemsToDisplay.length - 1;
    }
    else {
        $(this.firstChild).addClass('icon-circle-minus');
        $(this.firstChild).removeClass('icon-circle-plus');
        var elemsToDisplay = document.getElementsByClassName(this.parentNode.id);
        for (let i = 0, len = elemsToDisplay.length; i < len; i++){
          elemsToDisplay[i].style.display = 'table-row';
        };
        document.getElementById(this.parentNode.id.split(/\s+/)[0]).rowSpan +=elemsToDisplay.length - 1;
        document.getElementById(this.parentNode.id.split(/\s+/)[0] + ' ' + this.parentNode.id.split(/\s+/)[1]).rowSpan +=elemsToDisplay.length - 1;

    }
});
$('#colorDiff').change(function () {
        var tableElems = document.getElementById('table_illness').getElementsByTagName('td');
        if (this.checked) {
            for (let i = 0, len = tableElems.length; i < len; i++) {
                if (tableElems[i].innerText.endsWith('%')) {
                    var value = tableElems[i].innerText.split(/\s+/)[0];
                    if (value.startsWith('new')) {
                        tableElems[i].style.backgroundColor = '#e9432088';
                    }
                    if (value.startsWith('-')) {
                        if (Number(value) < -10) {
                            tableElems[i].style.backgroundColor = '#00ffa3';
                        }
                    }
                    else {
                        if (Number(value) > 10) {
                            tableElems[i].style.backgroundColor = '#e9432088';
                        }
                    }
                }
            }
        }
        else {
            for (let i = 0, len = tableElems.length; i < len; i++) {
                if (tableElems[i].innerText.endsWith('%')) {
                    var value = tableElems[i].innerText.split(/\s+/)[0];
                    if (value.startsWith('new')) {
                        tableElems[i].style.backgroundColor = 'transparent';
                    }
                    if (value.startsWith('-')) {
                        if (Number(value) < -10) {
                            tableElems[i].style.backgroundColor = 'transparent';
                        }
                    }
                    else {
                        if (Number(value) > 10) {
                            tableElems[i].style.backgroundColor = 'transparent';
                        }
                    }
                }
            }
        }
});
$('#coord_d_1').click(function () {
    var selected_mo = $("#mo_selection").val();
    var selected_smo = $("#smo_selection").val();
    var selected_year_1 = $("#select_year_1 option:selected").val();
    var selected_year_2 = $("#select_year_2 option:selected").val();
    var selected_month_1 = $("#select_month_1 option:selected").val();
    var selected_month_2 = $("#select_month_2 option:selected").val();
    this.href = '/coordination_illness/adult?selected_smo=' + selected_smo + '&selected_mo=' + selected_mo +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_2').click(function () {
    var selected_mo = $("#mo_selection").val();
    var selected_smo = $("#smo_selection").val();
    var selected_year_1 = $("#select_year_1 option:selected").val();
    var selected_year_2 = $("#select_year_2 option:selected").val();
    var selected_month_1 = $("#select_month_1 option:selected").val();
    var selected_month_2 = $("#select_month_2 option:selected").val();
    this.href = '/coordination_illness/pensioners?selected_smo=' + selected_smo + '&selected_mo=' + selected_mo +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_3').click(function () {
    var selected_mo = $("#mo_selection").val();
    var selected_smo = $("#smo_selection").val();
    var selected_year_1 = $("#select_year_1 option:selected").val();
    var selected_year_2 = $("#select_year_2 option:selected").val();
    var selected_month_1 = $("#select_month_1 option:selected").val();
    var selected_month_2 = $("#select_month_2 option:selected").val();
    this.href = '/coordination_illness/child?selected_smo=' + selected_smo + '&selected_mo=' + selected_mo +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_4').click(function () {
    var selected_mo = $("#mo_selection").val();
    var selected_smo = $("#smo_selection").val();
    var selected_year_1 = $("#select_year_1 option:selected").val();
    var selected_year_2 = $("#select_year_2 option:selected").val();
    var selected_month_1 = $("#select_month_1 option:selected").val();
    var selected_month_2 = $("#select_month_2 option:selected").val();
    this.href = '/coordination_illness/babies?selected_smo=' + selected_smo + '&selected_mo=' + selected_mo +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_5').click(function () {
    var selected_mo = $("#mo_selection").val();
    var selected_smo = $("#smo_selection").val();
    var selected_year_1 = $("#select_year_1 option:selected").val();
    var selected_year_2 = $("#select_year_2 option:selected").val();
    var selected_month_1 = $("#select_month_1 option:selected").val();
    var selected_month_2 = $("#select_month_2 option:selected").val();
    this.href = '/coordination_illness/all?selected_smo=' + selected_smo + '&selected_mo=' + selected_mo +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('.showelembtn').click(function () {
    this.style.display = 'none';
    var _cutId = this.id.split('hidden')[0];
    var table = document.getElementById('table_illness');
    var elemsToHide = document.getElementsByClassName(_cutId);
        if (_cutId.split(/\s+/).length > 1) {
            var parentElemsToShow = document.getElementsByClassName(_cutId.split(/\s+/)[0] + 'parent');
        }
        else {
            var parentElemsToShow = new Array();
        }

        if (_cutId == 'smo_header') {

           var items = document.getElementsByClassName('numheader0');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              }
        };
        if (_cutId == 'mo_header') {
              var items = document.getElementsByClassName('numheader1');

              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              }
        };
        if (_cutId == 'illness_header') {

              document.getElementById('string_code_header').style.display = 'table-cell';
              document.getElementById('nosologies_header').style.display = 'table-cell';
              var items = document.getElementsByClassName('_numheader0');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              var items = document.getElementsByClassName('_numheader1');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
        };
        if (_cutId == 'mkb_header') {
              var items = document.getElementsByClassName('_numheader2');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
        };
        if (_cutId == 'all_cases') {
              var items = document.getElementsByClassName('_numheader3');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('amp_header').style.display = 'table-cell';
              var items = document.getElementsByClassName('_numheader4');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('smp_header').style.display = 'table-cell';
              var items = document.getElementsByClassName('_numheader5');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('statzam_header').style.display = 'table-cell';
              var items = document.getElementsByClassName('_numheader6');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('smp_out_header').style.display = 'table-cell';
        };
        if (_cutId == 'string_code_header') {
              document.getElementById('illness_header').colSpan = document.getElementById('illness_header').colSpan - 1;
              var items = document.getElementsByClassName('_numheader0');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
        };
        if (_cutId == 'nosologies_header') {
             document.getElementById('illness_header').colSpan = document.getElementById('illness_header').colSpan - 1;
             var items = document.getElementsByClassName('_numheader1');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
        };
        if (_cutId == 'amp_header') {
             var items = document.getElementsByClassName('_numheader3');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan - 1;

        };
        if (_cutId == 'smp_header') {
              var items = document.getElementsByClassName('_numheader4');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan - 1;
        };
        if (_cutId == 'statzam_header') {
              var items = document.getElementsByClassName('_numheader5');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan - 1;
        };
        if (_cutId == 'smp_out_header') {
              var items = document.getElementsByClassName('_numheader6');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan - 1;
        };
        var count_rows = 0;
        for (let i = 0, len = elemsToHide.length; i < len; i++)
         {
             if (elemsToHide[i].style.display != 'table-cell') {
                count_rows ++;
             };
            elemsToHide[i].style.display = 'table-cell';

            }

        for (let i = 0, len = parentElemsToHide.length; i < len; i++) {
            parentElemsToHide[i].rowSpan -= count_rows;
        };
        if (parentElemsToHide.length == 0) {
            var notHided = document.getElementsByClassName(_cutId+'child');
            if (notHided.length > 0) {
                for (let j = 0, len_0 = notHided.length; j < len_0; j++) {
                    notHided[j].style.display = 'table-cell';
                };
            };
        }

    });


});
function showElems(editedItem) {
    editedItem.style.display = 'none';
    var _cutId = editedItem.id.split('hidden')[0];
    var table = document.getElementById('table_illness');
    var elemsToHide = document.getElementsByClassName(_cutId);
    if (document.getElementById(_cutId).tagName == 'TR') {
        document.getElementById(_cutId).style.display = 'table-row';
    }
    else {
        document.getElementById(_cutId).style.display = 'table-cell';
    }


        if (_cutId.split(/\s+/).length > 1) {
            var parentElemsToShow = document.getElementsByClassName(_cutId.split(/\s+/)[0] + 'parent');
        }
        else {
            var parentElemsToShow = new Array();
        }

        if (_cutId == 'smo_header') {

           var items = document.getElementsByClassName('numheader0');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById(_cutId).rowSpan = 2;
        };
        if (_cutId == 'mo_header') {
              var items = document.getElementsByClassName('numheader1');

              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              }
        };
        if (_cutId == 'illness_header') {
              document.getElementById('string_code_header').style.display = 'table-cell';
              document.getElementById('nosologies_header').style.display = 'table-cell';
              var items = document.getElementsByClassName('_numheader0');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              var items = document.getElementsByClassName('_numheader1');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
        };
        if (_cutId == 'mkb_header') {
              var items = document.getElementsByClassName('_numheader2');
              document.getElementById(_cutId).rowSpan = 2;
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
        };
        if (_cutId == 'all_cases') {
              var items = document.getElementsByClassName('_numheader3');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('amp_header').style.display = 'table-cell';
              var items = document.getElementsByClassName('_numheader4');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('smp_header').style.display = 'table-cell';
              var items = document.getElementsByClassName('_numheader5');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('statzam_header').style.display = 'table-cell';
              var items = document.getElementsByClassName('_numheader6');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('smp_out_header').style.display = 'table-cell';
        };
        if (_cutId == 'string_code_header') {
              document.getElementById('illness_header').colSpan = document.getElementById('illness_header').colSpan - 1;
              var items = document.getElementsByClassName('_numheader0');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
        };
        if (_cutId == 'nosologies_header') {
             document.getElementById('illness_header').colSpan = document.getElementById('illness_header').colSpan - 1;
             var items = document.getElementsByClassName('_numheader1');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
        };
        if (_cutId == 'amp_header') {
             var items = document.getElementsByClassName('_numheader3');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan - 1;

        };
        if (_cutId == 'smp_header') {
              var items = document.getElementsByClassName('_numheader4');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan - 1;
        };
        if (_cutId == 'statzam_header') {
              var items = document.getElementsByClassName('_numheader5');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan - 1;
        };
        if (_cutId == 'smp_out_header') {
              var items = document.getElementsByClassName('_numheader6');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan - 1;
        };
        var count_rows = 0;
        for (let i = 0, len = elemsToHide.length; i < len; i++)
         {
             if (elemsToHide[i].tagName == 'TR') {
                elemsToHide[i].style.display = 'table-row';
             }
             else {
                 elemsToHide[i].style.display = 'table-cell';
             }

            };
        count_rows = hideRows(editedItem, elemsToHide);

        var parentTableRow = document.getElementById(_cutId+'rowsmo');

        if (!parentTableRow){

        }
        else {
            document.getElementById(_cutId+'rowsmo').style.display = 'table-row';
        }
        if (count_rows != 0) {
            document.getElementById(_cutId).rowSpan = count_rows + 1;
        }
        for (let i = 0, len = parentElemsToShow.length; i < len; i++) {
            parentElemsToShow[i].rowSpan += count_rows;
        };
        var count_childs = 0;
        if (parentElemsToShow.length == 0) {
            var hided = document.getElementsByClassName(_cutId+'child');
            if (hided.length > 0) {
                for (let j = 0, len_0 = hided.length; j < len_0; j++) {
                    hided[j].style.display = 'table-cell';
                    count_childs +=1;
                };
                document.getElementById(_cutId).rowSpan = count_rows + count_childs;
            };
        }
        editedItem.remove();
        var hiddenCols = document.getElementById('hiddenColumns').childNodes;
        for (let i = 0, len = hiddenCols.length; i < len; i++) {
            try {

                if (hiddenCols[i].style.display == 'block') {
                    var hidden_col_id = hiddenCols[i].id.split('hidden')[0];
                    if (hidden_col_id == 'smo_header') {

                        var items = document.getElementsByClassName('numheader0');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }
                    ;
                    if (hidden_col_id == 'mo_header') {
                        var items = document.getElementsByClassName('numheader1');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                    }
                    ;
                    if (hidden_col_id == 'illness_header') {

                        var items = document.getElementsByClassName('_numheader0');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                        var items = document.getElementsByClassName('_numheader1');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }
                    ;
                    if (hidden_col_id == 'mkb_header') {
                        var items = document.getElementsByClassName('_numheader2');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }
                    ;
                    if (hidden_col_id == 'all_cases') {
                        var items = document.getElementsByClassName('_numheader3');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                        var items = document.getElementsByClassName('_numheader4');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                        var items = document.getElementsByClassName('_numheader5');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                        var items = document.getElementsByClassName('_numheader6');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }
                    ;
                    if (hidden_col_id == 'string_code_header') {
                        var items = document.getElementsByClassName('_numheader0');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }
                    ;
                    if (hidden_col_id == 'nosologies_header') {
                        var items = document.getElementsByClassName('_numheader1');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }
                    ;
                    if (hidden_col_id == 'amp_header') {
                        var items = document.getElementsByClassName('_numheader3');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;

                    }
                    ;
                    if (hidden_col_id == 'smp_header') {
                        var items = document.getElementsByClassName('_numheader4');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }
                    ;
                    if (hidden_col_id == 'statzam_header') {
                        var items = document.getElementsByClassName('_numheader5');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }
                    ;
                    if (hidden_col_id == 'smp_out_header') {
                        var items = document.getElementsByClassName('_numheader6');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }
                    ;
                }
            }
            catch {

            };
        }




}
function hideRows(editedElem, elemsToShow) {
    var count_rows = 0;
    for (let i = 0,len = elemsToShow.length; i < len; i++) {
        if (elemsToShow[i].cells[0].innerText.length <= 2) {
            elemsToShow[i].style.display = 'table-row';
            count_rows += 1;
        }
        else {
            elemsToShow[i].style.display = 'none';
        }
    }
    return count_rows;
}
