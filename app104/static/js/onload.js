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

                  $(items[i]).hide('fast');

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
            $(elemsToHide[i]).hide('fast');

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
        $(this.firstChild).removeClass('icon-circle-plus');
        $(this.firstChild).addClass('icon-circle-minus');

        var elemsToDisplay = document.getElementsByClassName(this.parentNode.id);
        for (let i = 0, len = elemsToDisplay.length; i < len; i++){
          $(elemsToDisplay[i]).slideDown(300);
        };
        document.getElementById(this.parentNode.id.split(/\s+/)[0]).rowSpan +=elemsToDisplay.length - 1;
        document.getElementById(this.parentNode.id.split(/\s+/)[0] + ' ' + this.parentNode.id.split(/\s+/)[1]).rowSpan +=elemsToDisplay.length - 1;

    }
});

$('#colorDiff').change(function () {
        var tableElems = document.getElementById('table_illness').getElementsByTagName('td');
        if (this.checked) {
            for (let i = 0, len = tableElems.length; i < len; i++) {
                let values = tableElems[i].getElementsByTagName('span')

                if (values.length >= 2) {
                    if (Number(values[1].innerText) != 0) {
                        let res = (Number(values[0].innerText) - Number(values[1].innerText)) / Number(values[1].innerText)
                        if (res > 0.1) {
                            tableElems[i].style.backgroundColor = '#e9432088';
                        }
                        if (res < -0.1) {
                            tableElems[i].style.backgroundColor = '#00ffa3';
                        }
                    }
                    else {
                        if (Number(values[0].innerText != 0)) {
                            tableElems[i].style.backgroundColor = '#e9432088';
                        }

                    }
                }
            }
        }
        else {
            for (let i = 0, len = tableElems.length; i < len; i++) {
                let values = tableElems[i].getElementsByTagName('span')

                if (values.length >= 2) {
                    if (Number(values[1].innerText) != 0) {
                        let res = (Number(values[0].innerText) - Number(values[1].innerText)) / Number(values[1].innerText)
                        if (res > 0.1) {
                            tableElems[i].style.backgroundColor = 'transparent';
                        }
                        if (res < -0.1) {
                            tableElems[i].style.backgroundColor = 'transparent';
                        }
                    }
                    else {
                        if (Number(values[0].innerText != 0)) {
                            tableElems[i].style.backgroundColor = 'transparent';
                        }

                    }
                }
            }
        }
        // if (this.checked) {
        //     for (let i = 0, len = tableElems.length; i < len; i++) {
        //         if (tableElems[i].innerText.endsWith('%')) {
        //             var value = tableElems[i].innerText.split(/\s+/)[0];
        //             if (value.startsWith('new')) {
        //                 tableElems[i].style.backgroundColor = '#e9432088';
        //             }
        //             if (value.startsWith('-')) {
        //                 if (Number(value) < -10) {
        //                     tableElems[i].style.backgroundColor = '#00ffa3';
        //                 }
        //             }
        //             else {
        //                 if (Number(value) > 10) {
        //                     tableElems[i].style.backgroundColor = '#e9432088';
        //                 }
        //             }
        //         }
        //     }
        // }
        // else {
        //     for (let i = 0, len = tableElems.length; i < len; i++) {
        //         if (tableElems[i].innerText.endsWith('%')) {
        //             var value = tableElems[i].innerText.split(/\s+/)[0];
        //             if (value.startsWith('new')) {
        //                 tableElems[i].style.backgroundColor = 'transparent';
        //             }
        //             if (value.startsWith('-')) {
        //                 if (Number(value) < -10) {
        //                     tableElems[i].style.backgroundColor = 'transparent';
        //                 }
        //             }
        //             else {
        //                 if (Number(value) > 10) {
        //                     tableElems[i].style.backgroundColor = 'transparent';
        //                 }
        //             }
        //         }
        //     }
        // }
});
$('#coord_d_1').click(function () {
    let smo_to_server_checked = document.getElementsByClassName('checked_smo');
    let smo_to_server = '';
    for( let i = 0, len=smo_to_server_checked.length; i < len; i++) {
        if (i != (smo_to_server_checked.length - 1)) {
            smo_to_server += String(smo_to_server_checked[i].value) + ','
        }
        else {
            smo_to_server += String(smo_to_server_checked[i].value)
        }
    };
    let mo_to_server_checked = document.getElementsByClassName('checked_mo');
    let mo_to_server = '';
    for( let i = 0, len=mo_to_server_checked.length; i < len; i++) {
        if (i != (mo_to_server_checked.length - 1)) {
            mo_to_server += String(mo_to_server_checked[i].value) + ','
        }
        else {
            mo_to_server += String(mo_to_server_checked[i].value)
        }
    };
    var selected_year_1 = convertYear(document.getElementById('select_year_1').querySelector('.chosen-value').value);
    var selected_year_2 = convertYear(document.getElementById('select_year_2').querySelector('.chosen-value').value);
    var selected_month_1 = convertMonth(document.getElementById('select_month_1').querySelector('.chosen-value').value);
    var selected_month_2 = convertMonth(document.getElementById('select_month_2').querySelector('.chosen-value').value);
    this.href = '/coordination_illness/adult?selected_smo=' + smo_to_server + '&selected_mo=' + mo_to_server +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_2').click(function () {
    let smo_to_server_checked = document.getElementsByClassName('checked_smo');
    let smo_to_server = '';
    for( let i = 0, len=smo_to_server_checked.length; i < len; i++) {
        if (i != (smo_to_server_checked.length - 1)) {
            smo_to_server += String(smo_to_server_checked[i].value) + ','
        }
        else {
            smo_to_server += String(smo_to_server_checked[i].value)
        }
    };
    let mo_to_server_checked = document.getElementsByClassName('checked_mo');
    let mo_to_server = '';
    for( let i = 0, len=mo_to_server_checked.length; i < len; i++) {
        if (i != (mo_to_server_checked.length - 1)) {
            mo_to_server += String(mo_to_server_checked[i].value) + ','
        }
        else {
            mo_to_server += String(mo_to_server_checked[i].value)
        }
    };
    var selected_year_1 = convertYear(document.getElementById('select_year_1').querySelector('.chosen-value').value);
    var selected_year_2 = convertYear(document.getElementById('select_year_2').querySelector('.chosen-value').value);
    var selected_month_1 = convertMonth(document.getElementById('select_month_1').querySelector('.chosen-value').value);
    var selected_month_2 = convertMonth(document.getElementById('select_month_2').querySelector('.chosen-value').value);
    this.href = '/coordination_illness/pensioners?selected_smo=' + smo_to_server + '&selected_mo=' + mo_to_server +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_3').click(function () {
    let smo_to_server_checked = document.getElementsByClassName('checked_smo');
    let smo_to_server = '';
    for( let i = 0, len=smo_to_server_checked.length; i < len; i++) {
        if (i != (smo_to_server_checked.length - 1)) {
            smo_to_server += String(smo_to_server_checked[i].value) + ','
        }
        else {
            smo_to_server += String(smo_to_server_checked[i].value)
        }
    };
    let mo_to_server_checked = document.getElementsByClassName('checked_mo');
    let mo_to_server = '';
    for( let i = 0, len=mo_to_server_checked.length; i < len; i++) {
        if (i != (mo_to_server_checked.length - 1)) {
            mo_to_server += String(mo_to_server_checked[i].value) + ','
        }
        else {
            mo_to_server += String(mo_to_server_checked[i].value)
        }
    };
    var selected_year_1 = convertYear(document.getElementById('select_year_1').querySelector('.chosen-value').value);
    var selected_year_2 = convertYear(document.getElementById('select_year_2').querySelector('.chosen-value').value);
    var selected_month_1 = convertMonth(document.getElementById('select_month_1').querySelector('.chosen-value').value);
    var selected_month_2 = convertMonth(document.getElementById('select_month_2').querySelector('.chosen-value').value);
    this.href = '/coordination_illness/babies?selected_smo=' + smo_to_server + '&selected_mo=' + mo_to_server +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_4').click(function () {
    let smo_to_server_checked = document.getElementsByClassName('checked_smo');
    let smo_to_server = '';
    for( let i = 0, len=smo_to_server_checked.length; i < len; i++) {
        if (i != (smo_to_server_checked.length - 1)) {
            smo_to_server += String(smo_to_server_checked[i].value) + ','
        }
        else {
            smo_to_server += String(smo_to_server_checked[i].value)
        }
    };
    let mo_to_server_checked = document.getElementsByClassName('checked_mo');
    let mo_to_server = '';
    for( let i = 0, len=mo_to_server_checked.length; i < len; i++) {
        if (i != (mo_to_server_checked.length - 1)) {
            mo_to_server += String(mo_to_server_checked[i].value) + ','
        }
        else {
            mo_to_server += String(mo_to_server_checked[i].value)
        }
    };
    var selected_year_1 = convertYear(document.getElementById('select_year_1').querySelector('.chosen-value').value);
    var selected_year_2 = convertYear(document.getElementById('select_year_2').querySelector('.chosen-value').value);
    var selected_month_1 = convertMonth(document.getElementById('select_month_1').querySelector('.chosen-value').value);
    var selected_month_2 = convertMonth(document.getElementById('select_month_2').querySelector('.chosen-value').value);
    this.href = '/coordination_illness/child?selected_smo=' + smo_to_server + '&selected_mo=' + mo_to_server +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_5').click(function () {
    let smo_to_server_checked = document.getElementsByClassName('checked_smo');
    let smo_to_server = '';
    for( let i = 0, len=smo_to_server_checked.length; i < len; i++) {
        if (i != (smo_to_server_checked.length - 1)) {
            smo_to_server += String(smo_to_server_checked[i].value) + ','
        }
        else {
            smo_to_server += String(smo_to_server_checked[i].value)
        }
    };
    let mo_to_server_checked = document.getElementsByClassName('checked_mo');
    let mo_to_server = '';
    for( let i = 0, len=mo_to_server_checked.length; i < len; i++) {
        if (i != (mo_to_server_checked.length - 1)) {
            mo_to_server += String(mo_to_server_checked[i].value) + ','
        }
        else {
            mo_to_server += String(mo_to_server_checked[i].value)
        }
    };
    var selected_year_1 = convertYear(document.getElementById('select_year_1').querySelector('.chosen-value').value);
    var selected_year_2 = convertYear(document.getElementById('select_year_2').querySelector('.chosen-value').value);
    var selected_month_1 = convertMonth(document.getElementById('select_month_1').querySelector('.chosen-value').value);
    var selected_month_2 = convertMonth(document.getElementById('select_month_2').querySelector('.chosen-value').value);
    this.href = '/coordination_illness/all?selected_smo=' + smo_to_server + '&selected_mo=' + mo_to_server +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});

