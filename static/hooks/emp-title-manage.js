// hooks/emp-title-manage.js
ModalHooks["emp_title_manage"] = {
  onLoaded(modalBody) {
    console.log("emp_title_manage modal loaded");
    if (modalBody.__empTitleAbortCtrl) {
      modalBody.__empTitleAbortCtrl.abort();
      }
      const ac = new AbortController();
      modalBody.__empTitleAbortCtrl = ac;
    const inp = modalBody.querySelector("#empCode");
    const suggestBox = modalBody.querySelector("#empSuggest");
    const name = modalBody.querySelector("#empName");
    const wrap = modalBody.querySelector("#empTitleTableWrap");
    const btnAdd = modalBody.querySelector(".js-add-title");

    if (!inp || !suggestBox || !name || !wrap || !btnAdd) return;

    let currentEmpNum = null;
    let currentPage = 1; // ✅ nhớ trang hiện tại để reload đúng sau khi thêm/sửa
    
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

    resetUI();

    async function fetchJSON(url, options = {}) {
      const res = await fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" },
        ...options
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    }

    async function loadTitles(page = 1) {
      if (!currentEmpNum) return;

      const p = parseInt(page, 10);
      currentPage = Number.isFinite(p) && p >= 1 ? p : 1;

      try {
        const url = `/api/employee/${encodeURIComponent(currentEmpNum)}/titles/?page=${currentPage}`;
        const data = await fetchJSON(url);
        wrap.innerHTML = data.html || `<div class="text-muted">Chưa có chức vụ.</div>`;
      } catch (err) {
        console.error("loadTitles error:", err);
        wrap.innerHTML = `<div class="text-danger">Lỗi tải dữ liệu</div>`;
      }
    }

    // ✅ lookup dropdown
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

        loadTitles(1);
      }
    });

    // ✅ Click phân trang + Click mở modal con (sửa/xem) trong bảng
    modalBody.addEventListener("click", (e) => {
      // Pagination
      const a = e.target.closest(".js-title-page");
      if (a) {
        e.preventDefault();
        loadTitles(a.dataset.page || 1);
        return;
      }

      // Open child modal (edit/view)
      const btn = e.target.closest("[data-open-child]");
      if (!btn) return;

      AppModalStack.openChild(btn.dataset.url, {
        title: btn.dataset.title || "Chức vụ",
        type: btn.dataset.type || "emp_title_form",
        onClosed: () => loadTitles(currentPage) // ✅ reload đúng trang đang đứng
      });
    });

    // Nếu user gõ/xoá -> reset hợp lý
    inp.addEventListener("input", () => {
      const v = inp.value.trim();

      if (!v) {
        resetUI();
        return;
      }

      inp.classList.remove("is-invalid");

      // nếu trước đó đã chọn, nhưng giờ sửa khác -> khoá nút + clear tên
      if (currentEmpNum && v !== currentEmpNum) {
        currentEmpNum = null;
        currentPage = 1;
        name.value = "";
        btnAdd.disabled = true;
        wrap.innerHTML = `<div class="text-muted">Hãy chọn đúng mã trong danh sách gợi ý.</div>`;
        inp.classList.remove("is-valid");
      }
    });

    // Rời input mà chưa chọn đúng -> báo invalid
    inp.addEventListener("blur", () => {
      const v = inp.value.trim();
      if (!v) return;
      if (!currentEmpNum) setInvalid();
    });

    // Thêm chức vụ (modal con)
    btnAdd.addEventListener("click", () => {
      if (!currentEmpNum) return;

      AppModalStack.openChild(`/titles/add/?emp_num=${encodeURIComponent(currentEmpNum)}`, {
        title: "Thêm chức vụ",
        type: "emp_title_form",
        onClosed: () => loadTitles(currentPage) // ✅ thêm xong vẫn ở trang hiện tại
      });
    });

    modalBody.addEventListener(
  "click",
  async (e) => {

    /* ===== XÓA CHỨC DANH ===== */
    const delBtn = e.target.closest(".js-delete-title");
    if (delBtn) {
      e.preventDefault();
      e.stopPropagation(); // ✅ RẤT QUAN TRỌNG

      const ok = confirm("Bạn có chắc chắn muốn xoá chức danh này?");
      if (!ok) return;

      try {
        const res = await fetch(delBtn.dataset.url, {
          method: "POST",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCSRFToken()
          }
        });

        const data = await res.json();

        if (data.success) {
          loadTitles(currentPage); // ✅ reload bảng
        } else {
          alert("Không thể xoá bản ghi");
        }
      } catch (err) {
        console.error(err);
        alert("Lỗi khi xoá");
      }

      return; // ✅ chặn listener khác
    }


  },
  { signal: ac.signal } // ✅ QUAN TRỌNG
  );
  function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]')?.value
      || document.cookie.split('; ')
           .find(row => row.startsWith('csrftoken='))
           ?.split('=')[1];
  }
      // 🔄 Reload trang khi ĐÓNG modal cha
      const modalEl = modalBody.closest(".modal");
      if (modalEl && !modalEl.__reloadHooked) {
        modalEl.__reloadHooked = true;

        modalEl.addEventListener("hidden.bs.modal", () => {
          // Nếu vẫn còn modal đang mở → là modal con → KHÔNG reload
          const stillOpenModal = document.querySelector(".modal.show");
          if (stillOpenModal) return;

          // ✅ Đóng modal cha thật → reload trang
          window.location.reload();
        });
      }
  }
};