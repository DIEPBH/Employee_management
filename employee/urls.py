from django.urls import path,include
from . import views
from .view_modules.emp_title_import import emp_title_import_modal

app_name = 'employee'

urlpatterns = [
    #Quản lý Cán bộ
    path('', views.index, name='index'),
    path('add/', views.add_employee, name='add_employee'),
    path('edit/<int:emp_id>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:emp_id>/', views.delete_employee, name='delete_employee'),
    path('add_modal/', views.add_employee_modal, name='add_employee_modal'),
    path('edit_modal/<int:emp_id>/', views.edit_employee_modal, name='edit_employee_modal'),

    #Chức danh Cán bộ
    path('titles/', views.index_emp_tile, name = 'index_emp_tile'),
    path('add_title/', views.title_manager_modal, name='title_manager_modal'),
    path('api/employee/', views.employee_lookup, name='employee_lookup'),
    path("api/employee/<str:emp_num>/titles/", views.employee_titles_table, name="employee_titles_table"),
    path("titles/add/", views.emp_title_form, name="emp_title_form"),
    path("titles/<int:id>/edit/", views.emp_title_edit_modal, name="emp_title_edit_modal"),#Sửa trên Modal
    path("titles/<int:id>/view/", views.emp_title_view_modal, name="emp_title_view_modal"), 
    path("titles/<int:id>/delete/", views.emp_title_delete, name="emp_title_delete"),
    path("titles/<int:id>/delete_/", views.emp_title_delete_, name="emp_title_delete_"), #Xóa trên search
    path("emp-title/import/", emp_title_import_modal, name="emp_title_import_modal"),

    #Quy hoạch cán bộ
    path('positions/', views.index_emp_position, name = 'index_emp_position'),
    path("api/employee/<str:emp_num>/position/", views.employee_position_table, name="employee_position_table"),
    path("positions/add/", views.emp_position_form, name="emp_position_form"),
    path('add_position/', views.position_manager_modal, name='position_manager_modal'),
    path("positions/<int:id>/edit/", views.emp_position_edit_modal, name="emp_position_edit_modal"),#Sửa trên Modal
    path("positions/<int:id>/view/", views.emp_position_view_modal, name="emp_position_view_modal"), 
    path("positions/<int:id>/delete/", views.emp_position_delete, name="emp_position_delete"),
    path("positions/<int:id>/delete_/", views.emp_position_delete_, name="emp_position_delete_"), #Xóa trên search

    #Thông tin đảng ủy cán bộ
    path('party_committee/', views.index_emp_party_committee, name = 'index_emp_party_committee'),
    path("api/employee/<str:emp_num>/party_committee/", views.employee_party_committee_table, name="employee_party_committee_table"),
    path("party_committee/add/", views.emp_party_committee_form, name="emp_party_committee_form"),
    path('add_party_committee/', views.party_committee_manager_modal, name='party_committee_manager_modal'),
    path("party_committee/<int:id>/edit/", views.emp_party_committee_edit_modal, name="emp_party_committee_edit_modal"),#Sửa trên Modal
    path("party_committee/<int:id>/view/", views.emp_party_committee_view_modal, name="emp_party_committee_view_modal"), 
    path("party_committee/<int:id>/delete/", views.emp_party_committee_delete, name="emp_party_committee_delete"),
    path("party_committee/<int:id>/delete_/", views.emp_party_committee_delete_, name="emp_party_committee_delete_"), #Xóa trên search

    #Thông tin đào tạo cán bộ
    path('training/', views.index_emp_training, name = 'index_emp_training'),
    path("api/employee/<str:emp_num>/training/", views.employee_training_table, name="employee_training_table"),
    path("training/add/", views.emp_training_form, name="emp_training_form"),
    path('add_training/', views.training_manager_modal, name='training_manager_modal'),
    path("training/<int:id>/edit/", views.emp_training_edit_modal, name="emp_training_edit_modal"),#Sửa trên Modal
    path("training/<int:id>/view/", views.emp_training_view_modal, name="emp_training_view_modal"), 
    path("training/<int:id>/delete/", views.emp_training_delete, name="emp_training_delete"),
    path("training/<int:id>/delete_/", views.emp_training_delete_, name="emp_training_delete_"), #Xóa trên search

    #Thông tin quá trình công tác cán bộ
    path('workprocess/', views.index_emp_work_process, name = 'index_emp_work_process'),
    path("api/employee/<str:emp_num>/workprocess/", views.employee_workprocess_table, name="employee_workprocess_table"),
    path("workprocess/add/", views.emp_workprocess_form, name="emp_workprocess_form"),
    path('add_workprocess/', views.workprocess_manager_modal, name='workprocess_manager_modal'),
    path("workprocess/<int:id>/edit/", views.emp_workprocess_edit_modal, name="emp_workprocess_edit_modal"),#Sửa trên Modal
    path("workprocess/<int:id>/view/", views.emp_workprocess_view_modal, name="emp_workprocess_view_modal"), 
    path("workprocess/<int:id>/delete/", views.emp_workprocess_delete, name="emp_workprocess_delete"),
    path("workprocess/<int:id>/delete_/", views.emp_workprocess_delete_, name="emp_workprocess_delete_"), #Xóa trên search

    #Thông tin quá trình Lương cán bộ
    path('salaryprocess/', views.index_emp_salary_process, name = 'index_emp_salary_process'),
    path("api/employee/<str:emp_num>/salaryprocess/", views.employee_salaryprocess_table, name="employee_salaryprocess_table"),
    path("salaryprocess/add/", views.emp_salaryprocess_form, name="emp_salaryprocess_form"),
    path('add_salaryprocess/', views.salaryprocess_manager_modal, name='salaryprocess_manager_modal'),
    path("salaryprocess/<int:id>/edit/", views.emp_salaryprocess_edit_modal, name="emp_salaryprocess_edit_modal"),#Sửa trên Modal
    path("salaryprocess/<int:id>/view/", views.emp_salaryprocess_view_modal, name="emp_salaryprocess_view_modal"), 
    path("salaryprocess/<int:id>/delete/", views.emp_salaryprocess_delete, name="emp_salaryprocess_delete"),
    path("salaryprocess/<int:id>/delete_/", views.emp_salaryprocess_delete_, name="emp_salaryprocess_delete_"), #Xóa trên search

    #Thông tin khen thưởng cán bộ
    path('award/', views.index_emp_award, name = 'index_emp_award'),
    path("api/employee/<str:emp_num>/award/", views.employee_award_table, name="employee_award_table"),
    path("award/add/", views.emp_award_form, name="emp_award_form"),
    path('add_award/', views.award_manager_modal, name='award_manager_modal'),
    path("award/<int:id>/edit/", views.emp_award_edit_modal, name="emp_award_edit_modal"),#Sửa trên Modal
    path("award/<int:id>/view/", views.emp_award_view_modal, name="emp_award_view_modal"), 
    path("award/<int:id>/delete/", views.emp_award_delete, name="emp_award_delete"),
    path("award/<int:id>/delete_/", views.emp_award_delete_, name="emp_award_delete_"), #Xóa trên search

    #Thông tin kỷ luật cán bộ
    path('discipline/', views.index_emp_discipline, name = 'index_emp_discipline'),
    path("api/employee/<str:emp_num>/discipline/", views.employee_discipline_table, name="employee_discipline_table"),
    path("discipline/add/", views.emp_discipline_form, name="emp_discipline_form"),
    path('add_discipline/', views.discipline_manager_modal, name='discipline_manager_modal'),
    path("discipline/<int:id>/edit/", views.emp_discipline_edit_modal, name="emp_discipline_edit_modal"),#Sửa trên Modal
    path("discipline/<int:id>/view/", views.emp_discipline_view_modal, name="emp_discipline_view_modal"), 
    path("discipline/<int:id>/delete/", views.emp_discipline_delete, name="emp_discipline_delete"),
    path("discipline/<int:id>/delete_/", views.emp_discipline_delete_, name="emp_discipline_delete_"), #Xóa trên search

    #Thông tin thân nhân cán bộ
    path('relationship/', views.index_emp_relationship, name = 'index_emp_relationship'),
    path("api/employee/<str:emp_num>/relationship/", views.employee_relationship_table, name="employee_relationship_table"),
    path("relationship/add/", views.emp_relationship_form, name="emp_relationship_form"),
    path('add_relationship/', views.relationship_manager_modal, name='relationship_manager_modal'),
    path("relationship/<int:id>/edit/", views.emp_relationship_edit_modal, name="emp_relationship_edit_modal"),#Sửa trên Modal
    path("relationship/<int:id>/view/", views.emp_relationship_view_modal, name="emp_relationship_view_modal"), 
    path("relationship/<int:id>/delete/", views.emp_relationship_delete, name="emp_relationship_delete"),
    path("relationship/<int:id>/delete_/", views.emp_relationship_delete_, name="emp_relationship_delete_"), #Xóa trên search

    #Thông tin ra nước ngoài cán bộ
    path('foreign/', views.index_emp_foreign, name = 'index_emp_foreign'),
    path("api/employee/<str:emp_num>/foreign/", views.employee_foreign_table, name="employee_foreign_table"),
    path("foreign/add/", views.emp_foreign_form, name="emp_foreign_form"),
    path('add_foreign/', views.foreign_manager_modal, name='foreign_manager_modal'),
    path("foreign/<int:id>/edit/", views.emp_foreign_edit_modal, name="emp_foreign_edit_modal"),#Sửa trên Modal
    path("foreign/<int:id>/view/", views.emp_foreign_view_modal, name="emp_foreign_view_modal"), 
    path("foreign/<int:id>/delete/", views.emp_foreign_delete, name="emp_foreign_delete"),
    path("foreign/<int:id>/delete_/", views.emp_foreign_delete_, name="emp_foreign_delete_"), #Xóa trên search

    #Thông tin tham gia quân đội của cán bộ
    path('army/', views.index_emp_army, name = 'index_emp_army'),
    path("api/employee/<str:emp_num>/army/", views.employee_army_table, name="employee_army_table"),
    path("army/add/", views.emp_army_form, name="emp_army_form"),
    path('add_army/', views.army_manager_modal, name='army_manager_modal'),
    path("army/<int:id>/edit/", views.emp_army_edit_modal, name="emp_army_edit_modal"),#Sửa trên Modal
    path("army/<int:id>/view/", views.emp_army_view_modal, name="emp_army_view_modal"), 
    path("army/<int:id>/delete/", views.emp_army_delete, name="emp_army_delete"),
    path("army/<int:id>/delete_/", views.emp_army_delete_, name="emp_army_delete_"), #Xóa trên search

    #Thông tin sức khỏe của cán bộ
    path('health/', views.index_emp_health, name = 'index_emp_health'),
    path("api/employee/<str:emp_num>/health/", views.employee_health_table, name="employee_health_table"),
    path("health/add/", views.emp_health_form, name="emp_health_form"),
    path('add_health/', views.health_manager_modal, name='health_manager_modal'),
    path("health/<int:id>/edit/", views.emp_health_edit_modal, name="emp_health_edit_modal"),#Sửa trên Modal
    path("health/<int:id>/view/", views.emp_health_view_modal, name="emp_health_view_modal"), 
    path("health/<int:id>/delete/", views.emp_health_delete, name="emp_health_delete"),
    path("health/<int:id>/delete_/", views.emp_health_delete_, name="emp_health_delete_"), #Xóa trên search
]
