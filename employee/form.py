from django import forms
from .models import Emp_Army,Emp_Health, Emp_Discipline, Emp_Foreign, Emp_Relationship, Emp_SalaryProcess, Emp_Training, Emp_information,Emp_Title,Emp_Position, Emp_PartyCommittee, Emp_workProcess, Emp_Awards, award_type, award_level
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
    def clean(self):
        cleaned = super().clean()
        stop_decision_date = self.cleaned_data.get('stop_decision_date')
        decision_date = self.cleaned_data.get('decision_date')
        if decision_date and stop_decision_date:
            if stop_decision_date and stop_decision_date < decision_date:
                raise forms.ValidationError("Ngày hết hiệu lực quyết định không thể lớn hơn ngày quyết định.")
        return cleaned
    

#form import từ file excel
class EmpImportForm(forms.Form):
    excel_file = forms.FileField() 


#form thêm mới quy hoạch cho cán bộ
class EmpPositionForm(forms.ModelForm):
    class Meta:
        model = Emp_Position
        fields = ['position','date_position','votes','date_stop_position','reason_stop_position','file']
        widgets = {
            'votes': forms.NumberInput(attrs={'step':'1'}),
            'date_position': forms.DateInput(attrs={'type': 'date'}),
            'date_stop_position': forms.DateInput(attrs={'type': 'date'}),
            'reason_stop_position': forms.Textarea
        }
    def clean_date_position(self):
        date_position = self.cleaned_data.get('date_position')
        if date_position and date_position > datetime.now().date():
            raise forms.ValidationError("Ngày nhận quy hoạch không thể lớn hơn ngày hiện tại.")
        return date_position
    def clean_date_stop_position(self):
        date_stop_position = self.cleaned_data.get('date_stop_position')
        if date_stop_position and date_stop_position > datetime.now().date():
            raise forms.ValidationError("Ngày dừng quy hoạch không thể lớn hơn ngày hiện tại.")
        return date_stop_position
    def clean_date_stop_position_1(self):
        date_stop_position = self.cleaned_data.get('date_stop_position')
        date_position = self.cleaned_data.get('date_position')
        if date_stop_position and date_stop_position > date_position:
            raise forms.ValidationError("Ngày hết hiệu lực quyết định không thể lớn hơn ngày quyết định.")
        return date_stop_position
    

