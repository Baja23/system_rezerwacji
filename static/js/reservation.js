document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("reservation_form");
  const findBtn = document.getElementById("tableID-button");
  if (!form || !findBtn) return;

  findBtn.addEventListener("click", findTables);
  form.addEventListener("submit", finalizeReservation);
});

function ymdToDmy(ymd) {
  if (!ymd || !/^\d{4}-\d{2}-\d{2}$/.test(ymd)) return ymd;
  const [y, m, d] = ymd.split("-");
  return `${d}/${m}/${y}`;
}

function getSearchPayload() {
  const dateRaw = document.getElementById("date")?.value;
  const start_time = document.getElementById("startTime")?.value;
  const end_time = document.getElementById("endTime")?.value;
  const number_of_people = document.getElementById("number_of_people")?.value;

  if (!dateRaw || !start_time || !end_time || !number_of_people) return null;

  return {
    date: ymdToDmy(dateRaw),
    start_time,
    end_time,
    number_of_people: Number(number_of_people),
  };
}

async function findTables() {
  const payload = getSearchPayload();
  if (!payload) {
    alert("Uzupełnij datę, godziny i liczbę osób.");
    return;
  }

  const res = await fetch("/api/reservation", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify(payload),
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    alert(data.error || "Nie udało się wyszukać stolików.");
    return;
  }

  // UWAGA: backend aktualnie NIE zwraca listy stolików (zwraca tylko tekst)
  // więc żeby tabela się wypełniła, backend musi zwrócić np. {available_tables:[...]}.
  renderTables(data.available_tables || []);
}

function renderTables(tables) {
  const tbody = document.querySelector("#table-id-selection tbody");
  tbody.innerHTML = "";

  if (!tables.length) {
    tbody.innerHTML = `<tr><td colspan="2">Brak wolnych stolików</td></tr>`;
    return;
  }

  for (const table of tables) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${table.name ?? "Stolik"}</td><td>${table.id}</td>`;
    tr.addEventListener("click", () => {
      document.getElementById("tableID").value = table.id;
    });
    tbody.appendChild(tr);
  }
}

async function finalizeReservation(e) {
  e.preventDefault();

  const accept_rules = document.getElementById("accept_rules")?.checked ?? false;
  const tableID = document.getElementById("tableID")?.value;

  if (!accept_rules) {
    alert("Musisz zaakceptować regulamin.");
    return;
  }
  if (!tableID) {
    alert("Wybierz numer stolika.");
    return;
  }

  const res = await fetch("/api/get_table", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ id: Number(tableID) }),
  });

  const data = await res.json().catch(() => ({}));

  if (res.ok) {
    window.location.href = data.redirect_url || "/reservation_sent";
    return;
  }

  alert(data.error || "Błąd rezerwacji.");
  window.location.href = data.redirect_url || "/reservation_fail";
}