// layout.js
App.onReady(() => {
  const toggleBtn = document.getElementById("menu-toggle");
  const wrapper = document.getElementById("wrapper");
  if (!toggleBtn || !wrapper) return;

  toggleBtn.addEventListener("click", () => {
    wrapper.classList.toggle("toggled");
  });
});
