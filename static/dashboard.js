document.addEventListener('DOMContentLoaded', init);

function init() {
    loadEntries();
    generateAndDisplayPasswords();
}

document.getElementById('exportButton').addEventListener('click', exportData);

document.getElementById('searchField').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const entries = document.querySelectorAll('.entry-item');

    entries.forEach(entry => {
        const nameField = entry.querySelector('.name-field');
        const name = nameField.value.toLowerCase();

        if (name.includes(searchTerm)) {
            entry.style.display = '';
        } else {
            entry.style.display = 'none';
        }
    });
});

function loadEntries() {
    fetchEntries().then(displayEntries);
}

function fetchEntries() {
    return fetch('https://onepass.com/api/get_entries', { method: 'GET' })
        .then(response => response.json());
}

function displayEntries(data) {
    const entries = data.entries;
    const entriesList = document.getElementById('entriesList');
    entriesList.innerHTML = '';

    entries.forEach(entry => {
        const entryItem = createEntryListItem(entry);
        entriesList.appendChild(entryItem);
    });
}

function createEntryListItem(entry) {
    const entryItem = document.createElement('li');
    entryItem.className = 'entry-item';
    entryItem.style.display = 'flex';
    entryItem.style.alignItems = 'center';

    const nameField = createInputField('name-field', entry.name, true);
    nameField.style.marginRight = '30px';
    const loginField = createInputField('login-field', entry.login, true);
    const passwordField = createInputField('password-field', entry.password, true, 'password');

    const toggleButton = createButton('Afficher/Masquer Mot de passe', () => togglePasswordVisibility(passwordField));
    const copyLoginButton = createButton('Copier', () => copyToClipboard(loginField));
    copyLoginButton.style.marginRight = '30px';
    const copyPasswordButton = createButton('Copier', () => copyToClipboard(passwordField));
    const deleteButton = createButton('Supprimer', () => confirmAndDeleteEntry(entry.id));

    appendChildren(entryItem, [
        createLabel('Nom'), createSpace(), nameField,
        createLabel('Login'), createSpace(), loginField, copyLoginButton,
        createLabel('Mot de passe'), createSpace(), passwordField, toggleButton, copyPasswordButton,
        deleteButton
    ]);

    return entryItem;
}

function createSpace() {
    const space = document.createElement('span');
    space.textContent = '\u00A0';
    return space;
}

function createInputField(className, value, readOnly, type = 'text') {
    const field = document.createElement('input');
    field.type = type;
    field.className = className;
    field.value = value;
    field.readOnly = readOnly;
    return field;
}

function createButton(text, onClick) {
    const button = document.createElement('button');
    button.textContent = text;
    button.addEventListener('click', onClick);
    return button;
}

function createLabel(text) {
    const label = document.createElement('strong');
    label.appendChild(document.createTextNode(text));
    return label;
}

function appendChildren(parent, children) {
    children.forEach(child => parent.appendChild(child));
}

function togglePasswordVisibility(passwordField) {
    passwordField.type = passwordField.type === 'password' ? 'text' : 'password';
}

function copyToClipboard(field) {
    if (field.type === 'password') {
        field.type = 'text';
        field.select();
        document.execCommand('copy');
        field.type = 'password';
    } else {
        field.select();
        document.execCommand('copy');
    }
}

function confirmAndDeleteEntry(entryId) {
    if (confirm('Voulez-vous vraiment supprimer cette entrée ?')) {
        deleteEntry(entryId);
    }
}

function deleteEntry(entryId) {
    fetch(`https://onepass.com/api/delete_entry/${entryId}`, { method: 'DELETE' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('saveResultMessage').textContent = data.message;
            loadEntries();
        })
        .catch(() => {
            document.getElementById('saveResultMessage').textContent = 'Une erreur s\'est produite lors de la suppression de l\'entrée.';
        });
}

function saveEntry() {
    const entryName = document.getElementById('entryName').value;
    const entryLogin = document.getElementById('entryLogin').value;
    const entryPassword = document.getElementById('entryPassword').value;

    if (!validateEntryFields(entryName, entryLogin, entryPassword)) {
        return;
    }

    fetch('https://onepass.com/api/save_entry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ entryName, entryLogin, entryPassword }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('saveResultMessage').innerText = data.message;
        loadEntries();
    });
}

