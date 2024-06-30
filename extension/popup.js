document.addEventListener('DOMContentLoaded', function () {
    const loginContainer = document.getElementById('login-container');
    const signUpContainer = document.getElementById('signup-container');
    const dashboardContainer = document.getElementById('dashboard-container');
    const showSignUpLink = document.getElementById('showSignUp');
    const showLoginLink = document.getElementById('showLogin');
    const goToDashboardFromLogin = document.getElementById('goToDashboardFromLogin');
    const goToDashboardFromSignUp = document.getElementById('goToDashboardFromSignUp');

    showSignUpLink.addEventListener('click', function () {
        loginContainer.style.display = 'none';
        signUpContainer.style.display = 'block';
    });

    showLoginLink.addEventListener('click', function () {
        signUpContainer.style.display = 'none';
        loginContainer.style.display = 'block';
    });

    goToDashboardFromLogin.addEventListener('click', function () {
        loginContainer.style.display = 'none';
        dashboardContainer.style.display = 'block';
    });

    goToDashboardFromSignUp.addEventListener('click', function () {
        signUpContainer.style.display = 'none';
        dashboardContainer.style.display = 'block';
    });

    document.getElementById('loginForm').addEventListener('submit', function(event) {
        event.preventDefault();
        login();
    });

    document.getElementById('signUpForm').addEventListener('submit', function(event) {
        event.preventDefault();
        signUp();
    });

    function login() {
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        fetch('http://192.168.1.97:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                document.getElementById('loginMessage').innerText = 'Connexion réussie !';
                loginContainer.style.display = 'none';
                dashboardContainer.style.display = 'block';
                localStorage.setItem('token', data.token); // Store the token
                initDashboard(); // Initialize the dashboard view
            } else {
                document.getElementById('loginMessage').innerText = data.message || 'Erreur lors de la connexion.';
            }
        })
        .catch(error => {
            console.error('Erreur lors de la connexion', error);
            document.getElementById('loginMessage').innerText = 'Connexion impossible. Veuillez réessayer.';
        });
    }

    function signUp() {
        const username = document.getElementById('signUpUsername').value;
        const password = document.getElementById('signUpPassword').value;

        fetch('http://192.168.1.97:5000/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                document.getElementById('signUpMessage').innerText = 'Compte créé avec succès !';
                signUpContainer.style.display = 'none';
                dashboardContainer.style.display = 'block';
                localStorage.setItem('token', data.token); // Store the token
                initDashboard(); // Initialize the dashboard view
            } else {
                document.getElementById('signUpMessage').innerText = data.message || 'Erreur lors de la création du compte.';
            }
        })
        .catch(error => {
            console.error('Erreur lors de la création du compte', error);
            document.getElementById('signUpMessage').innerText = 'Erreur lors de la création du compte. Veuillez réessayer.';
        });
    }

    function initDashboard() {
        console.log('Initializing dashboard');
        getEntries();
        generateAndDisplayPasswords();
    }
});
