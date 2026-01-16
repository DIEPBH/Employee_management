from django.urls import path,include
from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_employee, name='add_employee'),
    path('edit/<int:emp_id>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:emp_id>/', views.delete_employee, name='delete_employee'),
    path('add_modal/', views.add_employee_modal, name='add_employee_modal'),
    path('edit_modal/<int:emp_id>/', views.edit_employee_modal, name='edit_employee_modal'),
    path('title', views.index_emp_tile, name = 'index_emp_tile'),
    path('add_title/', views.add_employee_title_modal, name='add_employee_title_modal'),

    #popup quản lý chức danh
    # popup 1
    path("title/popup/", views.title_manager_modal, name="title_manager_modal"),
    path("api/emp_lookup/", views.api_emp_lookup, name="api_emp_lookup"),
    path("api/title_list/", views.api_title_list, name="api_title_list"),

    # popup 2 (form)
    path("title/add_modal/", views.add_employee_title_modal, name="add_employee_title_modal"),
    #path("title/edit_modal/<int:pk>/", views.edit_title_modal, name="edit_title_modal"),
    #path("title/delete/<int:pk>/", views.delete_title, name="delete_title"),
]