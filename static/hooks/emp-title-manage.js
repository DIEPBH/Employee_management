// hooks/emp-title-manage.js
ModalHooks["emp_title_manage"] = {
  onLoaded(modalBody) {
    console.log("emp_title_manage modal loaded");

    const inp = modalBody.querySelector("#empCode");
    const suggestBox = modalBody.querySelector("#empSuggest");
    const name = modalBody.querySelector("#empName");
    const wrap = modalBody.querySelector("#empTitleTableWrap");
    const btnAdd = modalBody.querySelector(".js-add-title");

    if (!inp || !suggestBox || !name || !wrap || !btnAdd) return;

    let currentEmpNum = null;

    function resetUI(msg = "Vui lòng nhập mã cán bộ để tra cứu.") {
      currentEmpNum = null;
      name.value = "";
      btnAdd.disabled = true;
      wrap.innerHTML = `<div class="text-muted">${msg}</div>`;
      inp.classList.remove("is-valid", "is-invalid");
    }

    function setInvalid(msg = "Mã cán bộ không hợp lệ hoặc không tồn tại.") {
      currentEmpNum = null;
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

      page = parseInt(page, 10);
      if (!Number.isFinite(page) || page < 1) page = 1;

      try {
        const url = `/api/employee/${encodeURIComponent(currentEmpNum)}/titles/?page=${page}`;
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
        name.value = emp.name;
        btnAdd.disabled = false;

        inp.classList.remove("is-invalid");
        inp.classList.add("is-valid");

        loadTitles(1); // <-- load trang 1 ngay khi chọn
      }
    });

    // Click phân trang trong bảng
    modalBody.addEventListener("click", (e) => {
      const a = e.target.closest(".js-title-page");
      if (a) {
        e.preventDefault();
        const page = a.dataset.page || 1;
        loadTitles(page);
        return;
      }

      // Click Sửa/Xem trong bảng
      const btn = e.target.closest("[data-open-child]");
      if (!btn) return;

      AppModalStack.openChild(btn.dataset.url, {
        title: btn.dataset.title || "Chức vụ",
        type: btn.dataset.type || "emp_title_form",
        onClosed: () => loadTitles(1) // hoặc loadTitles() nếu bạn muốn giữ trang hiện tại
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

      if (currentEmpNum && v !== currentEmpNum) {
        currentEmpNum = null;
        name.value = "";
        btnAdd.disabled = true;
        wrap.innerHTML = `<div class="text-muted">Hãy chọn đúng mã trong danh sách gợi ý.</div>`;
        inp.classList.remove("is-valid");
      }
    });

    inp.addEventListener("blur", () => {
      const v = inp.value.trim();
      if (!v) return;
      if (!currentEmpNum) setInvalid();
    });

    btnAdd.addEventListener("click", () => {
      if (!currentEmpNum) return;

      AppModalStack.openChild(`/titles/add/?emp_num=${encodeURIComponent(currentEmpNum)}`, {
        title: "Thêm chức vụ",
        type: "emp_title_form",
        onClosed: () => loadTitles(1)
      });
    });
  }
};