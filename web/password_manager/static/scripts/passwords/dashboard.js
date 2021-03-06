let passwordsTable,
    decryptPasswordForm, decryptName, decryptMaster, decryptButton,
    addPasswordForm, addName, addPasswordd, addMaster, addPasswordButton,
    changePasswordForm, changeName, changePasswordd, changeMaster, changeButton,
    showHistoryForm, showName, showMaster, showButton;

const MASTER_PASSWORD_MIN_LENGTH = 8, MASTER_PASSWORD_MAX_LENGTH = 30;
const SERVICE_NAME_MIN_LENGTH = 1, SERVICE_NAME_MAX_LENGTH = 30;

window.onload = function () {
    initialize();
}

function initialize() {
    // SHOW PASSWORDS
    passwordsTable = document.getElementById("passwords-table-body");
    getPasswords();


    // DECRYPT PASSWORD
    decryptPasswordForm = document.getElementById("decrypt_frm");
    decryptName = document.getElementById("decrypt-name");
    decryptMaster = document.getElementById("decrypt-master");
    decryptButton = document.getElementById("decrypt-button");
    decryptButton.onclick = () => {
        decryptButton.hidden = true;
        verifyMasterPassword();
        decryptButton.hidden = false;
    }


    // ADD PASSWORD
    addPasswordForm = document.getElementById("add_frm");
    addName = document.getElementById("add-name");
    addPasswordd = document.getElementById("add-password");
    addMaster = document.getElementById("add-master");
    addPasswordButton = document.getElementById("add-button");
    addPasswordButton.onclick = () => {
        addPasswordButton.hidden = true;
        addPassword();
        addPasswordButton.hidden = false;
    }


    // CHANGE PASSWORD
    changePasswordForm = document.getElementById("change_frm");
    changeName = document.getElementById("change-name");
    changePasswordd = document.getElementById("change-password");
    changeMaster = document.getElementById("change-master");
    changeButton = document.getElementById("change-button");
    changeButton.onclick = () => {
        changeButton.hidden = true;
        changePassword();
        changeButton.hidden = false;
    }

    // SHOW PASSWORD HISTORY
    showHistoryForm = document.getElementById("show_frm");
    showName = document.getElementById("show-name");
    showMaster = document.getElementById("show-master");
    showButton = document.getElementById("show-button");
    showButton.onclick = () => {
        showButton.hidden = true;
        showPasswordHistory();
        showButton.hidden = false;
    }
    historyTable = document.getElementById("history-table-body");




    // GENERATE PASSWORD
    generatePasswordForm = document.getElementById("generate_frm");
    generateLength = document.getElementById("generate-length");
    generateButton = document.getElementById("generate-button");
    generateButton.onclick = () => {
        generateButton.hidden = true;
        generatePassword();
        generateButton.hidden = false;
    }

}

// SHOW PASSWORDS
function getPasswords() {
    fetch("/api/passwords/").then(res => { res.json().then(obj => fillPasswordsTable(obj['passes'])); })
}
function fillPasswordsTable(passes) {
    while (passwordsTable.children.length > 0)
        passwordsTable.deleteRow(0);

    passes.forEach(
        pass => {
            const row = passwordsTable.insertRow(-1);
            for (k in pass) {
                var td = document.createElement('td');
                var cv = document.createTextNode(pass[k]);
                td.appendChild(cv);
                row.appendChild(td);
            }
        });
}


// DECRYPT PASSWORD
function verifyMasterPassword() {
    ut = document.getElementById("decrypt-text")
    if (validateVerifyForm()) {
        let formData = new FormData(decryptPasswordForm);
        fetch("/api/passwords/decrypt", { method: 'POST', body: formData }).then(res => {
            if (res.status === 200) {
                res.json().then(obj => {
                    ut.innerHTML = 'Twoje has??o do serwisu ' + decryptName.value + ' to:   ' + obj['pass'];
                    decryptPasswordForm.reset();
                    alert("Has??o dla serwisu " + decryptName.value + " zosta??o odszyfrowane!");
                });
            } else {
                ut.innerHTML = ""
                if (res.status === 429) {
                    alert("Podczas odszyfrowywania has??a wyst??pi?? b????d. Spr??buj ponownie za kilka minut!");
                } else {
                    alert("Podczas odszyfrowywania has??a wyst??pi?? b????d. Spr??buj ponownie p????niej!");
                }
            }
        });
    } else {
        ut.innerHTML = "";
    }
}


