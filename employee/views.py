from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from employee.form import EmpArmyForm, EmpDisciplineForm, EmpForeignForm, EmpHealthForm, EmpInformationForm, EmpTitleForm, EmpPositionForm, EmpPartyCommittee, EmpTraining, EmpWorkProcess, EmpSalaryProcess, EmpAwardForm, EmpRelationshipForm
from .models import Emp_Army, Emp_Foreign, Emp_Health, Emp_Training, Emp_information, Emp_Title, Emp_Position, Emp_PartyCommittee, Traning_level, committee, formality, Traning_level, Emp_workProcess, company, position, Emp_SalaryProcess, level, Emp_Awards, award_type, award_level, Emp_Discipline, Emp_Relationship, relationship_type
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
import logging
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
        logging.debug("emp: %r", emp)
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

# Sửa quy hoạch chức danh của cán bộ
@login_required #modal
def emp_position_edit_modal(request, id):
    position = get_object_or_404(Emp_Position, id=id)
    if request.method == "POST":
        form = EmpPositionForm(request.POST, request.FILES, instance=position)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "position/position_form.html",
            {"form": form,
             "post_url": reverse("employee:emp_position_edit_modal", args=[position.id])},
            request=request
        )
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpPositionForm(instance=position)
    html = render_to_string(
        "position/position_form.html",
        {"form": form,
         "post_url": reverse("employee:emp_position_edit_modal", args=[position.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})

#Xem quy hoạch chức danh của cán bộ:
@login_required
def emp_position_view_modal(request, id):
    position = get_object_or_404(Emp_Position, id=id)

    form = EmpPositionForm(instance=position)
    for field in form.fields.values():
        field.disabled = True
    html = render_to_string(
    "position/position_form.html",
    {
    "form": form,
    "mode": "view", 
    },
    request=request
    )
    return JsonResponse({"success": True, "html": html})

# Xóa bản ghi quy hoạch chức danh:
@login_required
def emp_position_delete(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    position = get_object_or_404(Emp_Position, id=id)
    position.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return JsonResponse({"success": True})

@login_required #Xóa trên màn search
def emp_position_delete_(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    position = get_object_or_404(Emp_Position, id=id)
    position.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return redirect('employee:index_emp_position')


#################################################################
############ Views quản lý thông tin cấp ủy đảng cán bộ##########
#################################################################

@login_required
def index_emp_party_committee(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        party_committee = request.GET.get('party_committee', '').strip()
        # lọc dữ liệu theo tham số tìm kiếm
        emp_party_committee = Emp_PartyCommittee.objects.select_related('emp', 'party_committee').order_by('created_at')
        committees = committee.objects.all()  # Lấy danh sách đảng ủy để hiển thị trong dropdown
        if emp_num:
            emp_party_committee = emp_party_committee.filter(emp__emp_num__icontains=emp_num)
        if full_name:
            emp_party_committee = emp_party_committee.filter(emp__full_name__icontains=full_name)
        if party_committee:
            emp_party_committee = emp_party_committee.filter(party_committee__id=party_committee)
        
        paginator = Paginator(emp_party_committee, 10)  # Hiển thị 10 dòng
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy() 
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'partycommittee/index_emp_partycommittee.html', {'page_obj': page_obj, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring, 'committees': committees})

#Modal thêm thông tin đảng ủy cán bộ   
@login_required
def party_committee_manager_modal(request):
    html = render_to_string("partycommittee/partycommittee_manager_modal.html", {}, request=request)
    return JsonResponse({"success": True, "html": html})

#submit form thêm thông tin đảng ủy cho cán bộ
@login_required
def emp_party_committee_form(request):
    emp_num = request.GET.get("emp_num") or request.POST.get("emp_num")
    if not emp_num:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Thiếu mã cán bộ</div>"})
    try:
        emp  = Emp_information.objects.get(emp_num=emp_num)
    except Emp_information.DoesNotExist:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Cán bộ không tồn tại</div>"})
    
    if request.method == "POST":
        form = EmpPartyCommittee(request.POST, request.FILES)
        form.instance.emp = emp
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.emp = emp
            obj.save()
            return JsonResponse({"success": True})

        html = render_to_string("partycommittee/partycommittee_form.html", {"form": form, 
                                                          "emp_num": emp_num, 
                                                          "post_url": reverse("employee:emp_party_committee_form"), "mode": "add"}, request=request)
        return JsonResponse({"success": False, "html": html, "errors": form.errors})

    form = EmpPartyCommittee(initial={"emp_num": emp_num})
    html = render_to_string("partycommittee/partycommittee_form.html", {"form": form, "emp_num": emp_num,
                                                       "post_url": reverse("employee:emp_party_committee_form"), "mode": "add"}, request=request)
    return JsonResponse({"success": True, "html": html})

# API bảng thông tin đảng ủy của cán bộ
@login_required
def employee_party_committee_table(request, emp_num):
    qs = (
    Emp_PartyCommittee.objects
    .select_related("party_committee")
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

    html = render_to_string("partycommittee/partycommittee_table.html",{"page_obj": page_obj, "emp_num": emp_num},request=request,)
    return JsonResponse({"success": True, "html": html})

# Sửa quy hoạch chức danh của cán bộ
@login_required #modal
def emp_party_committee_edit_modal(request, id):
    committee = get_object_or_404(Emp_PartyCommittee, id=id)
    if request.method == "POST":
        form = EmpPartyCommittee(request.POST, request.FILES, instance=committee)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "partycommittee/partycommittee_form.html",
            {"form": form,
             "post_url": reverse("employee:emp_party_committee_edit_modal", args=[committee.id])},
            request=request
        )
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpPartyCommittee(instance=committee)
    html = render_to_string(
        "partycommittee/partycommittee_form.html",
        {"form": form,
         "post_url": reverse("employee:emp_party_committee_edit_modal", args=[committee.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})

#Xem quy hoạch chức danh của cán bộ:
@login_required
def emp_party_committee_view_modal(request, id):
    committee = get_object_or_404(Emp_PartyCommittee, id=id)

    form = EmpPartyCommittee(instance=committee)
    for field in form.fields.values():
        field.disabled = True
    html = render_to_string(
    "partycommittee/partycommittee_form.html",
    {
    "form": form,
    "mode": "view", 
    },
    request=request
    )
    return JsonResponse({"success": True, "html": html})

# Xóa bản ghi quy hoạch chức danh:
@login_required
def emp_party_committee_delete(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    committee = get_object_or_404(Emp_PartyCommittee, id=id)
    committee.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return JsonResponse({"success": True})

@login_required #Xóa trên màn search
def emp_party_committee_delete_(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    committee = get_object_or_404(Emp_PartyCommittee, id=id)
    committee.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return redirect('employee:index_emp_party_committee')


#############################################################
############ Views quản lý thông tin đào tạo cán bộ##########
#############################################################

@login_required
def index_emp_training(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        formalitys = request.GET.get('formality', '').strip()
        level = request.GET.get('level', '').strip()
        # lọc dữ liệu theo tham số tìm kiếm
        emp_training = Emp_Training.objects.select_related('emp', 'formality', 'level').order_by('created_at')
        formality_list = formality.objects.all()  # Lấy danh sách hình thức đào tạo để hiển thị trong dropdown
        level_list = Traning_level.objects.all()  # Lấy danh sách cấp độ đào tạo để hiển thị trong dropdown
        if emp_num:
            emp_training = emp_training.filter(emp__emp_num__icontains=emp_num)
        if full_name:
            emp_training = emp_training.filter(emp__full_name__icontains=full_name)
        if formalitys:
            emp_training = emp_training.filter(formality__id=formalitys)
        if level:
            emp_training = emp_training.filter(level__id=level)
        
        paginator = Paginator(emp_training, 10)  # Hiển thị 10 dòng
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy() 
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'training/index_emp_training.html', {'emp_training': emp_training, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring, 'formality_list': formality_list, 'level_list': level_list})

#Modal thêm thông tin đào tạo cán bộ   
@login_required
def training_manager_modal(request):
    html = render_to_string("training/training_manager_modal.html", {}, request=request)
    return JsonResponse({"success": True, "html": html})

#submit form thêm thông tin đào tạo cho cán bộ
@login_required
def emp_training_form(request):
    emp_num = request.GET.get("emp_num") or request.POST.get("emp_num")
    if not emp_num:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Thiếu mã cán bộ</div>"})
    try:
        emp  = Emp_information.objects.get(emp_num=emp_num)
    except Emp_information.DoesNotExist:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Cán bộ không tồn tại</div>"})
    
    if request.method == "POST":
        form = EmpTraining(request.POST, request.FILES)
        form.instance.emp = emp
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.emp = emp
            obj.save()
            return JsonResponse({"success": True})

        html = render_to_string("training/training_form.html", {"form": form, 
                                                          "emp_num": emp_num, 
                                                          "post_url": reverse("employee:emp_training_form"), "mode": "add"}, request=request)
        return JsonResponse({"success": False, "html": html, "errors": form.errors})

    form = EmpTraining(initial={"emp_num": emp_num})
    html = render_to_string("training/training_form.html", {"form": form, "emp_num": emp_num,
                                                       "post_url": reverse("employee:emp_training_form"), "mode": "add"}, request=request)
    return JsonResponse({"success": True, "html": html})

# API bảng thông tin đào tạo của cán bộ
@login_required
def employee_training_table(request, emp_num):
    qs = (
    Emp_Training.objects
    .select_related("level")
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

    html = render_to_string("training/training_table.html",{"page_obj": page_obj, "emp_num": emp_num},request=request,)
    return JsonResponse({"success": True, "html": html})

# Sửa quy hoạch đào tạo của cán bộ
@login_required #modal
def emp_training_edit_modal(request, id):
    obj = get_object_or_404(Emp_Training, id=id)
    if request.method == "POST":
        form = EmpTraining(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "training/training_form.html",
            {"form": form,
             "post_url": reverse("employee:emp_training_edit_modal", args=[obj.id])},
            request=request
        )
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpTraining(instance=obj)
    html = render_to_string(
        "training/training_form.html",
        {"form": form,
         "post_url": reverse("employee:emp_training_edit_modal", args=[obj.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})

#Xem quy hoạch đào tạo của cán bộ:
@login_required
def emp_training_view_modal(request, id):
    obj = get_object_or_404(Emp_Training, id=id)

    form = EmpTraining(instance=obj)
    for field in form.fields.values():
        field.disabled = True
    html = render_to_string(
    "training/training_form.html",
    {
    "form": form,
    "mode": "view", 
    },
    request=request
    )
    return JsonResponse({"success": True, "html": html})

# Xóa bản ghi quy hoạch đào tạo:
@login_required
def emp_training_delete(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Training, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return JsonResponse({"success": True})

@login_required #Xóa trên màn search
def emp_training_delete_(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Training, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return redirect('employee:index_emp_training')


##############################################################
############ Views quản lý quá trình công tác cán bộ##########
##############################################################

@login_required
def index_emp_work_process(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        emp_company = request.GET.get('company', '').strip()
        emp_title = request.GET.get('title', '').strip()
        # lọc dữ liệu theo tham số tìm kiếm
        data = Emp_workProcess.objects.select_related('emp', 'emp_title', 'emp_company').order_by('created_at')
        title_list = position.objects.all()  # Lấy danh sách chức danh để hiển thị trong dropdown
        company_list = company.objects.all()  # Lấy danh sách công ty để hiển thị trong dropdown
        if emp_num:
            data = data.filter(emp__emp_num__icontains=emp_num)
        if full_name:
            data = data.filter(emp__full_name__icontains=full_name)
        if emp_company:
            data = data.filter(emp_company__id=emp_company)
        if emp_title:
            data = data.filter(emp_title__id=emp_title)
        
        paginator = Paginator(data, 10)  # Hiển thị 10 dòng
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy() 
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'workprocess/index_emp_workprocess.html', {'data': data, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring, 'title_list': title_list, 'company_list': company_list})

#Modal thêm thông tin đào tạo cán bộ   
@login_required
def workprocess_manager_modal(request):
    html = render_to_string("workprocess/workprocess_manager_modal.html", {}, request=request)
    return JsonResponse({"success": True, "html": html})

#submit form thêm thông tin quá trình công tác cho cán bộ
@login_required
def emp_workprocess_form(request):
    emp_num = request.GET.get("emp_num") or request.POST.get("emp_num")
    if not emp_num:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Thiếu mã cán bộ</div>"})
    try:
        emp  = Emp_information.objects.get(emp_num=emp_num)
    except Emp_information.DoesNotExist:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Cán bộ không tồn tại</div>"})
    
    if request.method == "POST":
        form = EmpWorkProcess(request.POST, request.FILES)
        form.instance.emp = emp
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.emp = emp
            obj.save()
            return JsonResponse({"success": True})

        html = render_to_string("workprocess/workprocess_form.html", {"form": form, 
                                                          "emp_num": emp_num, 
                                                          "post_url": reverse("employee:emp_workprocess_form"), "mode": "add"}, request=request)
        return JsonResponse({"success": False, "html": html, "errors": form.errors})

    form = EmpWorkProcess(initial={"emp_num": emp_num})
    html = render_to_string("workprocess/workprocess_form.html", {"form": form, "emp_num": emp_num,
                                                       "post_url": reverse("employee:emp_workprocess_form"), "mode": "add"}, request=request)
    return JsonResponse({"success": True, "html": html})

# API bảng thông tin quá trình công tác của cán bộ
@login_required
def employee_workprocess_table(request, emp_num):
    qs = (
    Emp_workProcess.objects
    .select_related("emp_company", "emp_title")
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

    html = render_to_string("workprocess/workprocess_table.html",{"page_obj": page_obj, "emp_num": emp_num},request=request,)
    return JsonResponse({"success": True, "html": html})

# Sửa quy hoạch quá trình công tác của cán bộ
@login_required #modal
def emp_workprocess_edit_modal(request, id):
    obj = get_object_or_404(Emp_workProcess, id=id)
    if request.method == "POST":
        form = EmpWorkProcess(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "workprocess/workprocess_form.html",
            {"form": form,
             "post_url": reverse("employee:emp_workprocess_edit_modal", args=[obj.id])},
            request=request
        )
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpWorkProcess(instance=obj)
    html = render_to_string(
        "workprocess/workprocess_form.html",
        {"form": form,
         "post_url": reverse("employee:emp_workprocess_edit_modal", args=[obj.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})

#Xem quy hoạch quá trình công tác của cán bộ:
@login_required
def emp_workprocess_view_modal(request, id):
    obj = get_object_or_404(Emp_workProcess, id=id)

    form = EmpWorkProcess(instance=obj)
    for field in form.fields.values():
        field.disabled = True
    html = render_to_string(
    "workprocess/workprocess_form.html",
    {
    "form": form,
    "mode": "view", 
    },
    request=request
    )
    return JsonResponse({"success": True, "html": html})

# Xóa bản ghi quy hoạch quá trình công tác:
@login_required
def emp_workprocess_delete(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_workProcess, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return JsonResponse({"success": True})

@login_required #Xóa trên màn search
def emp_workprocess_delete_(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_workProcess, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return redirect('employee:index_emp_work_process')


############################################################
############ Views quản lý quá trình lương cán bộ##########
############################################################

@login_required
def index_emp_salary_process(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        emp_level = request.GET.get('level', '').strip()
        decision_number = request.GET.get('decision_number', '').strip()
        # lọc dữ liệu theo tham số tìm kiếm
        data = Emp_SalaryProcess.objects.select_related('emp', 'level',).order_by('created_at')
        level_list = level.objects.all()  # Lấy danh sách chức danh để hiển thị trong dropdown
        if emp_num:
            data = data.filter(emp__emp_num__icontains=emp_num)
        if full_name:
            data = data.filter(emp__full_name__icontains=full_name)
        if emp_level:
            data = data.filter(emp_level__id=emp_level)
        if decision_number:
            data = data.filter(decision_number__icontains=decision_number)
        
        paginator = Paginator(data, 10)  # Hiển thị 10 dòng
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy() 
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'salaryprocess/index_emp_salaryprocess.html', {'data': data, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring, 'level_list': level_list})

#Modal thêm thông tin đào tạo cán bộ   
@login_required
def salaryprocess_manager_modal(request):
    html = render_to_string("salaryprocess/salaryprocess_manager_modal.html", {}, request=request)
    return JsonResponse({"success": True, "html": html})

#submit form thêm thông tin quá trình công tác cho cán bộ
@login_required
def emp_salaryprocess_form(request):
    emp_num = request.GET.get("emp_num") or request.POST.get("emp_num")
    if not emp_num:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Thiếu mã cán bộ</div>"})
    try:
        emp  = Emp_information.objects.get(emp_num=emp_num)
    except Emp_information.DoesNotExist:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Cán bộ không tồn tại</div>"})
    
    if request.method == "POST":
        form = EmpSalaryProcess(request.POST, request.FILES)
        form.instance.emp = emp
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.emp = emp
            obj.save()
            return JsonResponse({"success": True})

        html = render_to_string("salaryprocess/salaryprocess_form.html", {"form": form, 
                                                          "emp_num": emp_num, 
                                                          "post_url": reverse("employee:emp_salaryprocess_form"), "mode": "add"}, request=request)
        return JsonResponse({"success": False, "html": html, "errors": form.errors})

    form = EmpSalaryProcess(initial={"emp_num": emp_num})
    html = render_to_string("salaryprocess/salaryprocess_form.html", {"form": form, "emp_num": emp_num,
                                                       "post_url": reverse("employee:emp_salaryprocess_form"), "mode": "add"}, request=request)
    return JsonResponse({"success": True, "html": html})

# API bảng thông tin quá trình công tác của cán bộ
@login_required
def employee_salaryprocess_table(request, emp_num):
    qs = (
    Emp_SalaryProcess.objects
    .select_related("level")
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

    html = render_to_string("salaryprocess/salaryprocess_table.html",{"page_obj": page_obj, "emp_num": emp_num},request=request,)
    return JsonResponse({"success": True, "html": html})

# Sửa quy hoạch quá trình công tác của cán bộ
@login_required #modal
def emp_salaryprocess_edit_modal(request, id):
    obj = get_object_or_404(Emp_SalaryProcess, id=id)
    if request.method == "POST":
        form = EmpSalaryProcess(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "salaryprocess/salaryprocess_form.html",
            {"form": form,
             "post_url": reverse("employee:emp_salaryprocess_edit_modal", args=[obj.id])},
            request=request
        )
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpSalaryProcess(instance=obj)
    html = render_to_string(
        "salaryprocess/salaryprocess_form.html",
        {"form": form,
         "post_url": reverse("employee:emp_salaryprocess_edit_modal", args=[obj.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})

#Xem quy hoạch quá trình công tác của cán bộ:
@login_required
def emp_salaryprocess_view_modal(request, id):
    obj = get_object_or_404(Emp_SalaryProcess, id=id)

    form = EmpSalaryProcess(instance=obj)
    for field in form.fields.values():
        field.disabled = True
    html = render_to_string(
    "salaryprocess/salaryprocess_form.html",
    {
    "form": form,
    "mode": "view", 
    },
    request=request
    )
    return JsonResponse({"success": True, "html": html})

# Xóa bản ghi quy hoạch quá trình công tác:
@login_required
def emp_salaryprocess_delete(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_SalaryProcess, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return JsonResponse({"success": True})

@login_required #Xóa trên màn search
def emp_salaryprocess_delete_(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_SalaryProcess, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return redirect('employee:index_emp_salary_process')

#######################################################
############ Views quản lý khen thưởng cán bộ##########
#######################################################

@login_required
def index_emp_award(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        emp_award_type = request.GET.get('award_type', '').strip()
        emp_award_level = request.GET.get('award_level', '').strip()
        # lọc dữ liệu theo tham số tìm kiếm
        data = Emp_Awards.objects.select_related('emp', 'award_type', 'award_level').order_by('created_at')
        award_type_list = award_type.objects.all()  # Lấy danh sách loại khen thưởng để hiển thị trong dropdown
        award_level_list = award_level.objects.all()  # Lấy danh sách cấp khen thưởng để hiển thị trong dropdown
        if emp_num:
            data = data.filter(emp__emp_num__icontains=emp_num)
        if full_name:
            data = data.filter(emp__full_name__icontains=full_name)
        if emp_award_type:
            data = data.filter(award_type__id=emp_award_type)
        if emp_award_level:
            data = data.filter(award_level__id=emp_award_level)
        
        paginator = Paginator(data, 10)  # Hiển thị 10 dòng
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy() 
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'award/index_emp_award.html', {'data': data, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring, 'award_type_list': award_type_list, 'award_level_list': award_level_list})

#Modal thêm thông tin khen thưởng cán bộ   
@login_required
def award_manager_modal(request):
    html = render_to_string("award/award_manager_modal.html", {}, request=request)
    return JsonResponse({"success": True, "html": html})

#submit form thêm thông tin khen thưởng cho cán bộ
@login_required
def emp_award_form(request):
    emp_num = request.GET.get("emp_num") or request.POST.get("emp_num")
    if not emp_num:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Thiếu mã cán bộ</div>"})
    try:
        emp  = Emp_information.objects.get(emp_num=emp_num)
    except Emp_information.DoesNotExist:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Cán bộ không tồn tại</div>"})
    
    if request.method == "POST":
        form = EmpAwardForm(request.POST, request.FILES)
        form.instance.emp = emp
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.emp = emp
            obj.save()
            return JsonResponse({"success": True})

        html = render_to_string("award/award_form.html", {"form": form, 
                                                          "emp_num": emp_num, 
                                                          "post_url": reverse("employee:emp_award_form"), "mode": "add"}, request=request)
        return JsonResponse({"success": False, "html": html, "errors": form.errors})

    form = EmpAwardForm(initial={"emp_num": emp_num})
    html = render_to_string("award/award_form.html", {"form": form, "emp_num": emp_num,
                                                       "post_url": reverse("employee:emp_award_form"), "mode": "add"}, request=request)
    return JsonResponse({"success": True, "html": html})

# API bảng thông tin khen thưởng của cán bộ
@login_required
def employee_award_table(request, emp_num):
    qs = (
    Emp_Awards.objects
    .select_related("award_type", "award_level")
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

    html = render_to_string("award/award_table.html",{"page_obj": page_obj, "emp_num": emp_num},request=request,)
    return JsonResponse({"success": True, "html": html})

# Sửa quy hoạch quá trình công tác của cán bộ
@login_required #modal
def emp_award_edit_modal(request, id):
    obj = get_object_or_404(Emp_Awards, id=id)
    if request.method == "POST":
        form = EmpAwardForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "award/award_form.html",
            {"form": form,
             "post_url": reverse("employee:emp_award_edit_modal", args=[obj.id])},
            request=request
        )
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpAwardForm(instance=obj)
    html = render_to_string(
        "award/award_form.html",
        {"form": form,
         "post_url": reverse("employee:emp_award_edit_modal", args=[obj.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})

#Xem quy hoạch quá trình công tác của cán bộ:
@login_required
def emp_award_view_modal(request, id):
    obj = get_object_or_404(Emp_Awards, id=id)

    form = EmpAwardForm(instance=obj)
    for field in form.fields.values():
        field.disabled = True
    html = render_to_string(
    "award/award_form.html",
    {
    "form": form,
    "mode": "view", 
    },
    request=request
    )
    return JsonResponse({"success": True, "html": html})

# Xóa bản ghi khen thưởng của cán bộ:
@login_required
def emp_award_delete(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Awards, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return JsonResponse({"success": True})

@login_required #Xóa trên màn search
def emp_award_delete_(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Awards, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return redirect('employee:index_emp_award')


###################################################
############ Views quản lý kỷ luật cán bộ##########
###################################################

@login_required
def index_emp_discipline(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        # lọc dữ liệu theo tham số tìm kiếm
        data = Emp_Discipline.objects.select_related('emp').order_by('created_at')
        if emp_num:
            data = data.filter(emp__emp_num__icontains=emp_num)
        if full_name:
            data = data.filter(emp__full_name__icontains=full_name)
        
        paginator = Paginator(data, 10)  # Hiển thị 10 dòng
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy() 
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'discipline/index_emp_discipline.html', {'data': data, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring})

#Modal thêm thông tin kỷ luật cán bộ   
@login_required
def discipline_manager_modal(request):
    html = render_to_string("discipline/discipline_manager_modal.html", {}, request=request)
    return JsonResponse({"success": True, "html": html})

#submit form thêm thông tin kỷ luật cho cán bộ
@login_required
def emp_discipline_form(request):
    emp_num = request.GET.get("emp_num") or request.POST.get("emp_num")
    if not emp_num:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Thiếu mã cán bộ</div>"})
    try:
        emp  = Emp_information.objects.get(emp_num=emp_num)
    except Emp_information.DoesNotExist:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Cán bộ không tồn tại</div>"})
    
    if request.method == "POST":
        form = EmpDisciplineForm(request.POST, request.FILES)
        form.instance.emp = emp
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.emp = emp
            obj.save()
            return JsonResponse({"success": True})

        html = render_to_string("discipline/discipline_form.html", {"form": form, 
                                                          "emp_num": emp_num, 
                                                          "post_url": reverse("employee:emp_discipline_form"), "mode": "add"}, request=request)
        return JsonResponse({"success": False, "html": html, "errors": form.errors})

    form = EmpDisciplineForm(initial={"emp_num": emp_num})
    html = render_to_string("discipline/discipline_form.html", {"form": form, "emp_num": emp_num,
                                                       "post_url": reverse("employee:emp_discipline_form"), "mode": "add"}, request=request)
    return JsonResponse({"success": True, "html": html})

# API bảng thông tin kỷ luật của cán bộ
@login_required
def employee_discipline_table(request, emp_num):
    qs = (
    Emp_Discipline.objects
    .select_related("emp")
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

    html = render_to_string("discipline/discipline_table.html",{"page_obj": page_obj, "emp_num": emp_num},request=request,)
    return JsonResponse({"success": True, "html": html})

# Sửa quy hoạch quá trình công tác của cán bộ
@login_required #modal
def emp_discipline_edit_modal(request, id):
    obj = get_object_or_404(Emp_Discipline, id=id)
    if request.method == "POST":
        form = EmpDisciplineForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "discipline/discipline_form.html",
            {"form": form,
             "post_url": reverse("employee:emp_discipline_edit_modal", args=[obj.id])},
            request=request
        )
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpDisciplineForm(instance=obj)
    html = render_to_string(
        "discipline/discipline_form.html",
        {"form": form,
         "post_url": reverse("employee:emp_discipline_edit_modal", args=[obj.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})

#Xem quy hoạch quá trình công tác của cán bộ:
@login_required
def emp_discipline_view_modal(request, id):
    obj = get_object_or_404(Emp_Discipline, id=id)

    form = EmpDisciplineForm(instance=obj)
    for field in form.fields.values():
        field.disabled = True
    html = render_to_string(
    "discipline/discipline_form.html",
    {
    "form": form,
    "mode": "view", 
    },
    request=request
    )
    return JsonResponse({"success": True, "html": html})

# Xóa bản ghi kỷ luật của cán bộ:
@login_required
def emp_discipline_delete(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Discipline, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return JsonResponse({"success": True})

@login_required #Xóa trên màn search
def emp_discipline_delete_(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Discipline, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return redirect('employee:index_emp_discipline')


#####################################################
############ Views quản lý thân nhân cán bộ##########
#####################################################

@login_required
def index_emp_relationship(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        emp_relationship_type = request.GET.get('relationship_type', '').strip()
        # lọc dữ liệu theo tham số tìm kiếm
        data = Emp_Relationship.objects.select_related('emp', 'relationship_type').order_by('created_at')
        relationship_type_list = relationship_type.objects.all()  # Lấy danh sách loại thân nhân để hiển thị trong dropdown
        if emp_num:
            data = data.filter(emp__emp_num__icontains=emp_num)
        if full_name:
            data = data.filter(emp__full_name__icontains=full_name)
        if emp_relationship_type:
            data = data.filter(relationship_type__id=emp_relationship_type)
        
        paginator = Paginator(data, 10)  # Hiển thị 10 dòng
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy() 
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'relationship/index_emp_relationship.html', {'data': data, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring, 'relationship_type_list': relationship_type_list})

#Modal thêm thông tin thân nhân cán bộ   
@login_required
def relationship_manager_modal(request):
    html = render_to_string("relationship/relationship_manager_modal.html", {}, request=request)
    return JsonResponse({"success": True, "html": html})

#submit form thêm thông tin thân nhân cho cán bộ
@login_required
def emp_relationship_form(request):
    emp_num = request.GET.get("emp_num") or request.POST.get("emp_num")
    if not emp_num:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Thiếu mã cán bộ</div>"})
    try:
        emp  = Emp_information.objects.get(emp_num=emp_num)
    except Emp_information.DoesNotExist:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Cán bộ không tồn tại</div>"})
    
    if request.method == "POST":
        form = EmpRelationshipForm(request.POST, request.FILES)
        form.instance.emp = emp
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.emp = emp
            obj.save()
            return JsonResponse({"success": True})

        html = render_to_string("relationship/relationship_form.html", {"form": form, 
                                                          "emp_num": emp_num, 
                                                          "post_url": reverse("employee:emp_relationship_form"), "mode": "add"}, request=request)
        return JsonResponse({"success": False, "html": html, "errors": form.errors})

    form = EmpRelationshipForm(initial={"emp_num": emp_num})
    html = render_to_string("relationship/relationship_form.html", {"form": form, "emp_num": emp_num,
                                                       "post_url": reverse("employee:emp_relationship_form"), "mode": "add"}, request=request)
    return JsonResponse({"success": True, "html": html})

# API bảng thông tin thân nhân của cán bộ
@login_required
def employee_relationship_table(request, emp_num):
    qs = (
    Emp_Relationship.objects
    .select_related("relationship_type")
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

    html = render_to_string("relationship/relationship_table.html",{"page_obj": page_obj, "emp_num": emp_num},request=request,)
    return JsonResponse({"success": True, "html": html})

# Sửa thông tin thân nhân cán bộ
@login_required #modal
def emp_relationship_edit_modal(request, id):
    obj = get_object_or_404(Emp_Relationship, id=id)
    if request.method == "POST":
        form = EmpRelationshipForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "relationship/relationship_form.html",
            {"form": form,
             "post_url": reverse("employee:emp_relationship_edit_modal", args=[obj.id])},
            request=request
        )
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpRelationshipForm(instance=obj)
    html = render_to_string(
        "relationship/relationship_form.html",
        {"form": form,
         "post_url": reverse("employee:emp_relationship_edit_modal", args=[obj.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})

#Xem quy thông tin thân nhân cán bộ:
@login_required
def emp_relationship_view_modal(request, id):
    obj = get_object_or_404(Emp_Relationship, id=id)

    form = EmpRelationshipForm(instance=obj)
    for field in form.fields.values():
        field.disabled = True
    html = render_to_string(
    "relationship/relationship_form.html",
    {
    "form": form,
    "mode": "view", 
    },
    request=request
    )
    return JsonResponse({"success": True, "html": html})

# Xóa bản ghi thân nhân của cán bộ:
@login_required
def emp_relationship_delete(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Relationship, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return JsonResponse({"success": True})

@login_required #Xóa trên màn search
def emp_relationship_delete_(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Relationship, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return redirect('employee:index_emp_relationship')

###################################################################
############ Views quản lý thông tin ra nước ngoài cán bộ##########
###################################################################

@login_required
def index_emp_foreign(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        fromdate = request.GET.get('fromdate', '').strip()
        todate = request.GET.get('todate', '').strip()
        # lọc dữ liệu theo tham số tìm kiếm
        data = Emp_Foreign.objects.select_related('emp').order_by('created_at')
        if emp_num:
            data = data.filter(emp__emp_num__icontains=emp_num)
        if full_name:
            data = data.filter(emp__full_name__icontains=full_name)
        if fromdate:
            from_date = None
            try:
                from_date = datetime.strptime(fromdate, "%d/%m/%Y").date()
            except ValueError:
                pass
            if from_date is None:
                try:
                    from_date = datetime.strptime(fromdate, "%Y-%m-%d").date()
                except ValueError:
                    pass
            if from_date is not None:
                data = data.filter(from_date__gte=from_date)
        if todate:
            to_date = None
            try:
                to_date = datetime.strptime(todate, "%d/%m/%Y").date()
            except ValueError:
                pass
            if to_date is None:
                try:
                    to_date = datetime.strptime(todate, "%Y-%m-%d").date()
                except ValueError:
                    pass
            if to_date is not None:
                data = data.filter(to_date__lte=to_date)

        paginator = Paginator(data, 10)  # Hiển thị 10 dòng
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy() 
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'foreign/index_emp_foreign.html', {'data': data, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring})

#Modal thêm thông tin thân nhân cán bộ   
@login_required
def foreign_manager_modal(request):
    html = render_to_string("foreign/foreign_manager_modal.html", {}, request=request)
    return JsonResponse({"success": True, "html": html})

#submit form thêm thông tin thân nhân cho cán bộ
@login_required
def emp_foreign_form(request):
    emp_num = request.GET.get("emp_num") or request.POST.get("emp_num")
    if not emp_num:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Thiếu mã cán bộ</div>"})
    try:
        emp  = Emp_information.objects.get(emp_num=emp_num)
    except Emp_information.DoesNotExist:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Cán bộ không tồn tại</div>"})
    
    if request.method == "POST":
        form = EmpForeignForm(request.POST, request.FILES)
        form.instance.emp = emp
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.emp = emp
            obj.save()
            return JsonResponse({"success": True})

        html = render_to_string("foreign/foreign_form.html", {"form": form, 
                                                          "emp_num": emp_num, 
                                                          "post_url": reverse("employee:emp_foreign_form"), "mode": "add"}, request=request)
        return JsonResponse({"success": False, "html": html, "errors": form.errors})

    form = EmpForeignForm(initial={"emp_num": emp_num})
    html = render_to_string("foreign/foreign_form.html", {"form": form, "emp_num": emp_num,
                                                       "post_url": reverse("employee:emp_foreign_form"), "mode": "add"}, request=request)
    return JsonResponse({"success": True, "html": html})

# API bảng thông tin thân nhân của cán bộ
@login_required
def employee_foreign_table(request, emp_num):
    qs = (
    Emp_Foreign.objects
    .select_related("emp")
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

    html = render_to_string("foreign/foreign_table.html",{"page_obj": page_obj, "emp_num": emp_num},request=request,)
    return JsonResponse({"success": True, "html": html})

# Sửa thông tin thân nhân cán bộ
@login_required #modal
def emp_foreign_edit_modal(request, id):
    obj = get_object_or_404(Emp_Foreign, id=id)
    if request.method == "POST":
        form = EmpForeignForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "foreign/foreign_form.html",
            {"form": form,
             "post_url": reverse("employee:emp_foreign_edit_modal", args=[obj.id])},
            request=request
        )
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpForeignForm(instance=obj)
    html = render_to_string(
        "foreign/foreign_form.html",
        {"form": form,
         "post_url": reverse("employee:emp_foreign_edit_modal", args=[obj.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})

#Xem quy thông tin thân nhân cán bộ:
@login_required
def emp_foreign_view_modal(request, id):
    obj = get_object_or_404(Emp_Foreign, id=id)

    form = EmpForeignForm(instance=obj)
    for field in form.fields.values():
        field.disabled = True
    html = render_to_string(
    "foreign/foreign_form.html",
    {
    "form": form,
    "mode": "view", 
    },
    request=request
    )
    return JsonResponse({"success": True, "html": html})

# Xóa bản ghi thân nhân của cán bộ:
@login_required
def emp_foreign_delete(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Foreign, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return JsonResponse({"success": True})

@login_required #Xóa trên màn search
def emp_foreign_delete_(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Foreign, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return redirect('employee:index_emp_foreign')

##############################################################
############ Views quản lý thông tin nhập ngũ cán bộ##########
##############################################################

@login_required
def index_emp_army(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        datejoin = request.GET.get('datejoin', '').strip()
        dateout = request.GET.get('dateout', '').strip()
        # lọc dữ liệu theo tham số tìm kiếm
        data = Emp_Army.objects.select_related('emp').order_by('created_at')
        if emp_num:
            data = data.filter(emp__emp_num__icontains=emp_num)
        if full_name:
            data = data.filter(emp__full_name__icontains=full_name)
        if datejoin:
            date_join = None
            try:
                date_join = datetime.strptime(datejoin, "%d/%m/%Y").date()
            except ValueError:
                pass
            if date_join is None:
                try:
                    date_join = datetime.strptime(datejoin, "%Y-%m-%d").date()
                except ValueError:
                    pass
            if date_join is not None:
                data = data.filter(from_date__gte=date_join)
        if dateout:
            date_out = None
            try:
                date_out = datetime.strptime(dateout, "%d/%m/%Y").date()
            except ValueError:
                pass
            if date_out is None:
                try:
                    date_out = datetime.strptime(dateout, "%Y-%m-%d").date()
                except ValueError:
                    pass
            if date_out is not None:
                data = data.filter(to_date__lte=date_out)

        paginator = Paginator(data, 10)  # Hiển thị 10 dòng
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy() 
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'army/index_emp_army.html', {'data': data, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring})

#Modal thêm thông tin thân nhân cán bộ   
@login_required
def army_manager_modal(request):
    html = render_to_string("army/army_manager_modal.html", {}, request=request)
    return JsonResponse({"success": True, "html": html})

#submit form thêm thông tin thân nhân cho cán bộ
@login_required
def emp_army_form(request):
    emp_num = request.GET.get("emp_num") or request.POST.get("emp_num")
    if not emp_num:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Thiếu mã cán bộ</div>"})
    try:
        emp  = Emp_information.objects.get(emp_num=emp_num)
    except Emp_information.DoesNotExist:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Cán bộ không tồn tại</div>"})
    
    if request.method == "POST":
        form = EmpArmyForm(request.POST, request.FILES)
        form.instance.emp = emp
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.emp = emp
            obj.save()
            return JsonResponse({"success": True})

        html = render_to_string("army/army_form.html", {"form": form, 
                                                          "emp_num": emp_num, 
                                                          "post_url": reverse("employee:emp_army_form"), "mode": "add"}, request=request)
        return JsonResponse({"success": False, "html": html, "errors": form.errors})

    form = EmpArmyForm(initial={"emp_num": emp_num})
    html = render_to_string("army/army_form.html", {"form": form, "emp_num": emp_num,
                                                       "post_url": reverse("employee:emp_army_form"), "mode": "add"}, request=request)
    return JsonResponse({"success": True, "html": html})

# API bảng thông tin thân nhân của cán bộ
@login_required
def employee_army_table(request, emp_num):
    qs = (
    Emp_Army.objects
    .select_related("emp")
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

    html = render_to_string("army/army_table.html",{"page_obj": page_obj, "emp_num": emp_num},request=request,)
    return JsonResponse({"success": True, "html": html})

# Sửa thông tin thân nhân cán bộ
@login_required #modal
def emp_army_edit_modal(request, id):
    obj = get_object_or_404(Emp_Army, id=id)
    if request.method == "POST":
        form = EmpArmyForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "army/army_form.html",
            {"form": form,
             "post_url": reverse("employee:emp_army_edit_modal", args=[obj.id])},
            request=request
        )
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpArmyForm(instance=obj)
    html = render_to_string(
        "army/army_form.html",
        {"form": form,
         "post_url": reverse("employee:emp_army_edit_modal", args=[obj.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})

#Xem quy thông tin thân nhân cán bộ:
@login_required
def emp_army_view_modal(request, id):
    obj = get_object_or_404(Emp_Army, id=id)

    form = EmpArmyForm(instance=obj)
    for field in form.fields.values():
        field.disabled = True
    html = render_to_string(
    "army/army_form.html",
    {
    "form": form,
    "mode": "view", 
    },
    request=request
    )
    return JsonResponse({"success": True, "html": html})

# Xóa bản ghi thân nhân của cán bộ:
@login_required
def emp_army_delete(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Army, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return JsonResponse({"success": True})

@login_required #Xóa trên màn search
def emp_army_delete_(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Army, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return redirect('employee:index_emp_army')


##############################################################
############ Views quản lý thông tin sức khỏe cán bộ##########
##############################################################

@login_required
def index_emp_health(request):
    if request.user.is_authenticated:
        # tham số tìm kiếm
        emp_num = request.GET.get('emp_num', '')
        full_name = request.GET.get('full_name', '')
        datecheck = request.GET.get('datecheck', '').strip()
        # lọc dữ liệu theo tham số tìm kiếm
        data = Emp_Health.objects.select_related('emp').order_by('created_at')
        if emp_num:
            data = data.filter(emp__emp_num__icontains=emp_num)
        if full_name:
            data = data.filter(emp__full_name__icontains=full_name)
        if datecheck:
            date = None
            try:
                date = datetime.strptime(datecheck, "%d/%m/%Y").date()
            except ValueError:
                pass
            if date is None:
                try:
                    date = datetime.strptime(datecheck, "%Y-%m-%d").date()
                except ValueError:
                    pass
            if date is not None:
                data = data.filter(date_check__gte=date)
        paginator = Paginator(data, 10)  # Hiển thị 10 dòng
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Giữ nguyên các tham số tìm kiếm khi phân trang
        params = request.GET.copy() 
        params.pop("page", None)  # bỏ page cũ
        for k in list(params.keys()):
            if not (params.get(k) or "").strip():
                params.pop(k, None)
        querystring = urlencode(params)

        return render(request, 'Health/index_emp_health.html', {'data': data, 'page_obj': page_obj, 'paginator': paginator, 'querystring': querystring})

#Modal thêm thông tin sức khỏe cán bộ   
@login_required
def health_manager_modal(request):
    html = render_to_string("Health/health_manager_modal.html", {}, request=request)
    return JsonResponse({"success": True, "html": html})

#submit form thêm thông tin sức khỏe cho cán bộ
@login_required
def emp_health_form(request):
    emp_num = request.GET.get("emp_num") or request.POST.get("emp_num")
    if not emp_num:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Thiếu mã cán bộ</div>"})
    try:
        emp  = Emp_information.objects.get(emp_num=emp_num)
    except Emp_information.DoesNotExist:
        return JsonResponse({"success": False, "html": "<div class='alert alert-danger'>Cán bộ không tồn tại</div>"})
    
    if request.method == "POST":
        form = EmpHealthForm(request.POST, request.FILES)
        form.instance.emp = emp
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = datetime.now()
            obj.emp = emp
            obj.save()
            return JsonResponse({"success": True})

        html = render_to_string("Health/health_form.html", {"form": form, 
                                                          "emp_num": emp_num, 
                                                          "post_url": reverse("employee:emp_health_form"), "mode": "add"}, request=request)
        return JsonResponse({"success": False, "html": html, "errors": form.errors})

    form = EmpHealthForm(initial={"emp_num": emp_num})
    html = render_to_string("Health/health_form.html", {"form": form, "emp_num": emp_num,
                                                       "post_url": reverse("employee:emp_health_form"), "mode": "add"}, request=request)
    return JsonResponse({"success": True, "html": html})

# API bảng thông tin sức khỏe của cán bộ
@login_required
def employee_health_table(request, emp_num):
    qs = (
    Emp_Health.objects
    .select_related("emp")
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

    html = render_to_string("Health/health_table.html",{"page_obj": page_obj, "emp_num": emp_num},request=request,)
    return JsonResponse({"success": True, "html": html})

# Sửa thông tin sức khỏe cán bộ
@login_required #modal
def emp_health_edit_modal(request, id):
    obj = get_object_or_404(Emp_Health, id=id)
    if request.method == "POST":
        form = EmpHealthForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})

        html = render_to_string(
            "Health/health_form.html",
            {"form": form,
             "post_url": reverse("employee:emp_health_edit_modal", args=[obj.id])},
            request=request
        )
        return JsonResponse({"success": False, "html": html})
    # GET
    form = EmpHealthForm(instance=obj)
    html = render_to_string(
        "Health/health_form.html",
        {"form": form,
         "post_url": reverse("employee:emp_health_edit_modal", args=[obj.id])},
        request=request
    )
    return JsonResponse({"success": True, "html": html})

#Xem quy thông tin sức khỏe cán bộ:
@login_required
def emp_health_view_modal(request, id):
    obj = get_object_or_404(Emp_Health, id=id)

    form = EmpHealthForm(instance=obj)
    for field in form.fields.values():
        field.disabled = True
    html = render_to_string(
    "Health/health_form.html",
    {
    "form": form,
    "mode": "view", 
    },
    request=request
    )
    return JsonResponse({"success": True, "html": html})

# Xóa bản ghi sức khỏe của cán bộ:
@login_required
def emp_health_delete(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Health, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return JsonResponse({"success": True})

@login_required #Xóa trên màn search
def emp_health_delete_(request, id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    obj = get_object_or_404(Emp_Health, id=id)
    obj.delete()
    messages.success(request, 'Bản ghi đã được xóa thành công.')
    return redirect('employee:index_emp_health')