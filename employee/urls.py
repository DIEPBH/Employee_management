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
]
