# views/emp_title_import.py
from __future__ import annotations

from django.utils import timezone
from django.db import transaction
from datetime import datetime, date
from decimal import Decimal, InvalidOperation

from .import_base import excel_import_modal_view
from ..forms.imports import ExcelImportConfig
from ..models import Emp_Title, Emp_information, position


def _parse_excel_date(v):
    if v is None or v == "":
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    if isinstance(v, str):
        s = v.strip()
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                pass
    return None


def _parse_decimal(v):
    if v is None or v == "":
        return None
    try:
        s = str(v).strip().replace(" ", "")
        if s.count(",") == 1 and s.count(".") == 0:
            s = s.replace(",", ".")
        else:
            s = s.replace(",", "")
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return None


def process_emp_title_import(*, rows, col, request):
    # bắt buộc có 1 trong: position_id/position_code/position_name
    pos_keys = ["position_id", "position_code", "position_name"]
    if not any(k in col for k in pos_keys):
        return {"success": False, "message": f"Thiếu cột chức danh: cần 1 trong {', '.join(pos_keys)}"}

    # preload emp
    emp_nums = [str(r[col["emp_num"]]).strip() for r in rows if r[col["emp_num"]] not in (None, "")]
    emp_map = {e.emp_num: e for e in Emp_information.objects.filter(emp_num__in=set(emp_nums))}

    ok, errors = 0, []

    with transaction.atomic():
        for row_idx, r in enumerate(rows, start=2):
            try:
                emp_num = str(r[col["emp_num"]]).strip() if r[col["emp_num"]] is not None else ""
                if not emp_num:
                    raise ValueError("Thiếu emp_num")
                emp_obj = emp_map.get(emp_num)
                if not emp_obj:
                    raise ValueError(f"Không tìm thấy cán bộ emp_num={emp_num}")

                # map position (ưu tiên id)
                pos_obj = None
                if "position_id" in col:
                    pid = r[col["position_id"]]
                    if pid in (None, ""):
                        raise ValueError("Thiếu position_id")
                    pos_obj = position.objects.filter(pk=int(pid)).first()
                    if not pos_obj:
                        raise ValueError(f"Không tìm thấy position_id={pid}")
                elif "position_code" in col:
                    code = str(r[col["position_code"]]).strip() if r[col["position_code"]] is not None else ""
                    if not code:
                        raise ValueError("Thiếu position_code")
                    # sửa field code theo model position của bạn
                    pos_obj = position.objects.filter(code=code).first()
                    if not pos_obj:
                        raise ValueError(f"Không tìm thấy position_code={code}")
                else:
                    name = str(r[col["position_name"]]).strip() if r[col["position_name"]] is not None else ""
                    if not name:
                        raise ValueError("Thiếu position_name")
                    # sửa field name theo model position của bạn
                    pos_obj = position.objects.filter(name=name).first()
                    if not pos_obj:
                        raise ValueError(f"Không tìm thấy position_name={name}")

                allowances = _parse_decimal(r[col["allowances"]])
                if allowances is None:
                    raise ValueError("allowances không hợp lệ / bị trống")

                date_of_receipt = _parse_excel_date(r[col["date_of_receipt"]])
                if not date_of_receipt:
                    raise ValueError("date_of_receipt không hợp lệ / bị trống")

                form_of_appointment = str(r[col["form_of_appointment"]]).strip() if r[col["form_of_appointment"]] is not None else ""
                if not form_of_appointment:
                    raise ValueError("form_of_appointment bị trống")

                decision_number = str(r[col["decision_number"]]).strip() if r[col["decision_number"]] is not None else ""
                if not decision_number:
                    raise ValueError("decision_number bị trống")

                decision_date = _parse_excel_date(r[col["decision_date"]])
                if not decision_date:
                    raise ValueError("decision_date không hợp lệ / bị trống")

                stop_decision_date = _parse_excel_date(r[col["stop_decision_date"]]) if "stop_decision_date" in col else None
                is_active = (str(r[col["is_active"]]).strip() if "is_active" in col and r[col["is_active"]] not in (None, "") else None)

                obj = Emp_Title(
                    emp=emp_obj,
                    emp_title=pos_obj,
                    allowances=allowances,
                    date_of_receipt=date_of_receipt,
                    form_of_appointment=form_of_appointment,
                    decision_number=decision_number,
                    decision_date=decision_date,
                    stop_decision_date=stop_decision_date,
                    is_active=is_active,
                    created_by=request.user,
                    update_by=request.user,
                    update_at=timezone.now(),
                )

                obj.full_clean()  # chạy clean() để bắt overlap
                obj.save()
                ok += 1

            except Exception as e:
                errors.append({"row": row_idx, "error": str(e)})

    return {
        "success": True,
        "imported": ok,
        "failed": len(errors),
        "errors": errors[:200],
        "message": f"Import xong: {ok} dòng OK, {len(errors)} dòng lỗi."
    }


def emp_title_import_modal(request):
    config = ExcelImportConfig(
        required_columns=[
            "emp_num",
            "allowances",
            "date_of_receipt",
            "form_of_appointment",
            "decision_number",
            "decision_date",
            # không bắt buộc stop/is_active
        ],
        sheet_name=None,  # hoặc "Titles"
    )
    return excel_import_modal_view(
        request,
        config=config,
        template_form="imports/excel_import_form.html",
        processor=process_emp_title_import,
        title="Import chức danh từ Excel",
    )
