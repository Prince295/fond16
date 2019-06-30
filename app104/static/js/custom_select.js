$('#select_month_1').ready( function () {
    const inputField = document.getElementById('select_month_1').querySelector('.chosen-value');
    const dropdown = document.getElementById('select_month_1').querySelector('.value-list');
    const dropdownArray = [... document.getElementById('select_month_1').querySelectorAll('.li-selector')];
    // dropdown.classList.add('open');
    // inputField.focus(); // Demo purposes only
    let valueArray = [];
    dropdownArray.forEach(item => {
      valueArray.push(item.textContent);
    });

    const closeDropdown = () => {
      dropdown.classList.remove('open');
    }

    inputField.addEventListener('input', () => {
      dropdown.classList.add('open');
      let inputValue = inputField.value.toLowerCase();
      let valueSubstring;
      if (inputValue.length > 0) {
        for (let j = 0; j < valueArray.length; j++) {
          if (!(inputValue.substring(0, inputValue.length) === valueArray[j].substring(0, inputValue.length).toLowerCase())) {
            dropdownArray[j].classList.add('closed');
          } else {
            dropdownArray[j].classList.remove('closed');
          }
        }
      } else {
        for (let i = 0; i < dropdownArray.length; i++) {
          dropdownArray[i].classList.remove('closed');
        }
      }
    });

    dropdownArray.forEach(item => {
      item.addEventListener('click', (evt) => {
        inputField.value = item.textContent;
        dropdownArray.forEach(dropdown => {
          dropdown.classList.add('closed');
        });
      });
    })

    inputField.addEventListener('focus', () => {
       inputField.placeholder = 'Начните вводить..';
       dropdown.classList.add('open');
       dropdownArray.forEach(dropdown => {
         dropdown.classList.remove('closed');
       });
    });

    inputField.addEventListener('blur', () => {
       inputField.placeholder = 'Январь';
      dropdown.classList.remove('open');
    });

    document.getElementById('select_month_1').addEventListener('click', (evt) => {
      const isDropdown = dropdown.contains(evt.target);
      const isInput = inputField.contains(evt.target);
      if (!isDropdown && !isInput) {
        dropdown.classList.remove('open');
      }
    });
});




$('#select_year_1').ready( function () {
    const inputField = document.getElementById('select_year_1').querySelector('.chosen-value');
    const dropdown = document.getElementById('select_year_1').querySelector('.value-list');
    const dropdownArray = [... document.getElementById('select_year_1').querySelectorAll('.li-selector')];
    // dropdown.classList.add('open');
    // inputField.focus(); // Demo purposes only
    let valueArray = [];
    dropdownArray.forEach(item => {
      valueArray.push(item.textContent);
    });

    const closeDropdown = () => {
      dropdown.classList.remove('open');
    }

    inputField.addEventListener('input', () => {
      dropdown.classList.add('open');
      let inputValue = inputField.value.toLowerCase();
      let valueSubstring;
      if (inputValue.length > 0) {
        for (let j = 0; j < valueArray.length; j++) {
          if (!(inputValue.substring(0, inputValue.length) === valueArray[j].substring(0, inputValue.length).toLowerCase())) {
            dropdownArray[j].classList.add('closed');
          } else {
            dropdownArray[j].classList.remove('closed');
          }
        }
      } else {
        for (let i = 0; i < dropdownArray.length; i++) {
          dropdownArray[i].classList.remove('closed');
        }
      }
    });

    dropdownArray.forEach(item => {
      item.addEventListener('click', (evt) => {
        inputField.value = item.textContent;
        dropdownArray.forEach(dropdown => {
          dropdown.classList.add('closed');
        });
      });
    })

    inputField.addEventListener('focus', () => {
       inputField.placeholder = 'Начните вводить..';
       dropdown.classList.add('open');
       dropdownArray.forEach(dropdown => {
         dropdown.classList.remove('closed');
       });
    });

    inputField.addEventListener('blur', () => {
       inputField.placeholder = '2019';
      dropdown.classList.remove('open');
    });

    document.getElementById('select_year_1').addEventListener('click', (evt) => {
      const isDropdown = dropdown.contains(evt.target);
      const isInput = inputField.contains(evt.target);
      if (!isDropdown && !isInput) {
        dropdown.classList.remove('open');
      }
    });
});