// ADD PASSWORD
function addPassword() {
    if (validateAddForm()) {
        let formData = new FormData(addPasswordForm);
        fetch("/api/passwords/", { method: 'POST', body: formData }).then(res => {
            if (res.status === 201) {
                addPasswordForm.reset();
                getPasswords();
                alert("Has??o zosta??o dodane!");
            } else {
                if (res.status === 429) {
                    alert("Podczas dodawania has??a wyst??pi?? b????d. Spr??buj ponownie za kilka minut!");
                } else {
                    alert("Podczas dodawania has??a wyst??pi?? b????d. Spr??buj ponownie p????niej!");
                }
            }
        });
    }
}



// CHANGE PASSWORD
function changePassword() {
    let url = "/api/passwords/";
    let method = 'PUT';
    let formData = new FormData(changePasswordForm);

    fetch(url, { method: method, body: formData }).then(res => {
        if (res.status === 200) {
            changePasswordForm.reset();
            //getPasswords();
            alert("Has??o zosta??o zmienione!");
        } else {
            alert("Podczas zmiany has??a wyst??pi?? b????d. Spr??buj ponownie p????niej!");
        }
    });
}


// SHOW PASSWORD HISTORY
function showPasswordHistory() {
    let url = "/api/passwords/history";
    let method = 'POST';
    let formData = new FormData(showHistoryForm);

    fetch(url, { method: method, body: formData }).then(res => {
        if (res.status === 200) {
            showHistoryForm.reset();
            res.json().then(obj => fillHistoryTable(obj['history']));
        } else {
            alert("Podczas pobierania historii has??a wyst??pi?? b????d. Spr??buj ponownie p????niej!");
        }
    });
}

function fillHistoryTable(history) {
    while (historyTable.children.length > 0)
        historyTable.deleteRow(0);

    history.forEach(
        h => {
            const row = historyTable.insertRow(-1);
            for (k in h) {
                var td = document.createElement('td');
                var cv = document.createTextNode(h[k]);
                td.appendChild(cv);
                row.appendChild(td);
            }
        });
}




// GENERATE PASSWORD
function generatePassword() {
    let url = "/api/passwords/generate/" + generateLength.value;
    fetch(url).then(res => {
        res.json().then(obj => {
            ut = document.getElementById("generate-text");
            ut.innerHTML = 'Wygenerowane has??o : ' + obj['password'];
        })
    })
}


// VALIDATION
function validateVerifyForm() {
    if (("" + decryptName.value).length < SERVICE_NAME_MIN_LENGTH) {
        alert("Nazwa serwisu jest zbyt kr??tka!");
        return false;
    }
    if (("" + decryptName.value).length > SERVICE_NAME_MAX_LENGTH) {
        alert("Nazwa serwisu jest zbyt d??uga!");
        return false;
    }
    if (("" + decryptMaster.value).length < MASTER_PASSWORD_MIN_LENGTH) {
        alert("Has??o g????wne jest zbyt kr??tkie!");
        return false;
    }
    if (("" + decryptMaster.value).length > MASTER_PASSWORD_MAX_LENGTH) {
        alert("Has??o g????wne nie powinno by?? a?? tak d??ugie!");
        return false;
    }
    return true
}

function validateAddForm() {
    if (("" + addName.value).length < SERVICE_NAME_MIN_LENGTH) {
        alert("Nazwa serwisu jest zbyt kr??tka!");
        return false;
    }
    if (("" + addName.value).length > SERVICE_NAME_MAX_LENGTH) {
        alert("Nazwa serwisu jest zbyt d??uga!");
        return false;
    }
    if (("" + addPasswordd.value).length <= 0) {
        alert("Has??o nie mo??e by?? puste!");
        return false;
    }
    if (("" + addPasswordd.value).length > 40) {
        alert("Has??o nie powinno by?? a?? tak d??ugie!");
        return false;
    }
    if (("" + addMaster.value).length < MASTER_PASSWORD_MIN_LENGTH) {
        alert("Has??o g????wne jest zbyt kr??tkie!");
        return false;
    }
    if (("" + addMaster.value).length > MASTER_PASSWORD_MAX_LENGTH) {
        alert("Has??o g????wne nie powinno by?? a?? tak d??ugie!");
        return false;
    }
    return true
}

