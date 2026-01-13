(() => {
  const form = document.getElementById('register_form');
  if (!form) return; // ten plik nie jest dla tej strony

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    try {
      const fd = new FormData(form);

      // 1) gość
      const guest = {
        first_name: fd.get('first_name'),
        last_name: fd.get('last_name'),
        email: fd.get('email'),
        phone_number: fd.get('phone_number'),
        user_type_id: 1, // jeśli backend tego wymaga
      };

      const r1 = await fetch('/api/guest_reservation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify(guest),
      });

      const j1 = await r1.json().catch(() => ({}));
      if (!r1.ok) throw new Error(j1.error || 'Błąd danych gościa');

      // 2) rezerwacja
      const reservation = {
        date: fd.get('date'),
        start_time: fd.get('start_time'),
        end_time: fd.get('end_time'),
        number_of_people: Number(fd.get('number_of_people')),
      };

      const r2 = await fetch('/api/reservation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify(reservation),
      });

      const j2 = await r2.json().catch(() => ({}));
      if (!r2.ok) throw new Error(j2.error || 'Błąd rezerwacji');

      // 3) dopiero teraz redirect
      window.location.assign('/reservation_sent');

    } catch (err) {
      alert(err.message || String(err));
    }
  });
})();