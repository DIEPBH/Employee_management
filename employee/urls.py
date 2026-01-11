from django.urls import path,include
from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_employee, name='add_employee'),
    path('edit/<int:emp_id>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:emp_id>/', views.delete_employee, name='delete_employee'),
]