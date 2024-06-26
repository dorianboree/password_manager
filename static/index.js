function performRequest(url, method, data, successMessage, errorMessage, redirectUrl) {
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
                setTimeout(() => {
                    window.location.href = redirectUrl;
                }, 1000);
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

function checkPassword(password) {
    if (password.length < 8 || password.length > 80) {
        return false;
    }
    if (!/\d/.test(password)) {
        return false;
    }
    if (!/[A-Z]/.test(password)) {
        return false;
    }
    if (!/[a-z]/.test(password)) {
        return false;
    }
    var specialCharacters = "!@#$%^&*()-+?_=,<>/";
    if (!new RegExp('[' + specialCharacters + ']').test(password)) {
        return false;
    }
    return true;
}

function checkUsername(username) {
    if (username.length < 8 || username.length > 30) {
        return false;
    }
    var specialCharacters = "!@#$%^&*()-+?_=,<>/ÀàÂâÉéÈèÊêËëÎîÏïÔôŒœÙùÛûÜüÇç";
    if (new RegExp('[' + specialCharacters + ']').test(username)) {
        return false;
    }
    return true;
}

function createAccount(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!checkUsername(username)) {
        document.getElementById('resultMessage').innerText = 'Le nom d\'utilisateur doit comporter entre 8 et 30 caractères et ne doit pas contenir de caractères spéciaux ou de lettre avec accent.';
        document.getElementById('resultMessage').classList.remove('success');
        document.getElementById('resultMessage').classList.add('error');
        return;
    }

    if (!checkPassword(password)) {
        document.getElementById('resultMessage').innerText = 'Le mot de passe doit comporter entre 8 et 80 caractères, dont une majuscule, une minuscule, un chiffre et un caractère spécial.';
        document.getElementById('resultMessage').classList.remove('success');
        document.getElementById('resultMessage').classList.add('error');
        return;
    }

    performRequest('https://onepass.com/api/create_account', 'POST', { username, password }, 'Compte créé avec succès !', 'Une erreur s\'est produite lors de la création du compte.');
}

function login(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!checkUsername(username)) {
        document.getElementById('resultMessage').innerText = 'Le nom d\'utilisateur doit comporter entre 8 et 30 caractères et ne doit pas contenir de caractères spéciaux.';
        document.getElementById('resultMessage').classList.remove('success');
        document.getElementById('resultMessage').classList.add('error');
        return;
    }

    if (!checkPassword(password)) {
        document.getElementById('resultMessage').innerText = 'Le mot de passe doit comporter entre 8 et 80 caractères, dont une majuscule, une minuscule, un chiffre et un caractère spécial.';
        document.getElementById('resultMessage').classList.remove('success');
        document.getElementById('resultMessage').classList.add('error');
        return;
    }

    performRequest('https://onepass.com/api/login', 'POST', { username, password }, 'Connexion réussie !', 'Nom d\'utilisateur ou mot de passe incorrect.', '/static/dashboard.html');
}