$('#select_month_2').ready( function () {
    const inputField = document.getElementById('select_month_2').querySelector('.chosen-value');
    const dropdown = document.getElementById('select_month_2').querySelector('.value-list');
    const dropdownArray = [... document.getElementById('select_month_2').querySelectorAll('.li-selector')];
    // dropdown.classList.add('open');
    // inputField.focus(); // Demo purposes only
    let valueArray = [];
    dropdownArray.forEach(item => {
      valueArray.push(item.textContent);
    });

    const closeDropdown = () => {
      dropdown.classList.remove('open');
    }

    inputField.addEventListener('input', () => {
      dropdown.classList.add('open');
      let inputValue = inputField.value.toLowerCase();
      let valueSubstring;
      if (inputValue.length > 0) {
        for (let j = 0; j < valueArray.length; j++) {
          if (!(inputValue.substring(0, inputValue.length) === valueArray[j].substring(0, inputValue.length).toLowerCase())) {
            dropdownArray[j].classList.add('closed');
          } else {
            dropdownArray[j].classList.remove('closed');
          }
        }
      } else {
        for (let i = 0; i < dropdownArray.length; i++) {
          dropdownArray[i].classList.remove('closed');
        }
      }
    });

    dropdownArray.forEach(item => {
      item.addEventListener('click', (evt) => {
        inputField.value = item.textContent;
        dropdownArray.forEach(dropdown => {
          dropdown.classList.add('closed');
        });
      });
    })

    inputField.addEventListener('focus', () => {
       inputField.placeholder = 'Начните вводить..';
       dropdown.classList.add('open');
       dropdownArray.forEach(dropdown => {
         dropdown.classList.remove('closed');
       });
    });

    inputField.addEventListener('blur', () => {
       inputField.placeholder = 'Январь';
      dropdown.classList.remove('open');
    });

    document.getElementById('select_month_2').addEventListener('click', (evt) => {
      const isDropdown = dropdown.contains(evt.target);
      const isInput = inputField.contains(evt.target);
      if (!isDropdown && !isInput) {
        dropdown.classList.remove('open');
      }
    });
});

$('#select_year_2').ready( function () {
    const inputField = document.getElementById('select_year_2').querySelector('.chosen-value');
    const dropdown = document.getElementById('select_year_2').querySelector('.value-list');
    const dropdownArray = [... document.getElementById('select_year_2').querySelectorAll('.li-selector')];
    // dropdown.classList.add('open');
    // inputField.focus(); // Demo purposes only
    let valueArray = [];
    dropdownArray.forEach(item => {
      valueArray.push(item.textContent);
    });

    const closeDropdown = () => {
      dropdown.classList.remove('open');
    }

    inputField.addEventListener('input', () => {
      dropdown.classList.add('open');
      let inputValue = inputField.value.toLowerCase();
      let valueSubstring;
      if (inputValue.length > 0) {
        for (let j = 0; j < valueArray.length; j++) {
          if (!(inputValue.substring(0, inputValue.length) === valueArray[j].substring(0, inputValue.length).toLowerCase())) {
            dropdownArray[j].classList.add('closed');
          } else {
            dropdownArray[j].classList.remove('closed');
          }
        }
      } else {
        for (let i = 0; i < dropdownArray.length; i++) {
          dropdownArray[i].classList.remove('closed');
        }
      }
    });

    dropdownArray.forEach(item => {
      item.addEventListener('click', (evt) => {
        inputField.value = item.textContent;
        dropdownArray.forEach(dropdown => {
          dropdown.classList.add('closed');
        });
      });
    })

    inputField.addEventListener('focus', () => {
       inputField.placeholder = 'Начните вводить..';
       dropdown.classList.add('open');
       dropdownArray.forEach(dropdown => {
         dropdown.classList.remove('closed');
       });
    });

    inputField.addEventListener('blur', () => {
       inputField.placeholder = '2019';
      dropdown.classList.remove('open');
    });

    document.getElementById('select_year_2').addEventListener('click', (evt) => {
      const isDropdown = dropdown.contains(evt.target);
      const isInput = inputField.contains(evt.target);
      if (!isDropdown && !isInput) {
        dropdown.classList.remove('open');
      }
    });
});

