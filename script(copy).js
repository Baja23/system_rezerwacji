console.log("script loaded");


document.addEventListener('DOMContentLoaded', () => {
    console.log("Page loaded correctly.");
    // 1. Definicja zmiennych (const ...)
    const registerButton = document.getElementById('registration_form_button');
    const registrationContainer = document.getElementById('registration_container');
    const registrationForm = document.getElementById('register_form');
    const loginButton = document.getElementById('login_form_button');
    const loginContainer = document.getElementById('login_container');
    const loginForm = document.getElementById('login_form');
    const loggedInUserContainer = document.getElementById("logged_in_display_container");
    const reservationButton = document.getElementById('reservation_form_button');
    const reservationContainer = document.getElementById('reservation_container');
    const reservationForm = document.getElementById('reservation_form');
    // 2. Nasłuchiwanie przycisków
    // Przycisk rejestracji
    if (registerButton) {
        registerButton.addEventListener('click', () => {
            registrationContainer.style.display = 'block';
            console.log('Registration button clicked. Registration form displayed.');
        });
    }

    // Przycisk wysłania formularza rejestracji (pobrania danych i wysłania do API)
    if (registrationForm) {
        registrationForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('Trying to submit data from the registration form.');
            if(document.getElementById('password').value !== document.getElementById('confirm_password').value) {
                alert('Passwords do not match!');
                return false;
            }
            else {
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
                    alert('User registered successfully')
                // Lekka modyfikacja, do else wrzuciłem ładowanie błędu, a catch podzieliłem na błąd sieci oraz wygenerowanie błędu zaciągniętego z else
                } else {
                    console.error('Registration failed:' + result.error);
                    throw new Error(result.error);
                }
            } catch (error) {
                if (error instanceof TypeError) {
                console.error('Network error:', error);
                alert('Could not connect to the server.');
                }
                else {
                    alert(error.message);
                }
            }
        }
        });
    }

    // Przycisk logowania
    if (loginButton) {
        loginButton.addEventListener('click', () => {
            loginContainer.style.display = 'block';
            console.log('Login button clicked. Login form displayed.');
        });
    }

    // Przycisk wysłania formularza logowania
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('Trying to submit data from the login form.');
            const loginData = {
                user_name: document.getElementById('login_user_name').value,
                password: document.getElementById('login_password').value
            };
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(loginData)
                });
                const result = await response.json();
                if (response.ok) {
                    console.log('Login successful:' + result.message);
                    loggedInUserContainer.style.display = 'block';
                    loginContainer.style.display = 'none';

                } else {
                    console.error('Login failed:' + result.error);
                    alert('error: Invalid username or password')
                }
            } catch (error) {
                console.error('Network error:', error);
                alert('Could not connect to the server.');

            }
        });
    }
//--------- Pobieranie danych z bazy danych i przesyłanie do frontendu na temat aktywnych rezerwacji--------------
// pobranie listy rezerwacji z backendu

async function loadReservations() {
  console.log("loadReservations: START");

  const res = await fetch('/api/reservations');
  console.log("HTTP status:", res.status);

  if (!res.ok) {
    console.error('fetch not OK');
    return;
  }

  let data;
  try {
    data = await res.json();
  } catch (e) {
    console.error("JSON parse error:", e);
    return;
  }

  console.log("DATA RECEIVED:", data);

  const tbody = document.querySelector('#reservations-table tbody');
  console.log("Tbody element found:", !!tbody);

  tbody.innerHTML = "";

  console.log("Cleared tbody.");

  if (!Array.isArray(data)) {
    console.error("Data is not array!");
    return;
  }

  console.log("Data length:", data.length);

  data.forEach((r, index) => {
    console.log("Row", index, r);

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${r.id}</td>
      <td>${r.first_name}</td>
      <td>${r.last_name}</td>
      <td>${r.date}</td>
      <td>${r.start_time}</td>
      <td>${r.end_time}</td>
      <td>${r.number_of_people}</td>
      <td>${r.status || ''}</td>
      <td>---</td>
    `;
    tbody.appendChild(tr);

    console.log("Row appended", index);
  });

  console.log("loadReservations: END");
}






// 1. Ładowanie rezerwacji po starcie strony
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOMContentLoaded – wywołuję loadReservations');
  loadReservations().catch(err => console.error('Błąd loadReservations:', err));
});

async function loadReservations() {
  const res = await fetch('/api/reservations');
  if (!res.ok) {
    console.error('Błąd przy pobieraniu rezerwacji:', res.status);
    return;
  }

  const data = await res.json();
  console.log('Odebrane rezerwacje:', data);

  const tbody = document.querySelector('#reservations-table tbody');
  if (!tbody) {
    console.error('Nie znaleziono tbody dla #reservations-table');
    return;
  }
  tbody.innerHTML = '';

  // JEŚLI tu masz dane, a po tym nadal pusto, to problem leży w CSS / HTML, nie w JS
  if (!Array.isArray(data)) {
    console.error('Oczekiwano tablicy, a przyszło:', data);
    return;
  }

  data.forEach(r => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${r.id}</td>
      <td>${r.first_name}</td>
      <td>${r.last_name}</td>
      <td>${r.date}</td>
      <td>${r.start_time}</td>
      <td>${r.end_time}</td>
      <td>${r.number_of_people}</td>
      <td>${r.status || ''}</td>
      <td>
        <button class="btn-edit" data-id="${r.id}">Edytuj</button>
        <button class="btn-delete" data-id="${r.id}">Usuń</button>
      </td>
    `;
    tbody.appendChild(tr);
  });

  console.log('Wstawiono wiersze do tabeli:', tbody.rows.length);
}

