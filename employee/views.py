from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from employee.form import EmpInformationForm, EmpTitleForm, EmpPositionForm
from .models import Emp_information, Emp_Title, Emp_Position
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.db.models import Q, F, Count
from django.core.paginator import Paginator
from django.utils.http import urlencode
from urllib.parse import urlencode
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.

###########################################
############ Views quản lý cán bộ##########
###########################################
#index view hiển thị danh sách nhân viên với chức năng tìm kiếm và phân trang
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
            employees = employees.filter(gender=gender)
        # xử lý ngày tháng
        if dob:
            dob_date = None
            try:
                dob_date = datetime.strptime(dob, "%d/%m/%Y").date()
            except ValueError:
                pass
            if dob_date is None:
                try:
                    dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
                except ValueError:
                    pass
            # CHỈ lọc khi parse thành công
            if dob_date is not None:
                employees = employees.filter(day_of_birth=dob_date)

        paginator = Paginator(employees, 10)  # Hiển thị 10 nhân viên trên mỗi trang
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

# Thêm cán bộ mới vào hệ thống (1 màn add, 1 màn popup)
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
def add_employee_modal(request):
    if request.method == "POST":
        form = EmpInformationForm(request.POST, request.FILES)
        if form.is_valid():
            new_employee = form.save(commit=False)
            new_employee.created_by = request.user
            new_employee.created_at = datetime.now()
            new_employee.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "employee/employee_form.html",
            {"form": form,
             "post_url": reverse("employee:add_employee_modal"), "mode": "add"},
            request=request
        ) 
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpInformationForm()
    html = render_to_string(
        "employee/employee_form.html",
        {"form": form,
         "post_url": reverse("employee:add_employee_modal"), "mode": "add"},
        request=request
    )
    return JsonResponse({"success": True, "html": html})