#form thêm mới thông tin đảng ủy cho cán bộ
class EmpPartyCommittee(forms.ModelForm):
    class Meta:
        model = Emp_PartyCommittee
        fields = ['party_committee','from_date','to_date','file']
        widgets = {
            'party_committee': forms.Select(),
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_from_date(self):
        from_date = self.cleaned_data.get('from_date')
        if from_date and from_date > datetime.now().date():
            raise forms.ValidationError("Ngày bắt đầu không thể lớn hơn ngày hiện tại.")
        return from_date
    def clean_to_date(self):
        to_date = self.cleaned_data.get('to_date')
        if to_date and to_date > datetime.now().date():
            raise forms.ValidationError("Ngày kết thúc không thể lớn hơn ngày hiện tại.")
        return to_date
    def clean(self):
        cleaned = super().clean()
        to_date = self.cleaned_data.get('to_date')
        from_date = self.cleaned_data.get('from_date')
        if from_date and to_date and to_date < from_date:
            raise forms.ValidationError("Ngày kết thúc không thể nhỏ hơn ngày bắt đầu.")
        return cleaned
    
#form thêm mới thông tin đào tạo cho cán bộ
class EmpTraining(forms.ModelForm):
    class Meta:
        model = Emp_Training
        fields = ['from_date','to_date','level','specialized','formality','level','training_school','equal_number','file']
        widgets = {
            'level': forms.Select(),
            'formality': forms.Select(),
            'specialized': forms.TextInput(attrs={'class': 'form-control'}),
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_from_date(self):
        from_date = self.cleaned_data.get('from_date')
        if from_date and from_date > datetime.now().date():
            raise forms.ValidationError("Ngày bắt đầu không thể lớn hơn ngày hiện tại.")
        return from_date
    def clean_to_date(self):
        to_date = self.cleaned_data.get('to_date')
        if to_date and to_date > datetime.now().date():
            raise forms.ValidationError("Ngày kết thúc không thể lớn hơn ngày hiện tại.")
        return to_date
    def clean(self):
        cleaned = super().clean()
        to_date = self.cleaned_data.get('to_date')
        from_date = self.cleaned_data.get('from_date')
        if from_date and to_date and to_date < from_date:
            raise forms.ValidationError("Ngày kết thúc không thể nhỏ hơn ngày bắt đầu.")
        return cleaned
    
#form thêm mới thông tin quá trình công tác cho cán bộ
class EmpWorkProcess(forms.ModelForm):
    class Meta:
        model = Emp_workProcess
        fields = ['from_date','to_date','emp_title','work','emp_company','decision_number','decision_date','file']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
            'emp_title': forms.Select(),
            'work': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_company': forms.Select(),
            'decision_number': forms.TextInput(attrs={'class': 'form-control'}),
            'decision_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_from_date(self):
        from_date = self.cleaned_data.get('from_date')
        if from_date and from_date > datetime.now().date():
            raise forms.ValidationError("Ngày bắt đầu không thể lớn hơn ngày hiện tại.")
        return from_date
    def clean_to_date(self):
        to_date = self.cleaned_data.get('to_date')
        if to_date and to_date > datetime.now().date():
            raise forms.ValidationError("Ngày kết thúc không thể lớn hơn ngày hiện tại.")
        return to_date
    def clean(self):
        cleaned = super().clean()
        to_date = self.cleaned_data.get('to_date')
        from_date = self.cleaned_data.get('from_date')
        if from_date and to_date and to_date < from_date:
            raise forms.ValidationError("Ngày kết thúc không thể nhỏ hơn ngày bắt đầu.")
        return cleaned
    
#form thêm mới thông tin quá trình lương cho cán bộ
class EmpSalaryProcess(forms.ModelForm):
    class Meta:
        model = Emp_SalaryProcess
        fields = ['level','date_issue','salary_coefficient','date_receive','decision_number','decision_date','file']
        widgets = {
            'level': forms.Select(),
            'date_receive': forms.DateInput(attrs={'type': 'date'}),
            'date_issue': forms.DateInput(attrs={'type': 'date'}),
            'emp_title': forms.Select(),
            'work': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_company': forms.Select(),
            'decision_number': forms.TextInput(attrs={'class': 'form-control'}),
            'decision_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def clean_date_issue(self):
        date_issue = self.cleaned_data.get('date_issue')
        if date_issue and date_issue > datetime.now().date():
            raise forms.ValidationError("Ngày ban hành không thể lớn hơn ngày hiện tại.")
        return date_issue
    def clean_date_receive(self):
        date_receive = self.cleaned_data.get('date_receive')
        if date_receive and date_receive > datetime.now().date():
            raise forms.ValidationError("Ngày nhận không thể lớn hơn ngày hiện tại.")
        return date_receive
    def clean_decision_date(self):
        decision_date = self.cleaned_data.get('decision_date')
        if decision_date and decision_date > datetime.now().date():
            raise forms.ValidationError("Ngày quyết định không thể lớn hơn ngày hiện tại.")
        return decision_date
    
#form thêm mới thông tin quá trình khen thưởng cho cán bộ
class EmpAwardForm(forms.ModelForm):
    class Meta:
        model = Emp_Awards
        fields = ['date_issue','award_type','award_level','file']
        widgets = {
            'date_issue': forms.DateInput(attrs={'type': 'date'}),
            'award_type': forms.Select(),
            'award_level': forms.Select(),
        }
    def clean_date_issue(self):
        date_issue = self.cleaned_data.get('date_issue')
        if date_issue and date_issue > datetime.now().date():
            raise forms.ValidationError("Ngày ban hành không thể lớn hơn ngày hiện tại.")
        return date_issue
    
#form thêm mới thông tin kỷ luật cán bộ
class EmpDisciplineForm(forms.ModelForm):
    class Meta:
        model = Emp_Discipline
        fields = ['discipline_party','date_issue_party','discipline_government','date_issue_government','violations','summary_of_violations','date_recognizes_progress','file']
        widgets = {
            'date_issue_party': forms.DateInput(attrs={'type': 'date'}),
            'date_issue_government' : forms.DateInput(attrs={'type': 'date'}),
            'date_recognizes_progress': forms.DateInput(attrs={'type': 'date'}),
            'summary_of_violations': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def clean_date_issue_party(self):
        date_issue = self.cleaned_data.get('date_issue_party')
        if date_issue and date_issue > datetime.now().date():
            raise forms.ValidationError("Ngày ban hành không thể lớn hơn ngày hiện tại.")
        return date_issue
    def clean_date_issue_government(self):
        date_issue = self.cleaned_data.get('date_issue_government')
        if date_issue and date_issue > datetime.now().date():
            raise forms.ValidationError("Ngày ban hành không thể lớn hơn ngày hiện tại.")
        return date_issue
    def clean_date_recognizes_progress(self):
        date_recognizes_progress = self.cleaned_data.get('date_recognizes_progress')
        if date_recognizes_progress and date_recognizes_progress > datetime.now().date():
            raise forms.ValidationError("Ngày nhận xét tiến bộ không thể lớn hơn ngày hiện tại.")
        return date_recognizes_progress
    def clean(self):
        cleaned_data = super().clean()
        date_issue_party = self.cleaned_data.get('date_issue_party')
        date_issue_government = self.cleaned_data.get('date_issue_government')
        discipline_party = self.cleaned_data.get('discipline_party')
        discipline_government = self.cleaned_data.get('discipline_government')
        if discipline_party and not date_issue_party:
            raise forms.ValidationError("Vui lòng nhập ngày ban hành kỷ luật đảng.")
        if discipline_government and not date_issue_government:
            raise forms.ValidationError("Vui lòng nhập ngày ban hành kỷ luật chính quyền.")
    
    
#form thêm mới thông tin thân nhân của cán bộ
class EmpRelationshipForm(forms.ModelForm):
    class Meta:
        model = Emp_Relationship
        fields = ['relationship_type','full_name','date_of_birth','career','title','work_unit','address','address','file']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
                'relationship_type': forms.Select(),
                'career': forms.TextInput(attrs={'class': 'form-control'}),
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'work_unit': forms.TextInput(attrs={'class': 'form-control'}),
                'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > datetime.now().date():
            raise forms.ValidationError("Ngày sinh không thể lớn hơn ngày hiện tại.")
        return date_of_birth


#form thêm mới thông tin ra nước ngoài của cán bộ
class EmpForeignForm(forms.ModelForm):
    class Meta:
        model = Emp_Foreign
        fields = ['from_date','to_date','nation','reason','file']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
            'nation': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control'}),

        }
    def clean_from_date(self):
        from_date = self.cleaned_data.get('from_date')
        if from_date and from_date > datetime.now().date():
            raise forms.ValidationError("Ngày đi không thể lớn hơn ngày hiện tại.")
        return from_date
    def clean_to_date(self):
        to_date = self.cleaned_data.get('to_date')
        if to_date and to_date > datetime.now().date():
            raise forms.ValidationError("Ngày về không thể lớn hơn ngày hiện tại.")
        return to_date
    def clean(self):
        cleaned = super().clean()
        to_date = self.cleaned_data.get('to_date')
        from_date = self.cleaned_data.get('from_date')
        if from_date and to_date and to_date < from_date:
            raise forms.ValidationError("Ngày về không thể nhỏ hơn ngày đi.")
        return cleaned
    

#form thêm mới thông tin nhập ngũ của cán bộ
class EmpArmyForm(forms.ModelForm):
    class Meta:
        model = Emp_Army
        fields = ['date_join','level','position','place','date_out','file']
        widgets = {
            'date_join': forms.DateInput(attrs={'type': 'date'}),
            'date_out': forms.DateInput(attrs={'type': 'date'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
    def clean_date_join(self):
        date_join = self.cleaned_data.get('date_join')
        if date_join and date_join > datetime.now().date():
            raise forms.ValidationError("Ngày nhập ngũ không thể lớn hơn ngày hiện tại.")
        return date_join
    def clean_date_out(self):
        date_out = self.cleaned_data.get('date_out')
        if date_out and date_out > datetime.now().date():
            raise forms.ValidationError("Ngày xuất ngũ không thể lớn hơn ngày hiện tại.")
        return date_out
    def clean(self):
        cleaned = super().clean()
        date_out = self.cleaned_data.get('date_out')
        date_join = self.cleaned_data.get('date_join')
        if date_join and date_out and date_out < date_join:
            raise forms.ValidationError("Ngày xuất ngũ không thể nhỏ hơn ngày nhập ngũ.")
        return cleaned
    
#form thêm mới thông tin Sức khỏe của cán bộ
class EmpHealthForm(forms.ModelForm):
    class Meta:
        model = Emp_Health
        fields = ['date_check','heal_check','wounded_soldiers','agency','file']
        widgets = {
            'date_check': forms.DateInput(attrs={'type': 'date'}),
            'agency': forms.Select(attrs={'class': 'form-control'}),
            'heal_check': forms.Textarea(attrs={'class': 'form-control'}),
            'wounded_soldiers': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
    def clean_date_check(self):
        date_check = self.cleaned_data.get('date_check')
        if date_check and date_check > datetime.now().date():
            raise forms.ValidationError("Ngày kiểm tra sức khỏe không thể lớn hơn ngày hiện tại.")
        return date_check