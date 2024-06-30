document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (event) => {
            const usernameInput = form.querySelector('input[type=text], input[type=email], input[type=tel]');
            const passwordInput = form.querySelector('input[type=password]');
            if (usernameInput && passwordInput) {
                setTimeout(() => { // Delay to handle form validation and submission process
                    if (confirm('Voulez-vous enregistrer ce mot de passe dans votre gestionnaire de mots de passe ?')) {
                        chrome.runtime.sendMessage({
                            action: "saveCredentials",
                            data: {
                                url: window.location.hostname,
                                username: usernameInput.value,
                                password: passwordInput.value
                            }
                        });
                    }
                }, 1000);
            }
        });
    });
});