// 2. Delegacja kliknięć w tabeli (edytuj / usuń)
const table = document.querySelector('#reservations-table');
if (table) {
  table.addEventListener('click', async (e) => {
    const id = e.target.dataset.id;
    if (!id) return;

    const row = e.target.closest('tr');
    const cells = row.children;

    if (e.target.classList.contains('btn-edit')) {
      // mapowanie komórek -> formularz
      document.getElementById('edit-id').value        = id;
      document.getElementById('edit-name').value      = cells[1].textContent.trim();
      document.getElementById('edit-surname').value   = cells[2].textContent.trim();
      document.getElementById('edit-date').value      = cells[3].textContent.trim();   // tu docelowo: konwersja DD-MM-YYYY -> YYYY-MM-DD
      document.getElementById('edit-time-start').value= cells[4].textContent.trim();
      document.getElementById('edit-time-end').value  = cells[5].textContent.trim();
      document.getElementById('edit-people').value    = cells[6].textContent.trim();

      document.getElementById('edit-modal').style.display = 'block';
    }

    if (e.target.classList.contains('btn-delete')) {
      if (!confirm('Na pewno usunąć rezerwację?')) return;

      const res = await fetch(`/api/reservations/${id}`, { method: 'DELETE' });
      if (res.ok) {
        await loadReservations();
      } else {
        alert('Błąd przy usuwaniu');
      }
    }
  });
}

// 3. Obsługa wysłania formularza edycji
const editForm = document.getElementById('edit-form');
if (editForm) {
  editForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = document.getElementById('edit-id').value;
    const payload = {
      date: document.getElementById('edit-date').value,
      start_time: document.getElementById('edit-time-start').value,
      end_time: document.getElementById('edit-time-end').value,
      number_of_people: Number(document.getElementById('edit-people').value),
      // first_name / last_name realnie NIE powinny być zmieniane z panelu rezerwacji,
      // ale jeśli chcesz – musisz mieć odpowiedni endpoint w backendzie
    };

    const res = await fetch(`/api/reservations/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      document.getElementById('edit-modal').style.display = 'none';
      await loadReservations();
    } else {
      let errText = 'nieznany';
      try {
        const err = await res.json();
        errText = err.error || JSON.stringify(err);
      } catch (_) {}
      alert('Błąd: ' + errText);
    }
  });
}

async function loadReservations() {
  console.log("loadReservations: START");

  const res = await fetch('/api/reservations');
  console.log("HTTP status:", res.status);

  if (!res.ok) {
    console.error('fetch not OK');
    return;
  }

  let data;
  try {
    data = await res.json();
  } catch (e) {
    console.error("JSON parse error:", e);
    return;
  }

  console.log("DATA RECEIVED:", data);

  const tbody = document.querySelector('#reservations-table tbody');
  console.log("Tbody element found:", !!tbody);

  tbody.innerHTML = "";

  console.log("Cleared tbody.");

  if (!Array.isArray(data)) {
    console.error("Data is not array!");
    return;
  }

  console.log("Data length:", data.length);

  data.forEach((r, index) => {
    console.log("Row", index, r);

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${r.id}</td>
      <td>${r.first_name}</td>
      <td>${r.last_name}</td>
      <td>${r.date}</td>
      <td>${r.start_time}</td>
      <td>${r.end_time}</td>
      <td>${r.number_of_people}</td>
      <td>${r.status || ''}</td>
      <td>---</td>
    `;
    tbody.appendChild(tr);

    console.log("Row appended", index);
  });

  console.log("loadReservations: END");
}


//-----------------------------------------------------------------------



    //Do zrobienia:
        // 3. Logika formularza
        // 4. Rezerwowanie stolika
});