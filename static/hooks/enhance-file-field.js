// static/js/hooks/enhance-file-field.js
function enhanceClearableFileInput(modalBody) {
  if (!modalBody) return;

  // field file của bạn
  const item = modalBody.querySelector(".emp-form-item-file");
  if (!item) return;

  // tránh chạy lại nhiều lần
  if (item.classList.contains("is-enhanced")) return;

  // ===== tìm các thành phần Django render =====
  const fileInput = item.querySelector('input[type="file"]');
  if (!fileInput) return;

  const clearCheckbox =
    item.querySelector('input[type="checkbox"][name$="-clear"]') ||
    item.querySelector('input[type="checkbox"][id$="-clear_id"]');

  let clearLabel = null;
  if (clearCheckbox) {
    clearLabel =
      item.querySelector(`label[for="${clearCheckbox.id}"]`) ||
      clearCheckbox.closest("label");
  }

  const currentLink = item.querySelector("a"); // file hiện tại

  // ===== build UI mới =====
  const wrap = document.createElement("div");
  wrap.className = "ff-wrap";

  // row: currently + clear
  const row = document.createElement("div");
  row.className = "ff-row";

  const current = document.createElement("div");
  current.className = "ff-current";
  if (currentLink) current.appendChild(currentLink);

  row.appendChild(current);

  if (clearCheckbox) {
    const clearBox = document.createElement("div");
    clearBox.className = "ff-clear";

    clearBox.appendChild(clearCheckbox);

    if (!clearLabel) {
      clearLabel = document.createElement("label");
      clearLabel.textContent = "Clear";
      clearLabel.htmlFor = clearCheckbox.id;
    }
    clearBox.appendChild(clearLabel);

    row.appendChild(clearBox);
  }

  // change block
  const change = document.createElement("div");
  change.className = "ff-change";

  const changeLabel = document.createElement("span");
  changeLabel.className = "ff-label";
  changeLabel.textContent = "Change";

  change.appendChild(changeLabel);
  change.appendChild(fileInput);

  // ===== gắn DOM mới =====
  wrap.appendChild(row);
  wrap.appendChild(change);
  item.appendChild(wrap);

  // đánh dấu đã enhance
  item.classList.add("is-enhanced");
}