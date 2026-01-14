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
    if (date) params.push(`date=${date}`);
    if (firstName) params.push(`firstName=${firstName}`);
    if (lastName) params.push(`lastName=${lastName}`);
    if (startTime) params.push(`startTime=${startTime}`);
    if (endTime) params.push(`endTime=${endTime}`);
    if (status) params.push(`status=${status}`);

    if (params.length) url += "?" + params.join("&");

    const res = await fetch(url);
    const data = await res.json();

    const tbody = document.querySelector("#reservations-table tbody");
    tbody.innerHTML = "";

    // 🔥 RÓŻNICA ZALEŻNA OD STRONY
    const rows =
        pageType === "new"
            ? data.filter(r => r.status === "Awaiting confirmation")
            : data;

    rows.forEach(r => {
        const tr = document.createElement("tr");

        if (pageType === "new") {
            tr.innerHTML = `
              <td>${r.id}</td>
              <td>${r.firstName}</td>
              <td>${r.lastName}</td>
              <td>${r.date}</td>
              <td>${r.startTime}</td>
              <td>${r.endTime}</td>
              <td>${r.numberOfPeople}</td>
              <td>${r.status}</td>
              <td>
                <button class="accept-btn" data-id="${r.id}">Akceptuj</button>
                <button class="cancel-btn" data-id="${r.id}">Odrzuć</button>
              </td>
            `;
        } else {
            tr.innerHTML = `
              <td>${r.id}</td>
              <td>${r.restaurantTableId}</td>
              <td>${r.firstName}</td>
              <td>${r.lastName}</td>
              <td>${r.date}</td>
              <td>${r.startTime}</td>
              <td>${r.endTime}</td>
              <td>${r.numberOfPeople}</td>
              <td>${r.status}</td>
              <td>
                <button class="edit-btn" data-id="${r.id}">Edytuj</button>
                <button class="cancel-btn" data-id="${r.id}">Anuluj</button>
              </td>
            `;
        }

        tbody.appendChild(tr);
    });
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

document.addEventListener("click", async (e) => {
    const id = e.target.dataset.id;
    if (!id) return;

    // NOWE REZERWACJE
    if (pageType === "new") {
        if (e.target.classList.contains("accept-btn")) {
            await updateStatus(id, "Accepted");
            loadReservations();
        }
        if (e.target.classList.contains("cancel-btn")) {
            if (!confirm("Odrzucić rezerwację?")) return;
            await updateStatus(id, "Cancelled");
            loadReservations();
        }
    }

    // BIEŻĄCE REZERWACJE
    if (pageType === "current") {
        if (e.target.classList.contains("edit-btn")) {
            openEditModal(id);
        }
        if (e.target.classList.contains("cancel-btn")) {
            if (!confirm("Anulować rezerwację?")) return;
            await updateStatus(id, "Cancelled");
            loadReservations();
        }
    }
});