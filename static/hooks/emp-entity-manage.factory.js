// static/js/hooks/emp-entity-manage.factory.js
// Chuẩn hoá theo core:
// - Modal cha: AppModal.open(...) gọi ModalHooks[type].onLoaded(body)
// - Modal con: AppModalStack.openChild(url,{title,type,onClosed}) -> ẩn cha, mở con, đóng con thì show lại cha và gọi onClosed

(function () {
  function defaultGetCSRFToken() {
    return (
      document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
      document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        ?.split("=")[1]
    );
  }

  async function fetchJSON(url, options = {}) {
    const res = await fetch(url, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
      ...options,
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  /**
   * Factory tạo hook manage theo cán bộ
   */
  window.createEmpEntityManageHook = function createEmpEntityManageHook(cfg) {
    const {
      // selectors trong modal body (modal cha)
      empInputSel = "#empCode",
      empSuggestSel = "#empSuggest",
      empNameSel = "#empName",
      tableWrapSel = "#empTableWrap",
      btnAddSel = ".js-add",

      // table actions
      pageLinkSel = ".js-page",
      deleteBtnSel = ".js-delete",
      openChildSel = "[data-open-child]",

      // urls
      listUrl, // (empNum, page) => url trả {success, html}
      addUrl,  // (empNum) => url add form

      // modal child defaults
      childTypeDefault = "child_form",
      childTitleDefault = "Chi tiết",
      addTitleDefault = "Thêm mới",

      // callbacks
      onParentClosed,

      // helpers
      getCSRFToken = defaultGetCSRFToken,
      notifyError = (m) => alert(m),
      confirmDeleteText = "Bạn có chắc chắn muốn xoá bản ghi này?",
    } = cfg;

    if (typeof listUrl !== "function" || typeof addUrl !== "function") {
      throw new Error("createEmpEntityManageHook: listUrl/addUrl is required");
    }

    return {
      onLoaded(modalBody) {
        // Abort để tránh leak listener khi reopen modal
        if (modalBody.__empEntityAbortCtrl) modalBody.__empEntityAbortCtrl.abort();
        const ac = new AbortController();
        modalBody.__empEntityAbortCtrl = ac;

        const inp = modalBody.querySelector(empInputSel);
        const suggestBox = modalBody.querySelector(empSuggestSel);
        const name = modalBody.querySelector(empNameSel);
        const wrap = modalBody.querySelector(tableWrapSel);
        const btnAdd = modalBody.querySelector(btnAddSel);

        if (!inp || !suggestBox || !name || !wrap || !btnAdd) return;

        let currentEmpNum = null;
        let currentPage = 1;

        function resetUI(msg = "Vui lòng nhập mã cán bộ để tra cứu.") {
          currentEmpNum = null;
          currentPage = 1;
          name.value = "";
          btnAdd.disabled = true;
          wrap.innerHTML = `<div class="text-muted">${msg}</div>`;
          inp.classList.remove("is-valid", "is-invalid");
        }

        function setInvalid(msg = "Mã cán bộ không hợp lệ hoặc không tồn tại.") {
          currentEmpNum = null;
          currentPage = 1;
          name.value = "";
          btnAdd.disabled = true;
          wrap.innerHTML = `<div class="text-muted">${msg}</div>`;
          inp.classList.remove("is-valid");
          inp.classList.add("is-invalid");
        }

        async function loadList(page = 1) {
          if (!currentEmpNum) return;

          const p = parseInt(page, 10);
          currentPage = Number.isFinite(p) && p >= 1 ? p : 1;

          try {
            const url = listUrl(currentEmpNum, currentPage);
            const data = await fetchJSON(url, { signal: ac.signal });
            wrap.innerHTML = data.html || `<div class="text-muted">Chưa có dữ liệu.</div>`;
          } catch (err) {
            if (err?.name === "AbortError") return;
            console.error("loadList error:", err);
            wrap.innerHTML = `<div class="text-danger">Lỗi tải dữ liệu</div>`;
          }
        }

        // init
        resetUI();

        // lookup (dùng bindEmployeeLookup hiện có)
        bindEmployeeLookup({
          input: inp,
          suggestBox,
          onSelect(emp) {
            currentEmpNum = emp.code;
            currentPage = 1;

            name.value = emp.name;
            btnAdd.disabled = false;

            inp.classList.remove("is-invalid");
            inp.classList.add("is-valid");

            loadList(1);
          },
        });

        // Click delegation: phân trang / mở modal con / xóa
        modalBody.addEventListener(
          "click",
          async (e) => {
            // Pagination
            const a = e.target.closest(pageLinkSel);
            if (a) {
              e.preventDefault();
              loadList(a.dataset.page || 1);
              return;
            }

            // Delete
            const delBtn = e.target.closest(deleteBtnSel);
            if (delBtn) {
              e.preventDefault();
              e.stopPropagation(); // tránh click bubble lên openChild

              const ok = confirm(confirmDeleteText);
              if (!ok) return;

              try {
                const res = await fetch(delBtn.dataset.url, {
                  method: "POST",
                  headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": getCSRFToken(),
                  },
                  signal: ac.signal,
                });

                if (!res.ok) throw new Error(`HTTP ${res.status}`);

                const data = await res.json();
                if (data.success) loadList(currentPage);
                else notifyError("Không thể xoá bản ghi");
              } catch (err) {
                if (err?.name === "AbortError") return;
                console.error(err);
                notifyError("Lỗi khi xoá");
              }
              return;
            }

            // Open child modal (edit/view) - khớp core AppModalStack
            const btn = e.target.closest(openChildSel);
            if (!btn) return;

            AppModalStack.openChild(btn.dataset.url, {
              title: btn.dataset.title || childTitleDefault,
              type: btn.dataset.type || childTypeDefault,
              onClosed: () => loadList(currentPage),
            });
          },
          { signal: ac.signal }
        );

        // Input change/reset logic
        inp.addEventListener(
          "input",
          () => {
            const v = inp.value.trim();
            if (!v) {
              resetUI();
              return;
            }

            inp.classList.remove("is-invalid");

            // đã chọn rồi mà sửa khác -> khoá nút + clear tên
            if (currentEmpNum && v !== currentEmpNum) {
              currentEmpNum = null;
              currentPage = 1;
              name.value = "";
              btnAdd.disabled = true;
              wrap.innerHTML = `<div class="text-muted">Hãy chọn đúng mã trong danh sách gợi ý.</div>`;
              inp.classList.remove("is-valid");
            }
          },
          { signal: ac.signal }
        );

        // blur mà chưa select đúng -> invalid
        inp.addEventListener(
          "blur",
          () => {
            const v = inp.value.trim();
            if (!v) return;
            if (!currentEmpNum) setInvalid();
          },
          { signal: ac.signal }
        );

        // Add (modal con)
        btnAdd.addEventListener(
          "click",
          () => {
            if (!currentEmpNum) return;

            AppModalStack.openChild(addUrl(currentEmpNum), {
              title: btnAdd.dataset.title || addTitleDefault,
              type: btnAdd.dataset.type || childTypeDefault,
              onClosed: () => loadList(currentPage),
            });
          },
          { signal: ac.signal }
        );

        // Parent closed action (tuỳ bạn)
        const modalEl = modalBody.closest(".modal");
        if (modalEl && !modalEl.__empEntityClosedHooked) {
          modalEl.__empEntityClosedHooked = true;

          modalEl.addEventListener("hidden.bs.modal", () => {
            // nếu còn modal đang show => thường là submodal đang mở -> bỏ qua
            const stillOpenModal = document.querySelector(".modal.show");
            if (stillOpenModal) return;

            if (typeof onParentClosed === "function") onParentClosed(modalEl);
          });
        }
      },
    };
  };
})();
