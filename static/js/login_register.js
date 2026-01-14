console.log("script loaded");

// Jeden DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
    console.log("Page loaded correctly.");

    // ====== REJESTRACJA / LOGOWANIE ======
    const registerButton = document.getElementById('registration_form_button');
    const registrationContainer = document.getElementById('registration_container');
    const registrationForm = document.getElementById('register_form');
    const loginButton = document.getElementById('login_form_button');
    const loginContainer = document.getElementById('login_container');
    const loginForm = document.getElementById('login_form');
    const loggedInUserContainer = document.getElementById("logged_in_display_container");

    // Przycisk rejestracji
    if (registerButton && registrationContainer) {
        registerButton.addEventListener('click', () => {
            registrationContainer.style.display = 'block';
            console.log('Registration button clicked. Registration form displayed.');
        });
    }

    // Wysłanie formularza rejestracji
    if (registrationForm) {
        registrationForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('Trying to submit data from the registration form.');

            if (document.getElementById('password').value !== document.getElementById('confirm_password').value) {
                alert('Passwords do not match!');
                return false;
            }

            console.log('Passwords match. Proceeding with form submission.');
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
                    alert('User registered successfully');
                } else {
                    console.error('Registration failed:' + result.error);
                    throw new Error(result.error);
                }
            } catch (error) {
                if (error instanceof TypeError) {
                    console.error('Network error:', error);
                    alert('Could not connect to the server.');
                } else {
                    alert(error.message);
                }
            }
        });
    }

    /// Przycisk logowania (pokazanie formularza)
  if (loginButton && loginContainer) {
    loginButton.addEventListener('click', () => {
      loginContainer.style.display = 'block';
      console.log('Login button clicked. Login form displayed.');
    });
  }

  // Wysłanie formularza logowania
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const loginData = {
        user_name: document.getElementById('login_user_name').value,
        password: document.getElementById('login_password').value
      };
       console.log('loginData:', loginData);
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'same-origin',
          body: JSON.stringify(loginData)
        });

        const result = await response.json().catch(() => ({}));
        console.log('LOGIN status:', response.status, result);

        if (response.ok) {
          window.location.assign(result.redirect_url);
          return;
        }

        alert(result.error || 'Invalid username or password');

      } catch (error) {
        console.error('Network error:', error);
        alert('Could not connect to the server.');
      }
    });
  }
});




//Widocznośc bloków w guest_reservation


function goToStep(stepNumber) {
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active');
    });

    document.getElementById('step' + stepNumber).classList.add('active');
}
