# views/import_base.py
from __future__ import annotations

from typing import Callable, Dict, Any
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from ..forms.imports import ExcelImportForm, ExcelImportConfig
from ..services.excel_utils import load_excel_sheet, validate_required_columns


Processor = Callable[..., Dict[str, Any]]  # returns dict JSON


@login_required
def excel_import_modal_view(
    request,
    *,
    config: ExcelImportConfig,
    template_form: str,
    processor: Processor,
    title: str = "Import Excel",
):
    # GET: render form
    if request.method == "GET":
        form = ExcelImportForm(config=config)
        html = render_to_string(template_form, {"form": form, "title": title}, request=request)
        return JsonResponse({"success": True, "html": html})

    # POST: validate file
    form = ExcelImportForm(request.POST, request.FILES, config=config)
    if not form.is_valid():
        html = render_to_string(template_form, {"form": form, "title": title}, request=request)
        return JsonResponse({"success": False, "html": html})

    f = form.cleaned_data["file"]

    # load + validate header
    sheet = load_excel_sheet(f, sheet_name=config.sheet_name)
    missing = validate_required_columns(sheet.col, list(config.required_columns))
    if missing:
        return JsonResponse({"success": False, "message": f"Thiếu cột bắt buộc: {', '.join(missing)}"})

    # xử lý nghiệp vụ riêng
    result = processor(rows=sheet.rows, col=sheet.col, request=request)
    # result nên chứa: success, message, imported, failed, errors...
    return JsonResponse(result)
