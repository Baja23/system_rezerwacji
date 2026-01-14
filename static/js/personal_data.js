// /static/js/personal_data.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("reservation_form");
  const btn = document.getElementById("go_to_reservation"); // ustaw id na przycisku
  if (!form || !btn) return;

  btn.addEventListener("click", async (e) => {
    e.preventDefault();

    const payload = {
      first_name: form.querySelector('input[name="first_name"]')?.value?.trim(),
      last_name: form.querySelector('input[name="last_name"]')?.value?.trim(),
      email: form.querySelector('input[name="email"]')?.value?.trim(),
      phone_number: form.querySelector('input[name="phone_number"]')?.value?.trim(),
      agree_to_contact: form.querySelector('input[name="agree_to_contact"]')?.checked ?? false,
      user_type_id: 1
    };

    if (!payload.first_name || !payload.last_name || !payload.email || !payload.phone_number) {
      alert("Uzupełnij wszystkie wymagane pola.");
      return;
    }

    try {
      const res = await fetch("/api/personal_data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin", // kluczowe: sesja
        body: JSON.stringify(payload),
      });

      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        alert(data.error || "Błąd zapisu danych personalnych.");
        return;
      }

      // Flaga tylko do sensownego redirectu gdyby sesja znikła
      sessionStorage.setItem("guest_flow", "1");

      window.location.href = "/reservation";
    } catch (err) {
      console.error(err);
      alert("Błąd połączenia z serwerem.");
    }
  });
});