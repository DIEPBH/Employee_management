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
    path('title', views.index_emp_tile, name = 'index_emp_tile'),
    path('add_title/', views.title_manager_modal, name='title_manager_modal'),
    path('api/employee/', views.employee_lookup, name='employee_lookup'),
    path("api/employee/<str:emp_num>/titles/", views.employee_titles_table, name="employee_titles_table"),
    path("titles/add/", views.emp_title_form, name="emp_title_form"),
    #path("titles/<int:pk>/edit/", views.emp_title_edit_modal, name="emp_title_edit_modal"),
    #path("titles/<int:pk>/view/", views.emp_title_view_modal, name="emp_title_view_modal"),
    # 5) (tuỳ chọn) xóa
    #path("titles/<int:pk>/delete/", views.emp_title_delete, name="emp_title_delete"),

]