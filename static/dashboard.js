// static/dashboard.js
document.addEventListener('DOMContentLoaded', function () {
    // Appelle getEntries() lorsque la page est chargée
    getEntries();
    generateAndDisplayPasswords();
});

function getEntries() {
    fetch('/api/get_entries', { method: 'GET' })
        .then(response => response.json())
        .then(handleEntries)
}

function handleEntries(data) {
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

    const nameField = createNameField(entry.name);
    nameField.style.marginRight = '30px';
    const loginField = createLoginField(entry.login);
    const passwordField = createPasswordField(entry.password);

    const toggleButton = createToggleButton(passwordField);
    const copyLoginButton = createCopyButton(loginField, 'Copier Login');
    copyLoginButton.style.marginRight = '30px';
    const copyPasswordButton = createCopyButton(passwordField, 'Copier Mot de passe');

    const nameText = document.createElement('strong');
    nameText.appendChild(document.createTextNode('Nom'));
    entryItem.appendChild(nameText);
    entryItem.appendChild(document.createTextNode('\u00A0')); // Ajout d'un espace insécable
    entryItem.appendChild(nameField);

    const loginText = document.createElement('strong');
    loginText.appendChild(document.createTextNode('Login'));
    entryItem.appendChild(loginText);
    entryItem.appendChild(document.createTextNode('\u00A0')); // Ajout d'un espace insécable
    entryItem.appendChild(loginField);
    entryItem.appendChild(copyLoginButton); // Ajoute le bouton de copie pour le login

    const passwordText = document.createElement('strong');
    passwordText.appendChild(document.createTextNode('Mot de passe'));
    entryItem.appendChild(passwordText);
    entryItem.appendChild(document.createTextNode('\u00A0')); // Ajout d'un espace insécable
    entryItem.appendChild(passwordField);
    entryItem.appendChild(toggleButton);
    entryItem.appendChild(copyPasswordButton); // Ajoute le bouton de copie pour le mot de passe

    // Ajouter le bouton de suppression avec l'ID de l'entrée
    const deleteButton = createDeleteButton(entry.id);
    entryItem.appendChild(deleteButton);

    return entryItem;
}

function createNameField(name) {
    const nameField = document.createElement('input');
    nameField.type = 'text';
    nameField.className = 'name-field';
    nameField.value = name;
    nameField.readOnly = true;
    return nameField;
}

function createLoginField(login) {
    const loginField = document.createElement('input');
    loginField.type = 'text'; // Utilisez le type 'text' pour rendre le login visible
    loginField.className = 'login-field';
    loginField.value = login;
    loginField.readOnly = true;
    return loginField;
}

function createPasswordField(password) {
    const passwordField = document.createElement('input');
    passwordField.type = 'password';
    passwordField.className = 'password-field';
    passwordField.value = password;
    passwordField.readOnly = true;
    return passwordField;
}

function createToggleButton(passwordField) {
    const toggleButton = document.createElement('button');
    toggleButton.textContent = 'Afficher/Masquer Mot de passe';
    toggleButton.addEventListener('click', function () {
        passwordField.type = (passwordField.type === 'password') ? 'text' : 'password';
    });
    return toggleButton;
}

function createDeleteButton(entryId) {
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Supprimer';

    // Ajoutez un gestionnaire d'événement pour le clic sur le bouton de suppression
    deleteButton.addEventListener('click', function () {
        // Demande de confirmation avant la suppression
        const confirmed = confirm('Voulez-vous vraiment supprimer cette entrée?');

        if (confirmed) {
            // Appel à la fonction de suppression avec l'ID de l'entrée
            deleteEntry(entryId);
        }
    });

    return deleteButton;
}

