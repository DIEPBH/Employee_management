# forms/imports.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, List, Dict
from django import forms


@dataclass(frozen=True)
class ExcelImportConfig:
    """
    Cấu hình chung cho import excel.
    - required_columns: các cột bắt buộc (lowercase)
    - accepted_extensions: mặc định .xlsx/.xlsm
    - max_size_mb: giới hạn size
    - sheet_name: nếu None => dùng sheet active
    """
    required_columns: Iterable[str]
    accepted_extensions: tuple[str, ...] = (".xlsx", ".xlsm")
    max_size_mb: int = 5
    sheet_name: Optional[str] = None


class ExcelImportForm(forms.Form):
    file = forms.FileField(required=True)

    def __init__(self, *args, config: ExcelImportConfig, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    def clean_file(self):
        f = self.cleaned_data["file"]
        name = (f.name or "").lower()

        if not name.endswith(self.config.accepted_extensions):
            raise forms.ValidationError(
                f"Chỉ hỗ trợ: {', '.join(self.config.accepted_extensions)}"
            )

        max_bytes = self.config.max_size_mb * 1024 * 1024
        if f.size > max_bytes:
            raise forms.ValidationError(f"File quá lớn (tối đa {self.config.max_size_mb}MB)")

        return f
