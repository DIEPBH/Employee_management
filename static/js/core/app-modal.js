// static/js/core/app-modal.js
(function () {
  const modalEl = document.getElementById("appModal");
  const titleEl = document.getElementById("appModalTitle");
  const bodyEl  = document.getElementById("appModalBody");

  if (!modalEl || !window.bootstrap) return;

  let instance = null;
  let currentType = null;
  let suspendReset = false;

  function getInstance() {
    if (!instance) {
      instance = new bootstrap.Modal(modalEl, {
        backdrop: true,
        keyboard: true
      });
    }
    return instance;
  }

  function setLoading() {
    bodyEl.innerHTML = "<div class='p-3'>Đang tải...</div>";
  }

  async function fetchJSON(url, options = {}) {
    const res = await fetch(url, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
      ...options
    });
    return res.json();
  }

  async function open(url, opts = {}) {
    const { title = "", type = null } = opts;
    currentType = type;

    titleEl.textContent = title;
    setLoading();
    getInstance().show();

    try {
      const data = await fetchJSON(url);

      if (!data.success || !data.html) {
        bodyEl.innerHTML = "<div class='alert alert-danger'>Không tải được form</div>";
        return;
      }

      bodyEl.innerHTML = data.html;
      window.ModalHooks?.[type]?.onLoaded?.(bodyEl);

    } catch {
      bodyEl.innerHTML = "<div class='alert alert-danger'>Lỗi tải dữ liệu</div>";
    }
  }

  function close() {
    getInstance().hide();
  }

  function suspendCleanup(v = true) {
    suspendReset = v;
  }

  modalEl.addEventListener("hidden.bs.modal", () => {
    if (suspendReset) return;
    bodyEl.innerHTML = "<div class='p-3'>Đang tải...</div>";
    titleEl.textContent = "";
    currentType = null;
  });

  window.AppModal = { open, close, suspendCleanup };
})();
