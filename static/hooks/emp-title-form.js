// static/js/hooks/emp-title-form.js
window.ModalHooks = window.ModalHooks || {};

ModalHooks["emp_title_form"] = {
  onLoaded(modalBody) {
    console.log("title-form loaded")
    if (!modalBody) return;

    // ✅ gọi helper (đã được load global)
    if (window.enhanceClearableFileInput) {
      window.enhanceClearableFileInput(modalBody);
    }
  }
};