// static/js/hooks/emp-entity-presets.js
// Preset để tạo nhanh các hook kiểu: quản lý theo cán bộ (list/add/edit/delete/pagination)

(function () {
  /**
   * baseUrl convention:
   * - list:   `${baseUrl}/employee/<empNum>/?page=<page>`  (hoặc bạn tự map bằng listPath)
   * - add:    `${baseUrl}/add/?emp_num=<empNum>`          (hoặc addPath)
   *
   * Bạn có thể override listUrl/addUrl nếu API khác format.
   */

  function enc(v) {
    return encodeURIComponent(v ?? "");
  }

  window.createEmpCrudPreset = function createEmpCrudPreset(p) {
    const {
      // bắt buộc
      baseUrl,         // ví dụ: "/titles" hoặc "/rewards"
      childType,       // ví dụ: "emp_title_form"

      // phần list API theo emp
      // mặc định dùng: `${baseUrl}/api/employee/<emp>/ ?page=`
      // nhưng thường bạn đang có dạng: `/api/employee/<emp>/titles/?page=`
      // nên mình cho phép truyền listApiPrefix cho đúng nhanh
      listApiPrefix,   // ví dụ: "/api/employee/{emp}/titles/"

      // selectors & classes (tuỳ biến theo màn)
      tableWrapSel,    // ví dụ: "#empTitleTableWrap"
      btnAddSel,       // ví dụ: ".js-add-title"
      pageLinkSel,     // ví dụ: ".js-title-page"
      deleteBtnSel,    // ví dụ: ".js-delete-title"

      // text
      childTitleDefault = "Chi tiết",
      addTitleDefault = "Thêm mới",
      confirmDeleteText = "Bạn có chắc chắn muốn xoá bản ghi này?",

      // behavior
      onParentClosed, // ví dụ: () => window.location.reload()

      // advanced overrides (nếu URL khác chuẩn)
      listUrl, // (empNum,page)=>string
      addUrl,  // (empNum)=>string
    } = p || {};

    if (!baseUrl && !listApiPrefix) {
      throw new Error("createEmpCrudPreset: cần baseUrl hoặc listApiPrefix");
    }
    if (!childType) throw new Error("createEmpCrudPreset: cần childType");
    if (!tableWrapSel || !btnAddSel || !pageLinkSel || !deleteBtnSel) {
      throw new Error("createEmpCrudPreset: thiếu selector/class (tableWrapSel/btnAddSel/pageLinkSel/deleteBtnSel)");
    }

    const _listUrl =
      listUrl ||
      ((empNum, page) => {
        if (!listApiPrefix) {
          // fallback: `${baseUrl}/employee/<emp>/ ?page=`
          return `${baseUrl}/employee/${enc(empNum)}/?page=${Number(page) || 1}`;
        }
        // listApiPrefix support token {emp}
        const prefix = listApiPrefix.replace("{emp}", enc(empNum));
        return `${prefix}?page=${Number(page) || 1}`;
      });

    const _addUrl =
      addUrl ||
      ((empNum) => `${baseUrl}/add/?emp_num=${enc(empNum)}`);

    return {
      tableWrapSel,
      btnAddSel,
      pageLinkSel,
      deleteBtnSel,

      listUrl: _listUrl,
      addUrl: _addUrl,

      childTypeDefault: childType,
      childTitleDefault,
      addTitleDefault,
      confirmDeleteText,

      onParentClosed,
    };
  };
})();
