document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("logout_button");
  if (!btn) return;

  btn.addEventListener("click", (e) => {
    e.preventDefault();
    window.location.href = "/logout_button";
  });
});