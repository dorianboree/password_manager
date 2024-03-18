function performRequest(url, method, data, successMessage, errorMessage, redirectUrl) {
    event.preventDefault();

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        const resultMessageElement = document.getElementById('resultMessage');
        resultMessageElement.innerText = data.message;

        if (data.message === successMessage) {
            resultMessageElement.classList.remove('error');
            resultMessageElement.classList.add('success');

            if (redirectUrl) {
                window.location.href = redirectUrl;
            }
        } else {
            resultMessageElement.classList.remove('success');
            resultMessageElement.classList.add('error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const resultMessageElement = document.getElementById('resultMessage');
        resultMessageElement.innerText = errorMessage;
        resultMessageElement.classList.remove('success');
        resultMessageElement.classList.add('error');
    });
}

function createAccount() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username.length < 8) {
        document.getElementById('resultMessage').innerText = 'Le nom d\'utilisateur doit comporter au moins 8 caractères.';
        return;
    }

    if (password.length < 8) {
        document.getElementById('resultMessage').innerText = 'Le mot de passe doit comporter au moins 8 caractères.';
        return;
    }

    performRequest('/api/create_account', 'POST', { username, password }, 'Compte créé avec succès !', 'Une erreur s\'est produite lors de la création du compte.');
}

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username.length < 8) {
        document.getElementById('resultMessage').innerText = 'Le nom d\'utilisateur doit comporter au moins 8 caractères.';
        return;
    }

    if (password.length < 8) {
        document.getElementById('resultMessage').innerText = 'Le mot de passe doit comporter au moins 8 caractères.';
        return;
    }

    performRequest('/api/login', 'POST', { username, password }, 'Connexion réussie !', 'Une erreur s\'est produite lors de la connexion.', '/static/dashboard.html');
}
