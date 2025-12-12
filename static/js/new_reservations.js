console.log("new_reservations.js loaded");

document.addEventListener("DOMContentLoaded", () => {
    loadNewReservations();

    const filterBtn = document.getElementById("apply-filters");
    if (filterBtn) {
        filterBtn.addEventListener("click", e => {
            e.preventDefault();
            loadNewReservations();
        });
    }
});

async function loadNewReservations() {
    let url = "/api/reservations";
    const params = [];

    const dateInput = document.getElementById("filter-date")?.value;
    if (dateInput) {
        const [y, m, d] = dateInput.split("-");
        params.push(`date=${d}-${m}-${y}`);
    }

    const firstName = document.getElementById("filter-firstName")?.value;
    if (firstName) params.push(`firstName=${encodeURIComponent(firstName)}`);

    if (params.length) url += "?" + params.join("&");

    const res = await fetch(url);
    if (!res.ok) {
        console.error("Fetch error");
        return;
    }

    const data = await res.json();
    const tbody = document.querySelector("#reservations-table tbody");
    tbody.innerHTML = "";

    data
        .filter(r => r.status === "Awaiting confirmation")
        .forEach(r => {
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
                <td>
                    <button class="accept-btn" data-id="${r.id}">Akceptuj</button>
                    <button class="cancel-btn" data-id="${r.id}">Odrzuć</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
}

// === AKCEPTUJ / ODRZUĆ ===
document.addEventListener("click", async e => {
    const id = e.target.dataset.id;
    if (!id) return;

    // AKCEPTUJ
    if (e.target.classList.contains("accept-btn")) {
        await fetch(`/api/reservations/${id}/status`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: "Accepted" })
        });

        loadNewReservations();
    }

    // ODRZUĆ
    if (e.target.classList.contains("cancel-btn")) {
        if (!confirm("Odrzucić rezerwację?")) return;

        await fetch(`/api/reservations/${id}/status`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: "Cancelled" })
        });

        loadNewReservations();
    }
});
