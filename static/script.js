document.addEventListener('DOMContentLoaded', () => {
    console.log("Page loaded correctly.");
    // 1. Definicja zmiennych (const ...)
    const registerButton = document.getElementById('registration_form_button');
    const registrationContainter = document.getElementById('registration_container');
    const form = document.getElementById('register_form');
    // 2. Nasłuchiwanie przycisków
    // Przycisk rejestracji
    if (registerButton) {
        registerButton.addEventListener('click', () => {   
            registrationContainter.style.display = 'block';
            console.log('Registration button clicked. Registration form displayed.');
        });
    }
    // Przycisk wysłania formularza rejestracji (pobrania danych i wysłania do API)
    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('Trying to submit data from the registration form.');
            const formData = {
                first_name: document.getElementById('first_name').value,
                last_name: document.getElementById('last_name').value,
                email: document.getElementById('email').value,
                phone_number: document.getElementById('phone_number').value,
                user_name: document.getElementById('user_name').value,
                password: document.getElementById('password').value,
                user_type_id: parseInt(document.getElementById('user_type').value)
        };
            try {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                const result = await response.json();
                if (response.ok) {
                    console.log('Registration successful:' + result.message);

                } else {
                    console.error('Registration failed:' + result.error);
                }
            } catch (error) {
                console.error('Network error:', error);
                alert('Could not connect to the server.');
            }
        });
    }
    //Do zrobienia:
        // 3. Logika formularza
        // 4. Rezerwowanie stolika
        // 5. Logowanie
});