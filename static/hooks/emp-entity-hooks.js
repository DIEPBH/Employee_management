//////////////////////////////////////
//////Quản lý quy hoạch cán bộ////////
//////////////////////////////////////

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

//////////////////////////////////////
//////Quản lý đảng ủy cán bộ//////////
//////////////////////////////////////
ModalHooks["emp_party_committee_manage"] = createEmpEntityManageHook(
  createEmpCrudPreset({
    baseUrl: "/party_committee",
    listApiPrefix: "/api/employee/{emp}/party_committee/",
    childType: "emp_partycommittee_form",

    tableWrapSel: "#empartyCommitteeTableWrap",
    btnAddSel: ".js-add-partycommittee",
    pageLinkSel: ".js-partycommittee-page",
    deleteBtnSel: ".js-delete-partycommittee",

    childTitleDefault: "Thông tin đảng ủy cán bộ",
    addTitleDefault: "Thêm mới thông tin đảng ủy cán bộ",
    confirmDeleteText: "Bạn có chắc chắn muốn xoá thông tin đảng ủy cán bộ này?",
    
    onParentClosed: () => window.location.reload(),
  })
);

ModalHooks["emp_training_manage"] = createEmpEntityManageHook(
  createEmpCrudPreset({
    baseUrl: "/training",
    listApiPrefix: "/api/employee/{emp}/training/",
    childType: "emp_training_form",

    tableWrapSel: "#empTrainingTableWrap",
    btnAddSel: ".js-add-training",
    pageLinkSel: ".js-training-page",
    deleteBtnSel: ".js-delete-training",

    childTitleDefault: "Thông tin đào tạo",
    addTitleDefault: "Thêm mới thông tin đào tạo",
    confirmDeleteText: "Bạn có chắc chắn muốn xoá thông tin đào tạo này?",
    
    onParentClosed: () => window.location.reload(),
  })
);
