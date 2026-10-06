"use strict";
document.querySelectorAll("[data-quantity-step]").forEach((button) => {
  button.addEventListener("click", () => {
    const input = button.closest(".quantity-control").querySelector("input");
    const current = Number.parseInt(input.value, 10) || 1;
    const minimum = Number.parseInt(input.min, 10) || 1;
    const maximum = Number.parseInt(input.max, 10) || 999;
    input.value = Math.max(minimum, Math.min(maximum, current + Number(button.dataset.quantityStep)));
    input.dispatchEvent(new Event("change", { bubbles: true }));
  });
});
document.querySelectorAll("[data-auto-submit]").forEach((select) => {
  select.addEventListener("change", () => select.form.requestSubmit());
});
// Prevent accidental double clicks; the server also enforces checkout idempotency.
document.querySelectorAll("form").forEach((form) => {
  form.addEventListener("submit", () => {
    if (!form.checkValidity()) return;
    const button = form.querySelector('button[type="submit"]');
    if (button) {
      window.setTimeout(() => { button.disabled = true; }, 0);
      window.setTimeout(() => { button.disabled = false; }, 5000);
    }
  });
});
