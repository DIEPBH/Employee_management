// static/js/hooks/app-modal-hook.js
document.addEventListener("click", (e) => {
  const btn = e.target.closest(".js-open-modal");
  if (!btn) return;

  e.preventDefault();

  AppModal.open(btn.dataset.modalUrl, {
    title: btn.dataset.modalTitle || "",
    type:  btn.dataset.modalType || null,
    size:  btn.dataset.modalSize || "xl"
  });
});