function validateEntryFields(entryName, entryLogin, entryPassword) {
    let isValid = true;

    if (entryName.length === 0 || entryName.length > 100) {
        displayErrorMessage('entryName', 'Le champ "Nom" doit être rempli et ne peut pas dépasser 100 caractères.');
        isValid = false;
    } else {
        clearErrorMessage('entryName');
    }

    if (entryLogin.length === 0 || entryLogin.length > 100) {
        displayErrorMessage('entryLogin', 'Le champ "Login" doit être rempli et ne peut pas dépasser 100 caractères.');
        isValid = false;
    } else {
        clearErrorMessage('entryLogin');
    }

    if (entryPassword.length === 0 || entryPassword.length > 100) {
        displayErrorMessage('entryPassword', 'Le champ "Mot de passe" doit être rempli et ne peut pas dépasser 100 caractères.');
        isValid = false;
    } else {
        clearErrorMessage('entryPassword');
    }

    return isValid;
}

function displayErrorMessage(fieldId, errorMessage) {
    let errorContainer = document.getElementById(`${fieldId}Error`);
    if (!errorContainer) {
        errorContainer = document.createElement('span');
        errorContainer.id = `${fieldId}Error`;
        errorContainer.className = 'error-message';
        const field = document.getElementById(fieldId);
        field.parentNode.insertBefore(errorContainer, field.nextSibling);
    }
    errorContainer.innerText = errorMessage;
}

function clearErrorMessage(fieldId) {
    const errorContainer = document.getElementById(`${fieldId}Error`);
    if (errorContainer) {
        errorContainer.innerText = '';
    }
}

function logout() {
    fetch('https://onepass.com/api/logout', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        document.getElementById('saveResultMessage').innerText = data.message;
        window.location.href = '/';
    })
    .catch(() => {
        document.getElementById('saveResultMessage').innerText = 'Une erreur s\'est produite lors de la déconnexion.';
    });
}

function generateAndDisplayPasswords() {
    const passwordList = document.getElementById('passwordList');
    passwordList.innerHTML = '';

    const randomPassword = generateRandomPassword();
    const passwordField = createInputField('password-field', randomPassword, true);

    const copyButton = createButton('Copier', () => copyToClipboard(passwordField));

    const passwordItem = document.createElement('li');
    appendChildren(passwordItem, [passwordField, copyButton]);

    passwordList.appendChild(passwordItem);
}

function generateRandomPassword() {
    const length = parseInt(document.getElementById('passwordLength').value);
    const useLowercase = document.getElementById('useLowercase').checked;
    const useUppercase = document.getElementById('useUppercase').checked;
    const useNumbers = document.getElementById('useNumbers').checked;
    const useSpecialChars = document.getElementById('useSpecialChars').checked;

    const lowercaseChars = "abcdefghijklmnopqrstuvwxyz";
    const uppercaseChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const numericChars = "0123456789";
    const specialChars = "!@#$%^&*()_-+=";

    let allChars = "";
    if (useLowercase) allChars += lowercaseChars;
    if (useUppercase) allChars += uppercaseChars;
    if (useNumbers) allChars += numericChars;
    if (useSpecialChars) allChars += specialChars;

    let password = "";
    for (let i = 0; i < length; i++) {
        password += allChars.charAt(Math.floor(Math.random() * allChars.length));
    }

    return password;
}

function exportData() {
    const entries = document.querySelectorAll('.entry-item');

    let csvContent = 'Nom,Login,Mot de passe\n';

    entries.forEach(entry => {
        const name = entry.querySelector('.name-field').value;
        const login = entry.querySelector('.login-field').value;
        const password = entry.querySelector('.password-field').value;

        csvContent += `${name},${login},${password}\n`;
    });

    const csvFile = new Blob([csvContent], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.download = 'password.csv';
    downloadLink.href = window.URL.createObjectURL(csvFile);

    downloadLink.click();
}
