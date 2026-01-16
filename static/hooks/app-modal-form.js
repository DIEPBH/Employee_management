// static/js/hooks/app-modal-form.js
document.addEventListener("submit", async (e) => {
  const form = e.target.closest("#appModal form[data-ajax='1']");
  if (!form) return;

  e.preventDefault();

  const url  = form.action || location.href;
  const type = form.dataset.modalType;
  const formData = new FormData(form);

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest" },
      body: formData
    });

    const data = await res.json();

    if (data.success) {
      window.ModalHooks?.[type]?.onSuccess?.(data);
      AppModal.close();
      location.reload();
      return;
    }

    // submit lỗi → render lại form
    if (data.html) {
      document.getElementById("appModalBody").innerHTML = data.html;
      window.ModalHooks?.[type]?.onLoaded?.(
        document.getElementById("appModalBody")
      );
    }

  } catch {
    document.getElementById("appModalBody").innerHTML =
      "<div class='alert alert-danger'>Lỗi submit</div>";
  }
});
