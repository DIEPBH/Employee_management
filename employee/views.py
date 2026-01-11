from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from employee.form import EmpInformationForm
from .models import Emp_information
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.db.models import Q
# Create your views here.

@login_required
def index(request):
    if request.user.is_authenticated:
        employees = Emp_information.objects.all()
        return render(request, 'employee/index.html', {'employees': employees})
    
@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmpInformationForm(request.POST, request.FILES)
        if form.is_valid():
            new_employee = form.save(commit=False)
            new_employee.created_by = request.user
            new_employee.created_at = datetime.now()
            new_employee.save()
            messages.success(request, 'Nhân viên mới đã được thêm thành công.')
            return redirect('employee:index')
    else:
        form = EmpInformationForm()
    return render(request, 'employee/add_emp.html', {'form': form})

@login_required
def edit_employee(request, emp_id):
    employee = get_object_or_404(Emp_information, id=emp_id)
    if request.method == 'POST':
        form = EmpInformationForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thông tin nhân viên đã được cập nhật thành công.')
            return redirect('employee:index')
    else:
        form = EmpInformationForm(instance=employee)
    return render(request, 'employee/edit_emp.html', {'form': form, 'employee': employee})

@login_required
@require_POST
def delete_employee(request, emp_id):
    employee = get_object_or_404(Emp_information, id=emp_id)
    employee.delete()
    messages.success(request, 'Nhân viên đã được xóa thành công.')
    return redirect('employee:index')