$('#smo_selection').ready( function () {
    const inputField = document.getElementById('smo_selection').querySelector('.chosen-value');
    const dropdown = document.getElementById('smo_selection').querySelector('.value-list');
    const dropdownArray = [... document.getElementById('smo_selection').querySelectorAll('.li-selector')];
    // dropdown.classList.add('open');
    // inputField.focus(); // Demo purposes only
    let valueArray = [];
    dropdownArray.forEach(item => {
      valueArray.push(item.textContent);
    });

    const closeDropdown = () => {
      dropdown.classList.remove('open');
    }

    inputField.addEventListener('input', () => {
      dropdown.classList.add('open');
      let inputValue = inputField.value.toLowerCase();
      let valueSubstring;
      if (inputValue.length > 0) {
        for (let j = 0; j < valueArray.length; j++) {
          if (!(inputValue.substring(0, inputValue.length) === valueArray[j].substring(0, inputValue.length).toLowerCase())) {
            dropdownArray[j].classList.add('closed');
          } else {
            dropdownArray[j].classList.remove('closed');
          }
        }
      } else {
        for (let i = 0; i < dropdownArray.length; i++) {
          dropdownArray[i].classList.remove('closed');
        }
      }
    });

    dropdownArray.forEach(item => {
      item.addEventListener('click', (evt) => {


        if (evt.target.classList.contains('checked_smo')) {
            evt.target.style.backgroundColor = '#fafcfd';
            evt.target.classList.remove('checked_smo');
        }
        else {
            evt.target.style.backgroundColor = '#5bc0de';
            evt.target.classList.add('checked_smo');
        }
        // dropdown.classList.add('closed');
          let smo_endswith = getEndswithOrganisation(dropdown.getElementsByClassName('checked_smo').length);
        inputField.value = 'Выбрано всего : ' + dropdown.getElementsByClassName('checked_smo').length + ' ' + smo_endswith;
      });
    })

    inputField.addEventListener('focus', () => {
       inputField.placeholder = 'Начните вводить..';
       dropdown.classList.add('open');
       dropdownArray.forEach(dropdown => {
           dropdown.classList.remove('closed');
       });
    });

    inputField.addEventListener('blur', () => {
       inputField.placeholder = 'Выберите страховую компанию';
      // dropdown.classList.remove('open');
    });

    document.addEventListener('click', (evt) => {
      const isDropdown = dropdown.contains(evt.target);
      const isInput = inputField.contains(evt.target);
      if (!isDropdown && !isInput) {
          inputField.placeholder = 'Выберите страховую компанию';
          dropdown.classList.remove('open');
          dropdown.classList.add('closed');
      }
    });

});

$('#mo_selection').ready( function () {
    const inputField = document.getElementById('mo_selection').querySelector('.chosen-value');
    const dropdown = document.getElementById('mo_selection').querySelector('.value-list');
    const dropdownArray = [... document.getElementById('mo_selection').querySelectorAll('.li-selector')];
    // dropdown.classList.add('open');
    // inputField.focus(); // Demo purposes only
    let valueArray = [];
    dropdownArray.forEach(item => {
      valueArray.push(item.textContent);
    });

    const closeDropdown = () => {
      dropdown.classList.remove('open');
    }

    inputField.addEventListener('input', () => {
      dropdown.classList.add('open');
      let inputValue = inputField.value.toLowerCase();
      let valueSubstring;
      if (inputValue.length > 0) {
        for (let j = 0; j < valueArray.length; j++) {
          if (!(inputValue.substring(0, inputValue.length) === valueArray[j].substring(0, inputValue.length).toLowerCase())) {
            dropdownArray[j].classList.add('closed');
          } else {
            dropdownArray[j].classList.remove('closed');
          }
        }
      } else {
        for (let i = 0; i < dropdownArray.length; i++) {
          dropdownArray[i].classList.remove('closed');
        }
      }
    });

    dropdownArray.forEach(item => {
      item.addEventListener('click', (evt) => {


        if (evt.target.classList.contains('checked_mo')) {
            evt.target.style.backgroundColor = '#fafcfd';
            evt.target.classList.remove('checked_mo');

        }
        else {
            evt.target.style.backgroundColor = '#5bc0de';
            evt.target.classList.add('checked_mo');

        }
        let mo_endswith = getEndswithHospital(dropdown.getElementsByClassName('checked_mo').length);
        inputField.value = 'Выбрано всего : ' + dropdown.getElementsByClassName('checked_mo').length + ' ' + mo_endswith;

      });
    })

    inputField.addEventListener('focus', () => {
       inputField.placeholder = 'Начните вводить..';
       dropdown.classList.add('open');
       dropdownArray.forEach(dropdown => {
           dropdown.classList.remove('closed');
       });
    });

    inputField.addEventListener('blur', () => {
       inputField.placeholder = 'Выберите муниципальное образование';
      // dropdown.classList.remove('open');
    });

    document.addEventListener('click', (evt) => {
      const isDropdown = dropdown.contains(evt.target);
      const isInput = inputField.contains(evt.target);
      if (!isDropdown && !isInput) {
          inputField.placeholder = 'Выберите муниципальное образование';
          dropdown.classList.remove('open');
          dropdown.classList.add('closed');
      }
    });

});
function getEndswithOrganisation(len_array) {
    if ((len_array >= 11) & (len_array <= 19)) {
        return 'Организаций'
    }
    else if ((len_array % 10) == 1 ) {

        return 'Организация'
    }
    else if ((len_array % 10) == 0 ) {
        return 'Организаций'
    }
    else if ((len_array % 10) < 5  ){
        return 'Организации'
    }
    else {
        return 'Организаций'
    }
}

function getEndswithHospital(len_array) {
    if ((len_array >= 11) & (len_array <= 19)) {
        return 'Муниципальных образований'
    }
    else if ((len_array % 10) == 1 ) {

        return 'Муниципальное образование'
    }
    else if ((len_array % 10) == 0 ) {
        return 'Муниципальных образований'
    }
    else if ((len_array % 10) < 5  ){
        return 'Муниципальных образования'
    }
    else {
        return 'Муниципальных образований'
    }
}
