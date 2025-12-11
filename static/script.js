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
    const reservationButton = document.getElementById('reservation_form_button');
    const reservationContainer = document.getElementById('reservation_container');
    const reservationForm = document.getElementById('reservation_form');

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

    // Przycisk logowania
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
                    if (loggedInUserContainer) {
                        loggedInUserContainer.style.display = 'block';
                    }
                    if (loginContainer) {
                        loginContainer.style.display = 'none';
                    }
                } else {
                    console.error('Login failed:' + result.error);
                    alert('error: Invalid username or password');
                }
            } catch (error) {
                console.error('Network error:', error);
                alert('Could not connect to the server.');
            }
        });
    }

    // ====== REZERWACJE + FILTRY ======

    const filterBtn = document.getElementById("apply-filters");
    if (filterBtn) {
        filterBtn.addEventListener("click", (e) => {
            e.preventDefault();
            console.log("Filtr kliknięty – odświeżam listę");
            loadReservations();
        });
    }

    if (document.querySelector("#reservations-table tbody")) {
        console.log("Znaleziono tabelę rezerwacji – ładuję dane startowe");
        loadReservations().catch(err => console.error("loadReservations error:", err));
    }

    console.log("End of DOMContentLoaded handler.");
});

// Funkcja ładująca rezerwacje
async function loadReservations() {
    console.log("loadReservations: START");

    const dateInput = document.getElementById("filter-date")?.value;
    const firstName = document.getElementById("filter-firstName")?.value;
    const lastName = document.getElementById("filter-lastName")?.value;
    const startTime = document.getElementById("filter-startTime")?.value;
    const endTime = document.getElementById("filter-endTime")?.value;
    const status = document.getElementById("filter-status")?.value;

    let date = null;
    if (dateInput) {
        const [y, m, d] = dateInput.split("-");
        date = `${d}-${m}-${y}`;
    }

    let url = "/api/reservations";
    const params = [];
    if (date) params.push(`date=${encodeURIComponent(date)}`);
    if (firstName) params.push(`firstName=${encodeURIComponent(firstName)}`);
    if (lastName) params.push(`lastName=${encodeURIComponent(lastName)}`);
    if (startTime) params.push(`startTime=${encodeURIComponent(startTime)}`);
    if (endTime) params.push(`endTime=${encodeURIComponent(endTime)}`);
    if (status) params.push(`status=${encodeURIComponent(status)}`);

    if (params.length > 0) {
        url += "?" + params.join("&");
    }

    console.log("FETCH URL =", url);

    let res;
    try {
        res = await fetch(url);
    } catch (e) {
        console.error("Błąd fetch:", e);
        return;
    }

    console.log("HTTP status:", res.status);

    if (!res.ok) {
        console.error("fetch not OK");
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

    const tbody = document.querySelector("#reservations-table tbody");
    if (!tbody) {
        console.error("Nie znaleziono tbody");
        return;
    }

    tbody.innerHTML = "";
    if (!Array.isArray(data)) {
        console.error("Data nie jest tablicą");
        return;
    }

    console.log("Data length:", data.length);

    data.forEach((r, index) => {
        console.log("Row", index, r);

        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${r.id}</td>
          <td>${r.firstName}</td>
          <td>${r.lastName}</td>
          <td>${r.date}</td>
          <td>${r.startTime}</td>
          <td>${r.endTime}</td>
          <td>${r.numberOfPeople}</td>
          <td>${r.status}</td>
          <td class="actions-cell">
            <button class="action-btn edit-btn" data-id="${r.id}">Edytuj</button>
            <button class="action-btn cancel-btn" data-id="${r.id}">Anuluj</button>
          </td>
        `;
        tbody.appendChild(tr);

        console.log("Row appended", index);
    });

    console.log("loadReservations: END");
}

function convertDate(dateStr) {
    // zamienia 20-12-2025 → 2025-12-20 (format input[type=date])
    const [d, m, y] = dateStr.split("-");
    return `${y}-${m}-${d}`;
}

document.querySelector("#reservations-table").addEventListener("click", (e) => {
    if (e.target.classList.contains("edit-btn")) {

        const row = e.target.closest("tr").children;

        document.getElementById("edit-date").value = convertDate(row[3].textContent);
        document.getElementById("edit-time-start").value = row[4].textContent;
        document.getElementById("edit-time-end").value = row[5].textContent;
        document.getElementById("edit-people").value = row[6].textContent;

        document.getElementById("edit-modal").style.display = "block";
    }
});

document.getElementById("close-modal").addEventListener("click", () => {
    document.getElementById("edit-modal").style.display = "none";
});

document.getElementById("edit-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = document.getElementById("edit-id").value;

    const payload = {
        date: document.getElementById("edit-date").value,
        startTime: document.getElementById("edit-time-start").value,
        endTime: document.getElementById("edit-time-end").value,
        numberOfPeople: document.getElementById("edit-people").value
    };

    const res = await fetch(`/api/reservations/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        alert("Zapisano zmiany!");
        document.getElementById("edit-modal").style.display = "none";
        loadReservations(); // odśwież tabelę
    } else {
        alert("Błąd podczas zapisywania");
    }
});