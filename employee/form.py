from django import forms
from .models import Emp_information,Emp_Title
from datetime import datetime
from django.core.exceptions import ValidationError

#forms quản lý thông tin cán bộ
class EmpInformationForm(forms.ModelForm):
    class Meta:
        model = Emp_information
        fields = ['emp_num','full_name','current_name','day_of_birth','gender','place_of_hometown','current_residence','nation','religion',
                  'family_job','before_job','date_in_group','union','day_of_joining_the_party','day_offical',
                'recruitment_day','date_of_joining_the_police','recruitment_place','recruitment_source','blood_type',
                'appellation','keep_records','forte_ability','Descriptions','avatar']
        widgets = {
            'day_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_in_group': forms.DateInput(attrs={'type': 'date'}),
            'day_of_joining_the_party': forms.DateInput(attrs={'type': 'date'}),
            'day_offical': forms.DateInput(attrs={'type': 'date'}),
            'recruitment_day': forms.DateInput(attrs={'type': 'date'}),
            'date_of_joining_the_police': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_day_of_birth(self):
        day_of_birth = self.cleaned_data.get('day_of_birth')
        if day_of_birth and day_of_birth > datetime.now().date():
          raise forms.ValidationError("Ngày sinh không thể lớn hơn ngày hiện tại.")
        return day_of_birth
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['emp_num'].disabled = True

#form thêm mới chức danh cho cán bộ
class EmpTitleForm(forms.ModelForm):
    class Meta:
        model = Emp_Title
        fields = ['emp_title','allowances','date_of_receipt','form_of_appointment','decision_number','decision_date','stop_decision_date','file']
        widgets = {
            'emp_num': forms.TextInput(attrs={'readonly': 'readonly'}),
            'full_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'allowances': forms.NumberInput(attrs={'step': '0.01'}),
            'date_of_receipt': forms.DateInput(attrs={'type': 'date'}),
            'decision_date': forms.DateInput(attrs={'type': 'date'}),
            'stop_decision_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_date_of_receipt(self):
        date_of_receipt = self.cleaned_data.get('date_of_receipt')
        if date_of_receipt and date_of_receipt > datetime.now().date():
            raise forms.ValidationError("Ngày nhận chức danh không thể lớn hơn ngày hiện tại.")
        return date_of_receipt
    def clean_decision_date(self):
        decision_date = self.cleaned_data.get('decision_date')
        if decision_date and decision_date > datetime.now().date():
            raise forms.ValidationError("Ngày quyết định không thể lớn hơn ngày hiện tại.")
        return decision_date
    def clean_stop_decision_date(self):
        stop_decision_date = self.cleaned_data.get('stop_decision_date')
        if stop_decision_date and stop_decision_date > datetime.now().date():
            raise forms.ValidationError("Ngày hết hiệu lực quyết định không thể lớn hơn ngày hiện tại.")
        return stop_decision_date
    def clean_stop_decision_date_1(self):
        stop_decision_date = self.cleaned_data.get('stop_decision_date')
        decision_date = self.cleaned_data.get('decision_date')
        if stop_decision_date and stop_decision_date > decision_date:
            raise forms.ValidationError("Ngày hết hiệu lực quyết định không thể lớn hơn ngày quyết định.")
        return stop_decision_date
    