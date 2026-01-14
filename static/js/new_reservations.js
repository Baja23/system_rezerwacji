console.log("new_reservations.js loaded");

let pendingCancelId = null;

document.addEventListener("DOMContentLoaded", () => {
  loadNewReservations();

  document.getElementById("apply-filters")?.addEventListener("click", (e) => {
    e.preventDefault();
    loadNewReservations();
  });

  // modal anulowania (masz go w HTML)
  document.getElementById("close-modal")?.addEventListener("click", () => {
    hideCancelModal();
  });

  document.getElementById("cancel-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!pendingCancelId) return;

    const ok = await updateStatus(pendingCancelId, "Cancelled");
    hideCancelModal();

    if (ok) loadNewReservations();
  });
});

async function loadNewReservations() {
  let url = "/api/reservations";
  const params = [];

  const dateInput = document.getElementById("filter-date")?.value;
  if (dateInput) {
    const [y, m, d] = dateInput.split("-");
    params.push(`date=${encodeURIComponent(`${d}-${m}-${y}`)}`);
  }

  const firstName = document.getElementById("filter-firstName")?.value?.trim();
  if (firstName) params.push(`firstName=${encodeURIComponent(firstName)}`);

  const lastName = document.getElementById("filter-lastName")?.value?.trim();
  if (lastName) params.push(`lastName=${encodeURIComponent(lastName)}`);

  const startTime = document.getElementById("filter-startTime")?.value;
  if (startTime) params.push(`startTime=${encodeURIComponent(startTime)}`);

  const endTime = document.getElementById("filter-endTime")?.value;
  if (endTime) params.push(`endTime=${encodeURIComponent(endTime)}`);

  const status = document.getElementById("filter-status")?.value;
  if (status) params.push(`status=${encodeURIComponent(status)}`);

  if (params.length) url += "?" + params.join("&");

  const res = await fetch(url, { credentials: "same-origin" });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    alert(data.error || `Błąd pobierania (HTTP ${res.status})`);
    return;
  }

  const data = await res.json();
  const tbody = document.querySelector("#reservations-table tbody");
  if (!tbody) return;

  tbody.innerHTML = "";

  (Array.isArray(data) ? data : [])
    .filter((r) => r.status === "Awaiting confirmation")
    .forEach((r) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${r.id}</td>
        <td>${r.firstName ?? ""}</td>
        <td>${r.lastName ?? ""}</td>
        <td>${r.date ?? ""}</td>
        <td>${r.startTime ?? ""}</td>
        <td>${r.endTime ?? ""}</td>
        <td>${r.numberOfPeople ?? ""}</td>
        <td>${r.status ?? ""}</td>
        <td>
          <button type="button" class="accept-btn" data-id="${r.id}">Akceptuj</button>
          <button type="button" class="cancel-btn" data-id="${r.id}">Odrzuć</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
}

// === AKCEPTUJ / ODRZUĆ ===
document.addEventListener("click", async (e) => {
  const btn = e.target;
  const id = btn?.dataset?.id;
  if (!id) return;

  if (btn.classList.contains("accept-btn")) {
    const ok = await updateStatus(id, "Accepted");
    if (ok) loadNewReservations();
    return;
  }

  if (btn.classList.contains("cancel-btn")) {
    pendingCancelId = id;
    showCancelModal();
    return;
  }
});

async function updateStatus(id, status) {
  const res = await fetch(`/api/reservations/${id}/status`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ status }),
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    alert(data.error || `Błąd zmiany statusu (HTTP ${res.status})`);
    return false;
  }
  return true;
}

function showCancelModal() {
  const modal = document.getElementById("cancel-modal");
  if (modal) modal.style.display = "block";
}

function hideCancelModal() {
  pendingCancelId = null;
  const modal = document.getElementById("cancel-modal");
  if (modal) modal.style.display = "none";
}