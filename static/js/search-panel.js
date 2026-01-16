// search-panel.js
App.onReady(() => {
  const btn = document.getElementById("toggle-search");
  const wrapper = document.getElementById("search-panel-wrapper");
  if (!btn || !wrapper) return;

  const form = wrapper.querySelector("form");
  if (!form) return;

  const key = "searchPanelHidden";
  let animating = false;

  // chuẩn bị CSS-transition bằng inline height (mượt + không giật)
  function setCollapsed(collapsed, instant = false) {
    if (animating) return;
    animating = true;

    form.style.overflow = "hidden";
    form.style.willChange = "height, opacity";

    const done = () => {
      animating = false;
      form.style.willChange = "auto";
    };

    if (collapsed) {
      // đo chiều cao hiện tại
      form.style.display = "block";
      const h = form.scrollHeight;

      if (instant) {
        form.style.height = "0px";
        form.style.opacity = "0";
        form.style.display = "none";
        btn.textContent = "^"; // bạn muốn ký tự ^
        localStorage.setItem(key, "true");
        return done();
      }

      form.style.height = h + "px";
      form.style.opacity = "1";

      requestAnimationFrame(() => {
        form.style.height = "0px";
        form.style.opacity = "0";
      });

      const onEnd = (e) => {
        if (e.propertyName !== "height") return;
        form.removeEventListener("transitionend", onEnd);
        form.style.display = "none";
        btn.textContent = "^";
        localStorage.setItem(key, "true");
        done();
      };
      form.addEventListener("transitionend", onEnd);

    } else {
      form.style.display = "block";
      form.style.height = "0px";
      form.style.opacity = "0";

      const target = form.scrollHeight;

      if (instant) {
        form.style.height = "auto";
        form.style.opacity = "1";
        btn.textContent = "v"; // mở thì v
        localStorage.setItem(key, "false");
        return done();
      }

      requestAnimationFrame(() => {
        form.style.height = target + "px";
        form.style.opacity = "1";
      });

      const onEnd = (e) => {
        if (e.propertyName !== "height") return;
        form.removeEventListener("transitionend", onEnd);
        form.style.height = "auto";
        btn.textContent = "v";
        localStorage.setItem(key, "false");
        done();
      };
      form.addEventListener("transitionend", onEnd);
    }
  }

  // restore
  const savedHidden = localStorage.getItem(key) === "true";
  setCollapsed(savedHidden, true);

  btn.addEventListener("click", () => {
    const hidden = localStorage.getItem(key) === "true";
    setCollapsed(!hidden, false);
  });
});
