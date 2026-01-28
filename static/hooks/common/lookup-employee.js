// hooks/common/lookup-employee.js
function bindEmployeeLookup({ input, suggestBox, onSelect }) {
  if (!input || !suggestBox) return;

  let items = [];
  let activeIndex = -1;

  let timer = null;
  let lastQuery = "";
  let abortCtrl = null;

  function hide() {
    suggestBox.classList.add("d-none");
    suggestBox.innerHTML = "";
    items = [];
    activeIndex = -1;
  }

  function show() {
    suggestBox.classList.remove("d-none");
  }

  function render(list) {
    items = Array.isArray(list) ? list : [];
    activeIndex = -1;

    if (!items.length) {
      suggestBox.innerHTML = `<div class="empty">Không có kết quả phù hợp</div>`;
      show();
      return;
    }

    suggestBox.innerHTML = items
      .map(
        (it, idx) => `
        <div class="item" data-idx="${idx}" role="option" aria-selected="false">
          <span class="code">${it.code ?? ""}</span>
          <span class="name">${it.name ?? ""}</span>
        </div>
      `
      )
      .join("");

    show();
  }

  function setActive(i) {
    const els = suggestBox.querySelectorAll(".item");
    els.forEach((el) => {
      el.classList.remove("active");
      el.setAttribute("aria-selected", "false");
    });

    if (i >= 0 && i < els.length) {
      els[i].classList.add("active");
      els[i].setAttribute("aria-selected", "true");
      activeIndex = i;

      // đảm bảo item active luôn nằm trong view
      els[i].scrollIntoView({ block: "nearest" });
    }
  }

  async function fetchSuggest(q) {
    // cancel request trước đó
    if (abortCtrl) abortCtrl.abort();
    abortCtrl = new AbortController();

    const res = await fetch(`/api/employee/?q=${encodeURIComponent(q)}`, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
      signal: abortCtrl.signal
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  function selectItem(it) {
    if (!it) return;
    input.value = it.code;
    hide();
    if (typeof onSelect === "function") onSelect(it);
  }

  // ===== INPUT (debounce) =====
  input.addEventListener("input", () => {
    const q = input.value.trim();
    lastQuery = q;

    if (!q) {
      if (timer) clearTimeout(timer);
      hide();
      return;
    }

    if (timer) clearTimeout(timer);
    timer = setTimeout(async () => {
      try {
        const data = await fetchSuggest(q);

        // nếu user đã gõ sang query khác trong lúc chờ => bỏ
        if (input.value.trim() !== q) return;

        render(data.items || []);
      } catch (e) {
        // AbortError là bình thường khi gõ nhanh
        if (e?.name !== "AbortError") console.error("lookup error:", e);
        hide();
      }
    }, 200);
  });

  // ===== CLICK chọn (mousedown để không mất focus trước) =====
  suggestBox.addEventListener("mousedown", (e) => {
    const el = e.target.closest(".item");
    if (!el) return;
    const it = items[Number(el.dataset.idx)];
    selectItem(it);
  });

  // ===== KEYBOARD =====
  input.addEventListener("keydown", (e) => {
    if (suggestBox.classList.contains("d-none")) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive(Math.min(activeIndex + 1, items.length - 1));
      return;
    }

    if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive(Math.max(activeIndex - 1, 0));
      return;
    }

    if (e.key === "Enter") {
      // ưu tiên chọn item đang active
      if (activeIndex >= 0) {
        e.preventDefault();
        return selectItem(items[activeIndex]);
      }

      // nếu chưa active, thử match theo code đang gõ trong list hiện tại
      const code = input.value.trim();
      const matched = items.find((x) => (x.code || "").toLowerCase() === code.toLowerCase());
      if (matched) {
        e.preventDefault();
        return selectItem(matched);
      }

      // không match thì để emp-title-manage xử lý invalid khi blur
      return;
    }

    if (e.key === "Escape") {
      hide();
    }
  });

  // ===== CLICK ngoài để đóng =====
  document.addEventListener(
    "mousedown",
    (e) => {
      if (suggestBox.classList.contains("d-none")) return;
      if (e.target === input) return;
      if (suggestBox.contains(e.target)) return;
      hide();
    },
    true
  );

  // ===== BLUR: delay để kịp click item =====
  input.addEventListener("blur", () => setTimeout(hide, 140));
}