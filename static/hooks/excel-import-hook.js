// static/js/hooks/excel-import-hook.js
(function () {
  function qs(sel, root) { return (root || document).querySelector(sel); }

  function renderErrors(errors, limit = 50) {
    if (!Array.isArray(errors) || errors.length === 0) return "";
    const items = errors.slice(0, limit).map(e => {
      const row = e?.row ?? "?";
      const err = e?.error ?? "Lỗi không xác định";
      return `<li>Dòng ${row}: ${err}</li>`;
    }).join("");
    const more = errors.length > limit
      ? `<div class="small text-muted">...và ${errors.length - limit} lỗi khác</div>`
      : "";
    return `
      <div class="alert alert-warning mt-2">
        <div><b>Các dòng lỗi:</b></div>
        <ul class="mb-1">${items}</ul>
        ${more}
      </div>
    `;
  }

  async function postForm(form) {
    const url = form.getAttribute("action");
    const fd = new FormData(form);

    const res = await fetch(url, {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest" },
      body: fd
    });

    const ct = (res.headers.get("content-type") || "").toLowerCase();
    if (!ct.includes("application/json")) {
      const text = await res.text();
      throw new Error("Server không trả JSON. Kiểm tra view import. " + text.slice(0, 180));
    }
    return res.json();
  }

  function bindExcelImport(bodyEl, opts = {}) {
    const root = bodyEl || document;

    // Template chung của bạn nên có 1 form upload.
    // Khuyến nghị: thêm class js-excel-import-form trong template để bắt chắc.
    const form =
      qs("form.js-excel-import-form", root) ||
      qs("#excelImportForm", root) ||
      qs("form", root);

    if (!form) return;

    // tránh bind nhiều lần khi re-render
    if (form.dataset.bound === "1") return;
    form.dataset.bound = "1";

    const resultEl =
      qs(".js-import-result", root) ||
      qs("#importResult", root);

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      if (resultEl) {
        resultEl.innerHTML = `<div class="alert alert-info">Đang import...</div>`;
      }

      try {
        const data = await postForm(form);

        // Case: form invalid => server trả {success:false, html:"..."}
        if (data.success === false && data.html) {
          root.innerHTML = data.html;
          // bind lại trên HTML mới
          bindExcelImport(root, opts);
          return;
        }

        if (data.success) {
          const msg = data.message || `Import xong: ${data.imported || 0} thành công, ${data.failed || 0} lỗi.`;
          const html =
            `<div class="alert alert-success">${msg}</div>` +
            renderErrors(data.errors);

          if (resultEl) resultEl.innerHTML = html;

          // gọi reload theo app của bạn (tùy chọn)
          if (typeof window.reloadCurrentTable === "function") window.reloadCurrentTable();
          else if (typeof window.loadTitles === "function") window.loadTitles(1);

          if (typeof opts.onDone === "function") opts.onDone(data);
        } else {
          if (resultEl) {
            resultEl.innerHTML = `<div class="alert alert-danger">${data.message || "Import thất bại"}</div>`;
          }
        }
      } catch (err) {
        if (resultEl) {
          resultEl.innerHTML = `<div class="alert alert-danger">Lỗi: ${err.message || err}</div>`;
        }
      }
    });
  }

  // ==== Hook entry point theo cơ chế AppModal ====
  window.ModalHooks = window.ModalHooks || {};

  // Hook chung (dùng cho mọi import)
  function excelImportHook(ctx = {}) {
    // AppModal.open của bạn nên truyền bodyEl vào ctx.
    // Nếu chưa có ctx.bodyEl thì hook vẫn fallback được.
    const bodyEl = ctx.bodyEl || document.getElementById("appModalBody") || document;
    bindExcelImport(bodyEl);
  }

  // Alias: mọi type import bạn khai báo sẽ trỏ về hook chung
  // Với case hiện tại:
  ModalHooks["emp_title_import"] = excelImportHook;

  // Sau này thêm các import khác chỉ cần thêm vào đây:
  // ModalHooks["emp_position_import"] = excelImportHook;
  // ModalHooks["emp_reward_import"] = excelImportHook;
})();
