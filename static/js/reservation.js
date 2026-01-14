// /static/js/reservation.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("reservation_form");
  if (!form) return;

  // jeśli w buttonie jest <a href="...">, to potrafi ominąć submit
  const btn = document.getElementById("reservation_button");
  const a = btn?.querySelector("a");
  if (a) a.addEventListener("click", (e) => e.preventDefault());

  form.addEventListener("submit", submitReservation);
});

function ymdToDmy(ymd) {
  // input type="date" => YYYY-MM-DD, a u Ciebie backend często oczekuje DD/MM/YYYY
  if (!ymd || !/^\d{4}-\d{2}-\d{2}$/.test(ymd)) return ymd;
  const [y, m, d] = ymd.split("-");
  return `${d}/${m}/${y}`;
}

async function submitReservation(e) {
  e.preventDefault();

  const dateRaw = document.getElementById("date")?.value;
  const start_time = document.getElementById("startTime")?.value;
  const end_time = document.getElementById("endTime")?.value;
  const number_of_people = document.getElementById("number_of_people")?.value;
  const accept_rules = document.getElementById("accept_rules")?.checked ?? false;

  if (!dateRaw || !start_time || !end_time || !number_of_people) {
    alert("Uzupełnij datę, godziny i liczbę osób.");
    return;
  }
  if (!accept_rules) {
    alert("Musisz zaakceptować regulamin.");
    return;
  }

  try {
    const res = await fetch("/api/reservation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin", // kluczowe: sesja
      body: JSON.stringify({
        date: ymdToDmy(dateRaw),
        start_time,
        end_time,
        number_of_people: Number(number_of_people),
        accept_rules
      }),
    });

    const data = await res.json().catch(() => ({}));

    if (res.ok) {
      sessionStorage.removeItem("guest_flow");
      window.location.href = "/reservation_sent";
      return;
    }

    // jeśli backend mówi "brak usera w sesji" (401/403), to kierunek zależy od flow
    if (res.status === 401 || res.status === 403) {
      const isGuest = sessionStorage.getItem("guest_flow") === "1";
      alert(data.error || "Brak użytkownika w sesji.");
      window.location.href = isGuest ? "/personal_data" : "/login";
      return;
    }

    alert(data.error || "Błąd rezerwacji.");
    window.location.href = "/reservation_fail";
  } catch (err) {
    console.error(err);
    alert("Błąd połączenia z serwerem.");
  }
}