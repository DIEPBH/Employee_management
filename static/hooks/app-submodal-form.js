// static/js/hooks/app-submodal-form.js
document.addEventListener("submit", async (e) => {
  const form = e.target.closest("#appSubModal form[data-ajax='1']");
  if (!form) return;

  e.preventDefault();

  const url  = form.action || location.href;
  const type = form.dataset.modalType || "";
  const body = document.getElementById("appSubModalBody");
  const formData = new FormData(form);

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest" },
      body: formData
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    
    if (data.success) {
      // gọi hook thành công
      window.ModalHooks?.[type]?.onSuccess?.(data);

      // đóng sub modal
      bootstrap.Modal
        .getInstance(document.getElementById("appSubModal"))
        ?.hide();

      return;
    }

    // submit lỗi → render lại form vào SUB MODAL
    if (data.html) {
      body.innerHTML = data.html;
      window.ModalHooks?.[type]?.onLoaded?.(body);
      return;
    }

    body.innerHTML = "<div class='alert alert-danger'>Submit không thành công</div>";

  } catch (err) {
    body.innerHTML = "<div class='alert alert-danger'>Lỗi submit</div>";
    console.error("Submodal submit error:", err);
  }
});