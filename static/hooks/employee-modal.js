// static/js/hooks/employee-modal-hook.js

// Đảm bảo ModalHooks tồn tại
window.ModalHooks = window.ModalHooks || {};

ModalHooks["employee"] = {
  onLoaded(modalBody) {
    if (!modalBody) return;

    // === cleanup event cũ nếu modal render lại nội dung trong cùng 1 phiên ===
    // (ví dụ: submit lỗi validation -> server trả về HTML mới)
    if (modalBody.__employeeAbortCtrl) {
      modalBody.__employeeAbortCtrl.abort();
    }
    const ac = new AbortController();
    modalBody.__employeeAbortCtrl = ac;

    // avatar preview / clear
    const fileInput = modalBody.querySelector('input[type="file"][name="avatar"]');
    const clearCheckbox = modalBody.querySelector('input[name="avatar-clear"]');
    const btnClear = modalBody.querySelector("#btnAvatarClear");
    const img = modalBody.querySelector("#avatarPreviewImg");
    const empty = modalBody.querySelector("#avatarPreviewEmpty");

    // Helper hiển thị preview
    const showImage = (src) => {
      if (img) {
        img.src = src || "";
        img.style.display = src ? "block" : "none";
      }
      if (empty) empty.style.display = src ? "none" : "flex";
    };

    // Khi chọn file mới -> bỏ tick clear + preview
    if (fileInput) {
      fileInput.addEventListener(
        "change",
        () => {
          const f = fileInput.files?.[0];
          if (!f) return;

          if (clearCheckbox) clearCheckbox.checked = false;

          const url = URL.createObjectURL(f);
          showImage(url);

          // Tránh leak objectURL khi thay file nhiều lần
          // (đợi img load xong rồi revoke)
          if (img) {
            img.onload = () => URL.revokeObjectURL(url);
          }
        },
        { signal: ac.signal }
      );
    }

    // Nút "Xóa ảnh" (toggle checkbox clear)
    if (btnClear && clearCheckbox) {
      btnClear.addEventListener(
        "click",
        () => {
          clearCheckbox.checked = !clearCheckbox.checked;

          if (clearCheckbox.checked) {
            // Clear preview + clear input file
            if (fileInput) fileInput.value = "";
            showImage(null);
          } else {
            // Nếu bỏ clear, bạn có thể giữ trạng thái rỗng
            // hoặc hiển thị lại ảnh hiện tại (nếu backend render sẵn src)
            // => ở đây giữ nguyên trạng thái hiện tại
          }
        },
        { signal: ac.signal }
      );
    }

    // Khi tick vào checkbox clear (nếu user click trực tiếp checkbox)
    if (clearCheckbox) {
      clearCheckbox.addEventListener(
        "change",
        () => {
          if (clearCheckbox.checked) {
            if (fileInput) fileInput.value = "";
            showImage(null);
          }
        },
        { signal: ac.signal }
      );
    }

    // Nếu modal HTML có sẵn ảnh hiện tại (img.src), đảm bảo trạng thái empty đúng
    if (img && img.getAttribute("src")) {
      const src = img.getAttribute("src");
      if (src && src.trim() && src !== "#") showImage(src);
    } else {
      // không có src -> show empty
      showImage(null);
    }
  },

  onSuccess() {
    // Tùy bạn: reload table / gọi lại API / toast
    // Ví dụ đơn giản:
    // window.location.reload();
  }
};
