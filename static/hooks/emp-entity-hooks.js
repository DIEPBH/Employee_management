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

ModalHooks["emp_workprocess_manage"] = createEmpEntityManageHook(
  createEmpCrudPreset({
    baseUrl: "/workprocess",
    listApiPrefix: "/api/employee/{emp}/workprocess/",
    childType: "emp_workprocess_form",

    tableWrapSel: "#empWorkprocessTableWrap",
    btnAddSel: ".js-add-workprocess",
    pageLinkSel: ".js-workprocess-page",
    deleteBtnSel: ".js-delete-workprocess",

    childTitleDefault: "Thông tin quá trình công tác",
    addTitleDefault: "Thêm mới thông tin quá trình công tác",
    confirmDeleteText: "Bạn có chắc chắn muốn xoá thông tin quá trình công tác này?",
    
    onParentClosed: () => window.location.reload(),
  })
);

ModalHooks["emp_salaryprocess_manage"] = createEmpEntityManageHook(
  createEmpCrudPreset({
    baseUrl: "/salaryprocess",
    listApiPrefix: "/api/employee/{emp}/salaryprocess/",
    childType: "emp_salaryprocess_form",

    tableWrapSel: "#empSalaryprocessTableWrap",
    btnAddSel: ".js-add-salaryprocess",
    pageLinkSel: ".js-salaryprocess-page",
    deleteBtnSel: ".js-delete-salaryprocess",

    childTitleDefault: "Thông tin quá trình lương",
    addTitleDefault: "Thêm mới thông tin quá trình lương",
    confirmDeleteText: "Bạn có chắc chắn muốn xoá thông tin quá trình lương này?",
    
    onParentClosed: () => window.location.reload(),
  })
);


ModalHooks["emp_award_manage"] = createEmpEntityManageHook(
  createEmpCrudPreset({
    baseUrl: "/award",
    listApiPrefix: "/api/employee/{emp}/award/",
    childType: "emp_award_form",

    tableWrapSel: "#empAwardTableWrap",
    btnAddSel: ".js-add-award",
    pageLinkSel: ".js-award-page",
    deleteBtnSel: ".js-delete-award",

    childTitleDefault: "Thông tin khen thưởng",
    addTitleDefault: "Thêm mới thông tin khen thưởng",
    confirmDeleteText: "Bạn có chắc chắn muốn xoá thông tin khen thưởng này?",
    
    onParentClosed: () => window.location.reload(),
  })
);

ModalHooks["emp_discipline_manage"] = createEmpEntityManageHook(
  createEmpCrudPreset({
    baseUrl: "/discipline",
    listApiPrefix: "/api/employee/{emp}/discipline/",
    childType: "emp_discipline_form",

    tableWrapSel: "#empDisciplineTableWrap",
    btnAddSel: ".js-add-discipline",
    pageLinkSel: ".js-discipline-page",
    deleteBtnSel: ".js-delete-discipline",

    childTitleDefault: "Thông tin kỷ luật",
    addTitleDefault: "Thêm mới thông tin kỷ luật",
    confirmDeleteText: "Bạn có chắc chắn muốn xoá thông tin kỷ luật này?",
    
    onParentClosed: () => window.location.reload(),
  })
);

ModalHooks["emp_relationship_manage"] = createEmpEntityManageHook(
  createEmpCrudPreset({
    baseUrl: "/relationship",
    listApiPrefix: "/api/employee/{emp}/relationship/",
    childType: "emp_relationship_form",

    tableWrapSel: "#empRelationshipTableWrap",
    btnAddSel: ".js-add-relationship",
    pageLinkSel: ".js-relationship-page",
    deleteBtnSel: ".js-delete-relationship",

    childTitleDefault: "Thông tin thân nhân",
    addTitleDefault: "Thêm mới thông tin thân nhân",
    confirmDeleteText: "Bạn có chắc chắn muốn xoá thông tin thân nhân này?",
    
    onParentClosed: () => window.location.reload(),
  })
);

ModalHooks["emp_foreign_manage"] = createEmpEntityManageHook(
  createEmpCrudPreset({
    baseUrl: "/foreign",
    listApiPrefix: "/api/employee/{emp}/foreign/",
    childType: "emp_foreign_form",

    tableWrapSel: "#empForeignTableWrap",
    btnAddSel: ".js-add-foreign",
    pageLinkSel: ".js-foreign-page",
    deleteBtnSel: ".js-delete-foreign",

    childTitleDefault: "Thông tin người nước ngoài",
    addTitleDefault: "Thêm mới thông tin ra nước ngoài",
    confirmDeleteText: "Bạn có chắc chắn muốn xoá thông tin này?",
    
    onParentClosed: () => window.location.reload(),
  })
);

ModalHooks["emp_army_manage"] = createEmpEntityManageHook(
  createEmpCrudPreset({
    baseUrl: "/army",
    listApiPrefix: "/api/employee/{emp}/army/",
    childType: "emp_army_form",

    tableWrapSel: "#empArmyTableWrap",
    btnAddSel: ".js-add-army",
    pageLinkSel: ".js-army-page",
    deleteBtnSel: ".js-delete-army",

    childTitleDefault: "Thông tin quân đội",
    addTitleDefault: "Thêm mới thông tin quân đội",
    confirmDeleteText: "Bạn có chắc chắn muốn xoá thông tin này?",
    
    onParentClosed: () => window.location.reload(),
  })
);

ModalHooks["emp_health_manage"] = createEmpEntityManageHook(
  createEmpCrudPreset({
    baseUrl: "/health",
    listApiPrefix: "/api/employee/{emp}/health/",
    childType: "emp_health_form",

    tableWrapSel: "#empHealthTableWrap",
    btnAddSel: ".js-add-health",
    pageLinkSel: ".js-health-page",
    deleteBtnSel: ".js-delete-health",

    childTitleDefault: "Thông tin sức khỏe",
    addTitleDefault: "Thêm mới thông tin sức khỏe",
    confirmDeleteText: "Bạn có chắc chắn muốn xoá thông tin này?",
    
    onParentClosed: () => window.location.reload(),
  })
);