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
from django.core.paginator import Paginator
from django.utils.http import urlencode
from urllib.parse import urlencode
# Create your views here.

@login_required
def index(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        hometown = request.GET.get('hometown', '')
        dob = request.GET.get('dob', '').strip()
        gender = request.GET.get('gender', '')
        # lọc dữ liệu theo tham số tìm kiếm
        

        employees = Emp_information.objects.all()
        if emp_num:
            employees = employees.filter(emp_num__icontains=emp_num)
        if full_name:
            employees = employees.filter(full_name__icontains=full_name)
        if hometown:
            employees = employees.filter(place_of_hometown__icontains=hometown)
        if gender:
            employees = employees = employees.filter(gender=gender)
        
        if dob:
            dob_date = None

            # dd/mm/yyyy
            try:
                dob_date = datetime.strptime(dob, "%d/%m/%Y").date()
            except ValueError:
                pass

            # yyyy-mm-dd (nếu đôi lúc browser gửi dạng này)
            if dob_date is None:
                try:
                    dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
                except ValueError:
                    pass

            # CHỈ lọc khi parse thành công
            if dob_date is not None:
                employees = employees.filter(day_of_birth=dob_date)

        paginator = Paginator(employees, 1)  # Hiển thị 1 nhân viên trên mỗi trang
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy()
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'employee/index.html', {'employees': page_obj, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring})

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
