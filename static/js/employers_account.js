
console.log("current_reservations.js loaded");
document.addEventListener("DOMContentLoaded", () => {
    loadCurrentReservations();

    const filterBtn = document.getElementById("apply-filters");
    if (filterBtn) {
        filterBtn.addEventListener("click", (e) => {
            e.preventDefault();
            loadCurrentReservations();
        });
    }
});


// LOAD RESERVATIONS

async function loadCurrentReservations() {
    let url = "/api/reservations";
    const params = [];

    const dateInput = document.getElementById("filter-date")?.value;
    const firstName = document.getElementById("filter-firstName")?.value;
    const lastName = document.getElementById("filter-lastName")?.value;
    const startTime = document.getElementById("filter-startTime")?.value;
    const endTime = document.getElementById("filter-endTime")?.value;
    const status = document.getElementById("filter-status")?.value;

    if (dateInput) {
        const [y, m, d] = dateInput.split("-");
        params.push(`date=${d}-${m}-${y}`);
    }
    if (firstName) params.push(`firstName=${encodeURIComponent(firstName)}`);
    if (lastName) params.push(`lastName=${encodeURIComponent(lastName)}`);
    if (startTime) params.push(`startTime=${encodeURIComponent(startTime)}`);
    if (endTime) params.push(`endTime=${encodeURIComponent(endTime)}`);
    if (status) params.push(`status=${encodeURIComponent(status)}`);

    if (params.length) {
        url += "?" + params.join("&");
    }

    const res = await fetch(url);
    if (!res.ok) {
        console.error("Błąd pobierania rezerwacji");
        return;
    }

    const data = await res.json();
    const tbody = document.querySelector("#reservations-table tbody");
    tbody.innerHTML = "";

    data.forEach(r => {
        const tr = document.createElement("tr");
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
        tbody.appendChild(tr);
    });
}


// DATE CONVERTER

function convertDate(dateStr) {
    const [d, m, y] = dateStr.split("-");
    return `${y}-${m}-${d}`;
}


// TABLE CLICK HANDLER

document.addEventListener("click", async (e) => {
    const id = e.target.dataset.id;
    if (!id) return;

    // === EDIT ===
    if (e.target.classList.contains("edit-btn")) {
        const row = e.target.closest("tr").children;

        document.getElementById("edit-id").value = id;
        document.getElementById("edit-date").value = convertDate(row[4].textContent);
        document.getElementById("edit-time-start").value = row[5].textContent;
        document.getElementById("edit-time-end").value = row[6].textContent;
        document.getElementById("edit-people").value = row[7].textContent;

        document.getElementById("edit-modal").style.display = "block";
    }

    // === CANCEL ===
    if (e.target.classList.contains("cancel-btn")) {
        const confirmed = confirm("Czy na pewno anulować rezerwację?");
        if (!confirmed) return;

        const res = await fetch(`/api/reservations/${id}/status`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: "Cancelled" })
        });

        if (res.ok) {
            loadCurrentReservations();
        } else {
            alert("Błąd anulowania");
        }
    }
});


// MODAL CLOSE

document.getElementById("close-modal")?.addEventListener("click", () => {
    document.getElementById("edit-modal").style.display = "none";
});


// SAVE EDIT

document.getElementById("edit-form")?.addEventListener("submit", async (e) => {
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
        alert("Zapisano zmiany");
        document.getElementById("edit-modal").style.display = "none";
        loadCurrentReservations();
    } else {
        alert("Błąd zapisu");
    }
});