$('#coord_d_6').click(function () {
    let smo_to_server_checked = document.getElementsByClassName('checked_smo');
    let smo_to_server = '';
    for( let i = 0, len=smo_to_server_checked.length; i < len; i++) {
        if (i != (smo_to_server_checked.length - 1)) {
            smo_to_server += String(smo_to_server_checked[i].value) + ','
        }
        else {
            smo_to_server += String(smo_to_server_checked[i].value)
        }
    };
    let mo_to_server_checked = document.getElementsByClassName('checked_mo');
    let mo_to_server = '';
    for( let i = 0, len=mo_to_server_checked.length; i < len; i++) {
        if (i != (mo_to_server_checked.length - 1)) {
            mo_to_server += String(mo_to_server_checked[i].value) + ','
        }
        else {
            mo_to_server += String(mo_to_server_checked[i].value)
        }
    };
    var selected_year_1 = convertYear(document.getElementById('select_year_1').querySelector('.chosen-value').value);
    var selected_year_2 = convertYear(document.getElementById('select_year_2').querySelector('.chosen-value').value);
    var selected_month_1 = convertMonth(document.getElementById('select_month_1').querySelector('.chosen-value').value);
    var selected_month_2 = convertMonth(document.getElementById('select_month_2').querySelector('.chosen-value').value);
    this.href = '/coordination_death/adult?selected_smo=' + smo_to_server + '&selected_mo=' + mo_to_server +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_7').click(function () {
    let smo_to_server_checked = document.getElementsByClassName('checked_smo');
    let smo_to_server = '';
    for( let i = 0, len=smo_to_server_checked.length; i < len; i++) {
        if (i != (smo_to_server_checked.length - 1)) {
            smo_to_server += String(smo_to_server_checked[i].value) + ','
        }
        else {
            smo_to_server += String(smo_to_server_checked[i].value)
        }
    };
    let mo_to_server_checked = document.getElementsByClassName('checked_mo');
    let mo_to_server = '';
    for( let i = 0, len=mo_to_server_checked.length; i < len; i++) {
        if (i != (mo_to_server_checked.length - 1)) {
            mo_to_server += String(mo_to_server_checked[i].value) + ','
        }
        else {
            mo_to_server += String(mo_to_server_checked[i].value)
        }
    };
    var selected_year_1 = convertYear(document.getElementById('select_year_1').querySelector('.chosen-value').value);
    var selected_year_2 = convertYear(document.getElementById('select_year_2').querySelector('.chosen-value').value);
    var selected_month_1 = convertMonth(document.getElementById('select_month_1').querySelector('.chosen-value').value);
    var selected_month_2 = convertMonth(document.getElementById('select_month_2').querySelector('.chosen-value').value);
    this.href = '/coordination_death/pensioners?selected_smo=' + smo_to_server + '&selected_mo=' + mo_to_server +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_8').click(function () {
    let smo_to_server_checked = document.getElementsByClassName('checked_smo');
    let smo_to_server = '';
    for( let i = 0, len=smo_to_server_checked.length; i < len; i++) {
        if (i != (smo_to_server_checked.length - 1)) {
            smo_to_server += String(smo_to_server_checked[i].value) + ','
        }
        else {
            smo_to_server += String(smo_to_server_checked[i].value)
        }
    };
    let mo_to_server_checked = document.getElementsByClassName('checked_mo');
    let mo_to_server = '';
    for( let i = 0, len=mo_to_server_checked.length; i < len; i++) {
        if (i != (mo_to_server_checked.length - 1)) {
            mo_to_server += String(mo_to_server_checked[i].value) + ','
        }
        else {
            mo_to_server += String(mo_to_server_checked[i].value)
        }
    };
    var selected_year_1 = convertYear(document.getElementById('select_year_1').querySelector('.chosen-value').value);
    var selected_year_2 = convertYear(document.getElementById('select_year_2').querySelector('.chosen-value').value);
    var selected_month_1 = convertMonth(document.getElementById('select_month_1').querySelector('.chosen-value').value);
    var selected_month_2 = convertMonth(document.getElementById('select_month_2').querySelector('.chosen-value').value);
    this.href = '/coordination_death/babies?selected_smo=' + smo_to_server + '&selected_mo=' + mo_to_server +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_9').click(function () {
    let smo_to_server_checked = document.getElementsByClassName('checked_smo');
    let smo_to_server = '';
    for( let i = 0, len=smo_to_server_checked.length; i < len; i++) {
        if (i != (smo_to_server_checked.length - 1)) {
            smo_to_server += String(smo_to_server_checked[i].value) + ','
        }
        else {
            smo_to_server += String(smo_to_server_checked[i].value)
        }
    };
    let mo_to_server_checked = document.getElementsByClassName('checked_mo');
    let mo_to_server = '';
    for( let i = 0, len=mo_to_server_checked.length; i < len; i++) {
        if (i != (mo_to_server_checked.length - 1)) {
            mo_to_server += String(mo_to_server_checked[i].value) + ','
        }
        else {
            mo_to_server += String(mo_to_server_checked[i].value)
        }
    };
    var selected_year_1 = convertYear(document.getElementById('select_year_1').querySelector('.chosen-value').value);
    var selected_year_2 = convertYear(document.getElementById('select_year_2').querySelector('.chosen-value').value);
    var selected_month_1 = convertMonth(document.getElementById('select_month_1').querySelector('.chosen-value').value);
    var selected_month_2 = convertMonth(document.getElementById('select_month_2').querySelector('.chosen-value').value);
    this.href = '/coordination_death/child?selected_smo=' + smo_to_server + '&selected_mo=' + mo_to_server +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_10').click(function () {
    let smo_to_server_checked = document.getElementsByClassName('checked_smo');
    let smo_to_server = '';
    for( let i = 0, len=smo_to_server_checked.length; i < len; i++) {
        if (i != (smo_to_server_checked.length - 1)) {
            smo_to_server += String(smo_to_server_checked[i].value) + ','
        }
        else {
            smo_to_server += String(smo_to_server_checked[i].value)
        }
    };
    let mo_to_server_checked = document.getElementsByClassName('checked_mo');
    let mo_to_server = '';
    for( let i = 0, len=mo_to_server_checked.length; i < len; i++) {
        if (i != (mo_to_server_checked.length - 1)) {
            mo_to_server += String(mo_to_server_checked[i].value) + ','
        }
        else {
            mo_to_server += String(mo_to_server_checked[i].value)
        }
    };
    var selected_year_1 = convertYear(document.getElementById('select_year_1').querySelector('.chosen-value').value);
    var selected_year_2 = convertYear(document.getElementById('select_year_2').querySelector('.chosen-value').value);
    var selected_month_1 = convertMonth(document.getElementById('select_month_1').querySelector('.chosen-value').value);
    var selected_month_2 = convertMonth(document.getElementById('select_month_2').querySelector('.chosen-value').value);
    this.href = '/coordination_death/all?selected_smo=' + smo_to_server + '&selected_mo=' + mo_to_server +
    '&selected_year_1=' + selected_year_1 + '&selected_month_1=' + selected_month_1 +
    '&selected_year_2=' + selected_year_2 + '&selected_month_2=' + selected_month_2;
});
$('#coord_d_runner').click(function () {
    let smo_to_server = '';

    let mo_to_server = '';

    var selected_year_1 = convertYear(document.getElementById('select_year_1').querySelector('.chosen-value').value);
    var selected_year_2 = selected_year_1
    var selected_month_1 = convertMonth(document.getElementById('select_month_1').querySelector('.chosen-value').value);
    var selected_month_2 = convertMonth(String(Number(selected_month_1) - 1));
    this.href = '/coordination_illness_rebase?selected_smo=' + smo_to_server + '&selected_mo=' + mo_to_server +
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
$(document).on('click','.btngetclasses', function () {
    var _list = this.firstChild.className;
    if ( _list.indexOf("icon-circle-plus") != -1 ) {
        var params = window
            .location
            .search
            .replace('?', '')
            .split('&')
            .reduce(
                function (p, e) {
                    var a = e.split('=');
                    p[decodeURIComponent(a[0])] = decodeURIComponent(a[1]);
                    return p;
                },
                {}
            );
        let parent_id = this.parentNode.parentNode.id;
        let parent = this.parentNode.parentNode;
        let j = 1;
        parent_id = parent_id.split(' ');
        $.get('/return_classnames',
            {
                mo: parent_id[1],
                smo: parent_id[0],
                month: params['selected_month_1'],
                year: params['selected_year_1']
            },
            function (data) {
                $.each(data, function (key, value) {
                    var row_index = parent.rowIndex;
                    var newRow = document.getElementById('table_illness').insertRow(row_index + j);
                    var smo = document.getElementById(parent_id[0])
                    var mo = document.getElementById(parent_id[0] + ' ' + parent_id[1])
                    var newCell = newRow.insertCell(0);
                    newCell.innerText = key;
                    $(newRow).addClass(parent_id[0]);
                    $(newRow).addClass(parent_id[1]);
                    $(newRow).addClass(parent_id[2]);

                    newCell = newRow.insertCell(1);
                    let newDiv = document.createElement('div');
                    let newSecondDiv = document.createElement('div');
                    $(newCell).addClass('diagonal-line');
                    $(newCell).addClass('amp_header');
                    let first_child = document.createElement('span');
                    first_child.innerText = value[0];
                    let second_child = document.createElement('span');
                    second_child.innerText = value[4];
                    newDiv.appendChild(first_child);
                    newSecondDiv.appendChild(second_child);
                    newCell.appendChild(newDiv);
                    newCell.appendChild(newSecondDiv);

                    newCell = newRow.insertCell(2);
                    newDiv = document.createElement('div');
                    newSecondDiv = document.createElement('div');
                    $(newCell).addClass('diagonal-line');
                    $(newCell).addClass('smp_header');
                    first_child = document.createElement('span');
                    first_child.innerText = value[1];
                    second_child = document.createElement('span');
                    second_child.innerText = value[5];
                    newDiv.appendChild(first_child);
                    newSecondDiv.appendChild(second_child);
                    newCell.appendChild(newDiv);
                    newCell.appendChild(newSecondDiv);

                    newCell = newRow.insertCell(3);
                    newDiv = document.createElement('div');
                    newSecondDiv = document.createElement('div');
                    $(newCell).addClass('diagonal-line');
                    $(newCell).addClass('statzam_header');
                    first_child = document.createElement('span');
                    first_child.innerText = value[2];
                    second_child = document.createElement('span');
                    second_child.innerText = value[6];
                    newDiv.appendChild(first_child);
                    newSecondDiv.appendChild(second_child);
                    newCell.appendChild(newDiv);
                    newCell.appendChild(newSecondDiv);

                    newCell = newRow.insertCell(4);
                    newDiv = document.createElement('div');
                    newSecondDiv = document.createElement('div');
                    $(newCell).addClass('diagonal-line');
                    $(newCell).addClass('skormp_header');
                    first_child = document.createElement('span');
                    first_child.innerText = value[3];
                    second_child = document.createElement('span');
                    second_child.innerText = value[7];
                    newDiv.appendChild(first_child);
                    newSecondDiv.appendChild(second_child);
                    newCell.appendChild(newDiv);
                    newCell.appendChild(newSecondDiv);

                    newCell = newRow.insertCell(5);
                    newDiv = document.createElement('div');
                    newSecondDiv = document.createElement('div');
                    $(newCell).addClass('diagonal-line');
                    $(newCell).addClass('amp_header_second');
                    first_child = document.createElement('span');
                    first_child.innerText = value[0];
                    second_child = document.createElement('span');
                    second_child.innerText = value[8];
                    newDiv.appendChild(first_child);
                    newSecondDiv.appendChild(second_child);
                    newCell.appendChild(newDiv);
                    newCell.appendChild(newSecondDiv);

                    newCell = newRow.insertCell(6);
                    newDiv = document.createElement('div');
                    newSecondDiv = document.createElement('div');
                    $(newCell).addClass('diagonal-line');
                    $(newCell).addClass('smp_header_second');
                    first_child = document.createElement('span');
                    first_child.innerText = value[1];
                    second_child = document.createElement('span');
                    second_child.innerText = value[9];
                    newDiv.appendChild(first_child);
                    newSecondDiv.appendChild(second_child);
                    newCell.appendChild(newDiv);
                    newCell.appendChild(newSecondDiv);

                    newCell = newRow.insertCell(7);
                    newDiv = document.createElement('div');
                    newSecondDiv = document.createElement('div');
                    $(newCell).addClass('diagonal-line');
                    $(newCell).addClass('statzam_header_second');
                    first_child = document.createElement('span');
                    first_child.innerText = value[2];
                    second_child = document.createElement('span');
                    second_child.innerText = value[10];
                    newDiv.appendChild(first_child);
                    newSecondDiv.appendChild(second_child);
                    newCell.appendChild(newDiv);
                    newCell.appendChild(newSecondDiv);

                    newCell = newRow.insertCell(8);
                    newDiv = document.createElement('div');
                    newSecondDiv = document.createElement('div');
                    $(newCell).addClass('diagonal-line');
                    $(newCell).addClass('skormp_header_second');
                    first_child = document.createElement('span');
                    first_child.innerText = value[3];
                    second_child = document.createElement('span');
                    second_child.innerText = value[11];
                    newDiv.appendChild(first_child);
                    newSecondDiv.appendChild(second_child);
                    newCell.appendChild(newDiv);
                    newCell.appendChild(newSecondDiv);

                    smo.rowSpan++;
                    mo.rowSpan++;
                    j++;
                });
            },
            'json');
        $(this.firstChild).addClass('icon-circle-minus');
        $(this.firstChild).removeClass('icon-circle-plus');
    }
    else {
        var items_to_remove_list = document.getElementsByClassName(this.parentNode.parentNode.id);
        var parent_id = this.parentNode.parentNode.id.split(' ');
        var smo = document.getElementById(parent_id[0])
        var mo = document.getElementById(parent_id[0] + ' ' + parent_id[1])
        let items_length = items_to_remove_list.length;
        let _table = document.getElementById('table_illness');
        for ( let i = 0; i < items_length; i++) {
            _table.deleteRow(this.parentNode.parentNode.rowIndex + 1);
            smo.rowSpan--;
            mo.rowSpan--;
        };
        $(this.firstChild).addClass('icon-circle-plus');
        $(this.firstChild).removeClass('icon-circle-minus');

    };

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
              if (!document.getElementById('string_codeheaderhidden')) {
                  document.getElementById('string_code_header').style.display = 'table-cell';
              };
              if (!document.getElementById('nosologies_headerhidden')) {
                  document.getElementById('nosologies_header').style.display = 'table-cell';
              };
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
              if (!document.getElementById('amp_headerhidden')) {
                  document.getElementById('amp_header').style.display = 'table-cell';
              };
              var items = document.getElementsByClassName('_numheader4');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              if (!document.getElementById('smp_headerhidden')) {
                  document.getElementById('smp_header').style.display = 'table-cell';
              };
              var items = document.getElementsByClassName('_numheader5');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              if (!document.getElementById('statzam_headerhidden')) {
                  document.getElementById('statzam_header').style.display = 'table-cell';
              };
              var items = document.getElementsByClassName('_numheader6');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              if (!document.getElementById('smp_out_headerhidden')) {
                  document.getElementById('smp_out_header').style.display = 'table-cell';
              };
        };
        if (_cutId == 'string_code_header') {
              document.getElementById('illness_header').colSpan = document.getElementById('illness_header').colSpan + 1;
              var items = document.getElementsByClassName('_numheader0');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
        };
        if (_cutId == 'nosologies_header') {
             document.getElementById('illness_header').colSpan = document.getElementById('illness_header').colSpan + 1;
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
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan + 1;

        };
        if (_cutId == 'smp_header') {
              var items = document.getElementsByClassName('_numheader4');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan + 1;
        };
        if (_cutId == 'statzam_header') {
              var items = document.getElementsByClassName('_numheader5');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan + 1;
        };
        if (_cutId == 'smp_out_header') {
              var items = document.getElementsByClassName('_numheader6');
              for ( let i = 0, len=items.length; i < len; i++) {
                  items[i].style.display = 'table-cell';
              };
              document.getElementById('all_cases').colSpan = document.getElementById('all_cases').colSpan + 1;
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
                    hided[j].rowSpan = count_rows / hided.length + 1;
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
                        document.getElementById(hidden_col_id).style.display = 'none';
                        var items = document.getElementsByClassName('numheader0');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }

                    else if (hidden_col_id == 'mo_header') {
                        document.getElementById(hidden_col_id).style.display = 'none';
                        var items = document.getElementsByClassName('numheader1');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                    }

                    else if (hidden_col_id == 'illness_header') {
                        document.getElementById(hidden_col_id).style.display = 'none';
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

                    else if (hidden_col_id == 'mkb_header') {
                        document.getElementById(hidden_col_id).style.display = 'none';
                        var items = document.getElementsByClassName('_numheader2');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }

                    else if (hidden_col_id == 'all_cases') {
                        document.getElementById(hidden_col_id).style.display = 'none';
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

                    else if (hidden_col_id == 'string_code_header') {
                        document.getElementById(hidden_col_id).style.display = 'none';
                        var items = document.getElementsByClassName('_numheader0');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }

                    else if (hidden_col_id == 'nosologies_header') {
                        document.getElementById(hidden_col_id).style.display = 'none';
                        var items = document.getElementsByClassName('_numheader1');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }

                    else if (hidden_col_id == 'amp_header') {
                        document.getElementById(hidden_col_id).style.display = 'none';
                        var items = document.getElementsByClassName('_numheader3');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;

                    }

                    else if (hidden_col_id == 'smp_header') {
                        document.getElementById(hidden_col_id).style.display = 'none';
                        var items = document.getElementsByClassName('_numheader4');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }

                    else if (hidden_col_id == 'statzam_header') {
                        document.getElementById(hidden_col_id).style.display = 'none';
                        var items = document.getElementsByClassName('_numheader5');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }

                    else if (hidden_col_id == 'smp_out_header') {
                        document.getElementById(hidden_col_id).style.display = 'none';
                        var items = document.getElementsByClassName('_numheader6');
                        for (let i = 0, len = items.length; i < len; i++) {
                            items[i].style.display = 'none';
                        }
                        ;
                    }
                    else {
                        if (!document.getElementById(hidden_col_id)){

                        }
                        else {
                            if (document.getElementById(hidden_col_id).classList.contains('numheader1')) {
                                document.getElementById(hidden_col_id).style.display = 'none';

                                let array_of_hidden_children = document.getElementsByClassName(hidden_col_id);
                                for (let i = 0, len = array_of_hidden_children.length; i < len; i++) {
                                    if (array_of_hidden_children[i].style.display == 'table-row') {
                                        document.getElementById(hidden_col_id.split(' ')[0]).rowSpan -= 1;
                                        array_of_hidden_children[i].style.display = 'none';
                                    }
                                }
                            }
                        }
                    }
                }
            }
            catch {

            };
        }




}
function hideRows(editedElem, elemsToShow) {
    var count_rows = 0;

    for (let i = 0,len = elemsToShow.length; i < len; i++) {
        if (!elemsToShow[i].cells) {
            if ((elemsToShow[i].tagName == 'th') | (elemsToShow[i].tagName == 'td')) {
                elemsToShow[i].style.display = 'table-cell'
            }
        }
        else {
            if (elemsToShow[i].cells[0].innerText.length <= 2) {
                elemsToShow[i].style.display = 'table-row';
                count_rows += 1;
                var need_to_change_icon = elemsToShow[i].getElementsByClassName('icon-circle-minus');
                if (!need_to_change_icon) {
                }
                else {

                    $(need_to_change_icon[0]).addClass('icon-circle-plus');
                    $(need_to_change_icon[0]).removeClass('icon-circle-minus');
                }

            }
            else {
                elemsToShow[i].style.display = 'none';
            }
        }
    }
    return count_rows;
}

function convertMonth(month) {
    let month_array = {
        'Январь' : '1',
        'Февраль' : '2',
        'Март' : '3',
        'Апрель' : '4',
        'Май' : '5',
        'Июнь' : '6',
        'Июль' : '7',
        'Август' : '8',
        'Сентябрь' : '9',
        'Октябрь' : '10',
        'Ноябрь' : '11',
        'Декабрь' : '12'
    };
    if (month != '') {
        return month_array[month]
    }
    else {
        return '1'
    }
}
function convertYear(year) {
    if (year != '')
    {
        return year
    }
    else {
        return '2019'
    }

}
