//////////////////////////////////////
//////Quản lý quy hoạch cán bộ////////
//////////////////////////////////////

// static/js/hooks/emp-reward-manage.js

ModalHooks["emp_position_manage"] = createEmpEntityManageHook(
  createEmpCrudPreset({
    baseUrl: "/positions",
    listApiPrefix: "/api/employee/{emp}/position/",
    childType: "emp_position_form",

    tableWrapSel: "#empPositionTableWrap",
    btnAddSel: ".js-add-position",
    pageLinkSel: ".js-position-page",
    deleteBtnSel: ".js-delete-position",

    childTitleDefault: "Quy hoạch chức vụ",
    addTitleDefault: "Thêm mới quy hoạch chức vụ",
    confirmDeleteText: "Bạn có chắc chắn muốn xoá quy hoạch chức vụ này?",

    onParentClosed: () => window.location.reload(),
  })
);
