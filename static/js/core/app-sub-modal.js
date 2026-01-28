(function () {
  const parentEl = document.getElementById("appModal");
  const childEl  = document.getElementById("appSubModal");

  if (!parentEl || !childEl || !window.bootstrap) return;

  const childTitleEl = document.getElementById("appSubModalTitle");
  const childBodyEl  = document.getElementById("appSubModalBody");

  let childInstance = null;
  let restoreParentAfterClose = false;

  function getChild() {
    if (!childInstance) {
      childInstance = new bootstrap.Modal(childEl, { backdrop: true, keyboard: true });
    }
    return childInstance;
  }

  async function fetchJSON(url, options = {}) {
    const res = await fetch(url, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
      ...options
    });
    return res.json();
  }

  function setChildLoading() {
    childBodyEl.innerHTML = "<div class='p-3'>Đang tải...</div>";
  }

  async function openChild(url, opts = {}) {
    const { title = "", type = "", onClosed = null } = opts;

    // 1) Ẩn modal cha (không dispose)
    const parentInst = bootstrap.Modal.getInstance(parentEl);
    if (parentInst) {
      restoreParentAfterClose = true;
      window.AppModal?.suspendCleanup?.(true);
      parentInst.hide();
    } else {
      restoreParentAfterClose = false;
    }

    // 2) Mở modal con
    childTitleEl.textContent = title;
    setChildLoading();
    getChild().show();

    try {
      const data = await fetchJSON(url);
      if (!data.success || !data.html) {
        childBodyEl.innerHTML = "<div class='alert alert-danger m-0'>Không tải được form</div>";
        return;
      }
      childBodyEl.innerHTML = data.html;
      window.ModalHooks?.[type]?.onLoaded?.(childBodyEl);
    } catch (e) {
      childBodyEl.innerHTML = "<div class='alert alert-danger m-0'>Lỗi tải</div>";
    }

    // 3) Khi con đóng → hiện lại cha + callback refresh
    childEl.addEventListener("hidden.bs.modal", function handler() {
      childEl.removeEventListener("hidden.bs.modal", handler);

      if (restoreParentAfterClose) {
        // show lại parent sau khi child hidden xong
        window.AppModal?.suspendCleanup?.(false);
        const p = bootstrap.Modal.getInstance(parentEl);
        p?.show();
      }
      if (typeof onClosed === "function") onClosed();
    });
  }

  window.AppModalStack = { openChild };
})();