function saveEntry() {
    // Récupérer les valeurs des champs
    const entryName = document.getElementById('entryName').value;
    const entryLogin = document.getElementById('entryLogin').value;
    const entryPassword = document.getElementById('entryPassword').value;

    // Vérifier la longueur des champs et afficher les messages d'erreur à côté des champs correspondants
    if (entryName.length === 0 || entryName.length > 100) {
        displayErrorMessage('entryName', 'Le champ "Nom" doit être rempli et ne peut pas dépasser 100 caractères.');
        return;
    } else {
        clearErrorMessage('entryName');
    }

    if (entryLogin.length === 0 || entryLogin.length > 100) {
        displayErrorMessage('entryLogin', 'Le champ "Login" doit être rempli et ne peut pas dépasser 100 caractères.');
        return;
    } else {
        clearErrorMessage('entryLogin');
    }

    if (entryPassword.length === 0 || entryPassword.length > 100) {
        displayErrorMessage('entryPassword', 'Le champ "Mot de passe" doit être rempli et ne peut pas dépasser 100 caractères.');
        return;
    } else {
        clearErrorMessage('entryPassword');
    }

    // Effectuer l'appel à l'API uniquement si les vérifications passent
    fetch('/api/save_entry', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ entryName, entryLogin, entryPassword }),
    })
    .then(response => response.json())
    .then(data => {
        // Afficher le message de résultat
        document.getElementById('saveResultMessage').innerText = data.message;

        // Mettre à jour la liste des entrées
        getEntries();
    });
}

// Fonction pour afficher un message d'erreur à côté d'un champ spécifique
function displayErrorMessage(fieldId, errorMessage) {
    const errorContainer = document.getElementById(`${fieldId}Error`);
    if (errorContainer) {
        errorContainer.innerText = errorMessage;
    } else {
        // Créer un élément span pour afficher le message d'erreur
        const errorSpan = document.createElement('span');
        errorSpan.id = `${fieldId}Error`;
        errorSpan.className = 'error-message'; // Ajouter cette ligne pour une classe spécifique
        errorSpan.innerText = errorMessage;

        // Insérer le message d'erreur après le champ correspondant
        const field = document.getElementById(fieldId);
        if (field) {
            field.parentNode.insertBefore(errorSpan, field.nextSibling);
        }
    }
}

// Fonction pour effacer un message d'erreur à côté d'un champ spécifique
function clearErrorMessage(fieldId) {
    const errorContainer = document.getElementById(`${fieldId}Error`);
    if (errorContainer) {
        errorContainer.innerText = '';
    }
}

function deleteEntry(entryId) {
    fetch(`/api/delete_entry/${entryId}`, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => {
            const saveResultMessage = document.getElementById('saveResultMessage');
            saveResultMessage.textContent = data.message;
            getEntries(); // Mettre à jour la liste après la suppression
        })
        .catch(error => console.error('Error deleting entry:', error));
}

function logout() {
    fetch('/api/logout', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('saveResultMessage').innerText = data.message;
        // Rediriger vers la page de connexion après la déconnexion
        window.location.href = '/';
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('saveResultMessage').innerText = 'Une erreur s\'est produite lors de la déconnexion.';
    });
}

function generateRandomPassword() {
    const length = document.getElementById('passwordLength').value;
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
        const randomIndex = Math.floor(Math.random() * allChars.length);
        password += allChars.charAt(randomIndex);
    }

    return password;
}

function getRandomChar(characters) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    return characters.charAt(randomIndex);
}

function generateAndDisplayPasswords() {
    const passwordList = document.getElementById('passwordList');
    passwordList.innerHTML = '';

    // Générer un seul mot de passe
    const randomPassword = generateRandomPassword();

    const passwordItem = document.createElement('li');

    // Utilisez un champ de texte au lieu d'un champ de mot de passe
    const passwordField = createTextField(randomPassword);

    // Ajoutez un bouton de copie pour le mot de passe
    const copyButton = createCopyButton(passwordField);

    passwordItem.appendChild(passwordField);
    passwordItem.appendChild(copyButton);

    passwordList.appendChild(passwordItem);
}

// Ajoutez cette fonction pour créer un champ de texte mot de passe aléatoire
function createTextField(password) {
    const textField = document.createElement('input');
    textField.type = 'text';
    textField.className = 'password-field';
    textField.value = password;
    textField.readOnly = true;
    return textField;
}

function createCopyButton(textField) {
    const copyButton = document.createElement('button');
    copyButton.textContent = 'Copier';

    copyButton.addEventListener('click', function () {
        // Sauvegarder le type du champ
        const fieldType = textField.type;

        // Temporairement changer le type du champ à 'text'
        textField.type = 'text';

        // Sélectionner et copier le texte
        textField.select();
        document.execCommand('copy');

        // Rétablir le type du champ à son état initial
        textField.type = fieldType;
    });

    return copyButton;
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
    downloadLink.style.display = 'none';

    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

document.getElementById('exportButton').addEventListener('click', exportData);
