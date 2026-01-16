document.addEventListener("DOMContentLoaded", async () => {
  const nameEl = document.getElementById("full_name");
  const dateEl = document.getElementById("reservation_date");
  const startEl = document.getElementById("start_time");
  const endEl = document.getElementById("end_time");

  if (!nameEl || !dateEl || !startEl || !endEl) return;

  try {
    const res = await fetch("/api/reservation_sent", {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" }
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || "Nie udało się pobrać danych rezerwacji");

    const fullName = `${data.first_name ?? ""} ${data.last_name ?? ""}`.trim();

    nameEl.textContent = fullName || "-";
    dateEl.textContent = data.date || "-";
    startEl.textContent = data.start_time || "-";
    endEl.textContent = data.end_time || "-";

    // jeśli chcesz też stolik, dodaj w HTML: <span id="ra-table"></span>
    const tableEl = document.getElementById("ra-table");
    if (tableEl) tableEl.textContent = data.table_id ?? "-";

  } catch (err) {
    console.error(err);
    // opcjonalnie pokaż błąd na stronie:
    const pre = document.querySelector("pre");
    if (pre) pre.textContent = err.message || String(err);
  }
});