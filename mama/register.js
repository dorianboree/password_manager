document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('registerForm');

    registerForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const formData = {
            username: username,
            password: password
        };

        // Exemple d'envoi de données à l'API Flask (à remplacer par votre logique d'envoi)
        fetch('http://192.168.1.97:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);  // Exemple d'affichage de message (à adapter)
        })
        .catch(error => console.error('Erreur lors de l\'inscription :', error));
    });
});
