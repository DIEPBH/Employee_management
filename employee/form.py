from django import forms
from .models import Emp_information
from datetime import datetime
from django.core.exceptions import ValidationError

#
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