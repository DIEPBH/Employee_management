from django.urls import path,include
from . import views

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

    #Quy hoạch cán bộ
    path('positions/', views.index_emp_position, name = 'index_emp_position'),
    path("api/employee/<str:emp_num>/position/", views.employee_position_table, name="employee_position_table"),
    path("positions/add/", views.emp_position_form, name="emp_position_form"),
    path('add_position/', views.position_manager_modal, name='position_manager_modal'),

]