#Chỉnh sửa thông tin cán bộ (1 màn edit, 1 màn popup)
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
def edit_employee_modal(request, emp_id):
    employee = get_object_or_404(Emp_information, id=emp_id)
    if request.method == "POST":
        form = EmpInformationForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "employee/employee_form.html",
            {"form": form,
             "post_url": reverse("employee:edit_employee_modal", args=[employee.id])},
            request=request
        ) 
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpInformationForm(instance=employee)
    html = render_to_string(
        "employee/employee_form.html",
        {"form": form,
         "post_url": reverse("employee:edit_employee_modal", args=[employee.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})


@login_required
@require_POST
def delete_employee(request, emp_id):
    employee = get_object_or_404(Emp_information, id=emp_id)
    employee.delete()
    messages.success(request, 'Nhân viên đã được xóa thành công.')
    return redirect('employee:index')


#####################################################
############ Views quản lý chức danh cán bộ##########
#####################################################

@login_required
def index_emp_tile(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        decision_number = request.GET.get('decision_number', '')
        decision_date = request.GET.get('decision_date', '').strip()
        # lọc dữ liệu theo tham số tìm kiếm
        emp_tile = Emp_Title.objects.select_related('emp').order_by('created_at')
        if emp_num:
            emp_tile = emp_tile.filter(emp__emp_num__icontains=emp_num)
        if full_name:
            emp_tile = emp_tile.filter(emp__full_name__icontains=full_name)
        if decision_number:
            emp_tile = emp_tile.filter(decision_number__icontains=decision_number)
        if decision_date:
            decision_date = None
            try:
                decision_date = datetime.strptime(decision_date, "%d/%m/%Y").date()
            except ValueError:
                pass
            if decision_date is None:
                try:
                    decision_date = datetime.strptime(decision_date, "%Y-%m-%d").date()
                except ValueError:
                    pass
            # CHỈ lọc khi parse thành công
            if decision_date is not None:
                emp_tile = emp_tile.filter(decision_date=decision_date)
        
        paginator = Paginator(emp_tile, 10)  # Hiển thị 10 dòng
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy()
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'title/index_emp_title.html', {'titles': page_obj, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring})

# Thêm chức danh mới cho cán bộ
    #API modal thêm chức danh
@login_required
def title_manager_modal(request):
    html = render_to_string("title/title_manager_modal.html", {}, request=request)
    return JsonResponse({"success": True, "html": html})

# employee/api.py
@login_required
def employee_lookup(request):
    q = (request.GET.get("q") or "").strip()

    qs = Emp_information.objects.all()
    if q:
        qs = qs.filter(Q(emp_num__icontains=q) | Q(full_name__icontains=q))

    qs = qs.order_by("emp_num")[:20]
    items = [{"code": e.emp_num, "name": e.full_name} for e in qs]
    return JsonResponse({"success": True, "items": items})

#submit form thêm chức danh cho cán bộ
@login_required
def emp_title_form(request):
    emp_num = request.GET.get("emp_num") or request.POST.get("emp_num")
    if not emp_num:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Thiếu mã cán bộ</div>"})
    try:
        emp  = Emp_information.objects.get(emp_num=emp_num)
    except Emp_information.DoesNotExist:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Cán bộ không tồn tại</div>"})
    
    if request.method == "POST":
        form = EmpTitleForm(request.POST, request.FILES)
        form.instance.emp = emp
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.emp = emp
            obj.is_active = 'Y'
            obj.save()
            return JsonResponse({"success": True})

        html = render_to_string("title/title_form.html", {"form": form, 
                                                          "emp_num": emp_num, 
                                                          "post_url": reverse("employee:emp_title_form"), "mode": "add"}, request=request)
        return JsonResponse({"success": False, "html": html, "errors": form.errors})

    form = EmpTitleForm(initial={"emp_num": emp_num})
    html = render_to_string("title/title_form.html", {"form": form, "emp_num": emp_num,
                                                       "post_url": reverse("employee:emp_title_form"), "mode": "add"}, request=request)
    return JsonResponse({"success": True, "html": html})

# API bảng chức danh của cán bộ
@login_required
def employee_titles_table(request, emp_num):
    qs = (
    Emp_Title.objects
    .select_related("emp_title")
    .filter(emp=emp_num)
    .order_by("-decision_date")
    )

    paginator = Paginator(qs, 10) # <-- đổi 10 dòng/trang 
    raw_page = request.GET.get("page", "1")
    try:
        page_number = int(raw_page)
    except (TypeError, ValueError):
        page_number = 1


    if page_number < 1:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    html = render_to_string("title/title_table.html",{"page_obj": page_obj, "emp_num": emp_num},request=request,)
    return JsonResponse({"success": True, "html": html})

# Sửa chức danh của cán bộ
@login_required #modal
def emp_title_edit_modal(request, id):
    title = get_object_or_404(Emp_Title, id=id)
    if request.method == "POST":
        form = EmpTitleForm(request.POST, request.FILES, instance=title)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "title/title_form.html",
            {"form": form,
             "post_url": reverse("employee:emp_title_edit_modal", args=[title.id])},
            request=request
        ) 
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpTitleForm(instance=title)
    html = render_to_string(
        "title/title_form.html",
        {"form": form,
         "post_url": reverse("employee:emp_title_edit_modal", args=[title.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})


#Xem chức danh của cán bộ:
@login_required
def emp_title_view_modal(request, id):
    title = get_object_or_404(Emp_Title, id=id)

    form = EmpTitleForm(instance=title)
    for field in form.fields.values():
        field.disabled = True
    html = render_to_string(
    "title/title_form.html",
    {
    "form": form,
    "mode": "view", # 👈 rất quan trọng
    },
    request=request
    )
    return JsonResponse({"success": True, "html": html})

# Xóa bản ghi chức danh:
@login_required
def emp_title_delete(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    title = get_object_or_404(Emp_Title, id=id)
    title.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return JsonResponse({"success": True})

@login_required #Xóa trên màn search
def emp_title_delete_(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    title = get_object_or_404(Emp_Title, id=id)
    title.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return redirect('employee:index_emp_tile')


###############################################################
############ Views quản lý quy hoạch chức danh cán bộ##########
###############################################################

@login_required
def index_emp_position(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        date_position = request.GET.get('date_position', '').strip()
        # lọc dữ liệu theo tham số tìm kiếm
        emp_position = Emp_Position.objects.select_related('emp').order_by('created_at')
        if emp_num:
            emp_position = emp_position.filter(emp__emp_num__icontains=emp_num)
        if full_name:
            emp_position = emp_position.filter(emp__full_name__icontains=full_name)
        
        if date_position:
            date_position = None
            try:
                date_position = datetime.strptime(date_position, "%d/%m/%Y").date()
            except ValueError:
                pass
            if date_position is None:
                try:
                    date_position = datetime.strptime(date_position, "%Y-%m-%d").date()
                except ValueError:
                    pass
            # CHỈ lọc khi parse thành công
            if date_position is not None:
                emp_position = emp_position.filter(date_position=date_position)
        
        paginator = Paginator(emp_position, 10)  # Hiển thị 10 dòng
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy()
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'position/index_emp_position.html', {'positions': page_obj, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring})

#Modal thêm quy hoạch cán bộ   
@login_required
def position_manager_modal(request):
    html = render_to_string("position/position_manager_modal.html", {}, request=request)
    return JsonResponse({"success": True, "html": html})

#submit form thêm quy hoạch chức danh cho cán bộ
@login_required
def emp_position_form(request):
    emp_num = request.GET.get("emp_num") or request.POST.get("emp_num")
    if not emp_num:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Thiếu mã cán bộ</div>"})
    try:
        emp  = Emp_information.objects.get(emp_num=emp_num)
    except Emp_information.DoesNotExist:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Cán bộ không tồn tại</div>"})
    
    if request.method == "POST":
        form = EmpPositionForm(request.POST, request.FILES)
        form.instance.emp = emp
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.emp = emp
            obj.is_active = 'Y'
            obj.save()
            return JsonResponse({"success": True})

        html = render_to_string("position/position_form.html", {"form": form, 
                                                          "emp_num": emp_num, 
                                                          "post_url": reverse("employee:emp_position_form"), "mode": "add"}, request=request)
        return JsonResponse({"success": False, "html": html, "errors": form.errors})

    form = EmpPositionForm(initial={"emp_num": emp_num})
    html = render_to_string("position/position_form.html", {"form": form, "emp_num": emp_num,
                                                       "post_url": reverse("employee:emp_position_form"), "mode": "add"}, request=request)
    return JsonResponse({"success": True, "html": html})

# API bảng quy hoạch chức danh của cán bộ
@login_required
def employee_position_table(request, emp_num):
    qs = (
    Emp_Position.objects
    .select_related("position")
    .filter(emp=emp_num)
    .order_by("-created_at")
    )

    paginator = Paginator(qs, 10) # <-- đổi 10 dòng/trang 
    raw_page = request.GET.get("page", "1")
    try:
        page_number = int(raw_page)
    except (TypeError, ValueError):
        page_number = 1


    if page_number < 1:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    html = render_to_string("position/position_table.html",{"page_obj": page_obj, "emp_num": emp_num},request=request,)
    return JsonResponse({"success": True, "html": html})