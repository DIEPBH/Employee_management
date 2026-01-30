from tracemalloc import start
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
import os
from django.core.exceptions import ValidationError
from django.db.models import Q
# Create your models here.
#Bảng phân quyền người dùng theo đơn vị
class usercompany(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.ForeignKey('company', on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    def __str__(self):
        unique_together = ('user', 'company')
        return f"{self.user.username} - {self.company.name}"
    
# Các bảng danh mục
class company(models.Model): #Đơn vị
    id = models.AutoField(primary_key=True)
    name = models.CharField("Đơn vị",max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name

class team(models.Model): #Đội công tác
    id = models.AutoField(primary_key=True)
    name = models.CharField("Đội công tác",max_length=100, unique=True, null=False)
    #leader = models.CharField("Đội trưởng",max_length=100, null=False)
    company = models.ForeignKey(company, on_delete=models.CASCADE, verbose_name="Đơn vị", default='')
    def __str__(self):
        return self.name
    
class level(models.Model): #Cấp bậc
    id = models.AutoField(primary_key=True)
    name = models.CharField("Cấp bậc",max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name
    
class position(models.Model): #Chức vụ
    id = models.AutoField(primary_key=True)
    name = models.CharField("Chức vụ",max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name
    
class education(models.Model): #Trình độ học vấn
    id = models.AutoField(primary_key=True)
    name = models.CharField("Trình độ học vấn",max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name
    
class theoretical_level(models.Model): #Trình độ lý luận chính trị
    id = models.AutoField(primary_key=True)
    name = models.CharField("Trình độ lý luận chính trị",max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name

# Các bảng master
# Bảng thông tin cứng nhân viên
class Emp_information(models.Model):
    MEMBER_CHOICES = [
        ('Y', 'Có'),
        ('N', 'Không'),
    ]
    GENDER_CHOICES = [
        ('M', 'Nam'),
        ('F', 'Nữ'),
    ]
    id = models.AutoField(primary_key=True)
    emp_num = models.CharField("Số hiệu",max_length=10, unique=True, null=False)
    full_name = models.CharField("Họ và tên",max_length=100, null=False)
    current_name = models.CharField("Tên hiện tại",max_length=100, null=False)
    day_of_birth = models.DateField("Ngày sinh",null=False)
    gender = models.CharField("Giới tính",max_length=1, null=False,choices=GENDER_CHOICES)
    place_of_hometown = models.CharField("Quê quán",max_length=100, null=False)
    current_residence = models.CharField("Nơi cư trú hiện tại",max_length=100, null=False)
    nation = models.CharField("Dân tộc",max_length=50, null=False)
    religion = models.CharField("Tôn giáo",max_length=50, null=False)
    family_job = models.CharField("Nghề nghiệp của gia đình",max_length=100, null=False)
    before_job = models.CharField("Công việc trước đây",max_length=100, null=False)
    date_in_group = models.DateField("Ngày vào đoàn",null=False)
    union = models.CharField("Đoàn viên",max_length=1, null=False,choices=MEMBER_CHOICES)
    day_of_joining_the_party = models.DateField("Ngày vào Đảng",null=False)
    day_offical = models.DateField("Ngày chính thức",null=False)
    recruitment_day = models.DateField("Ngày tuyển dụng",null=False)
    date_of_joining_the_police = models.DateField("Ngày vào công an",null=False)
    recruitment_place = models.ForeignKey(company, on_delete=models.CASCADE, verbose_name="Nơi tuyển dụng", default='', null=True)
    recruitment_source = models.CharField("Nguồn tuyển dụng",max_length=100, null=False)
    blood_type = models.CharField("Nhóm máu",max_length=10, null=False)
    appellation = models.CharField("Danh hiệu được phong",max_length=50, null=False)
    keep_records = models.CharField("Địa chỉ hồ sơ",max_length=100, null=False)
    forte_ability = models.CharField("Năng lực nổi bật",max_length=100, null=False)
    Descriptions = models.TextField("Mô tả",null=True)
    avatar = models.ImageField("Ảnh chân dung",upload_to='employee_avatars/', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Người tạo")
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)

    #Xóa avatar khi xóa nhân viên
    @receiver(post_delete, sender='employee.Emp_information')
    def delete_avatar(sender, *args, instance, **kwargs):
        if instance.avatar and os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)
    #Xóa avatar khi thay đổi ảnh mới
    @receiver(pre_save, sender='employee.Emp_information')
    def pre_save_avatar(sender, instance, **kwargs):
        if not instance.pk:
            return False
        try:
            old_avatar = Emp_information.objects.get(pk=instance.pk).avatar
        except Emp_information.DoesNotExist:
            return False
        new_avatar = instance.avatar
        if not old_avatar == new_avatar:
            if old_avatar and os.path.isfile(old_avatar.path):
                os.remove(old_avatar.path)
    #khai báo hàm hiển thị tên nhân viên
    def __str__(self):
        return self.full_name
    @property
    def _name_(self):
        return self.full_name
    
#2 bảng chức danh và chức vụ của nhân viên
class Emp_Title(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên")
    emp_title = models.ForeignKey(position, on_delete=models.CASCADE, verbose_name="Chức danh")
    allowances = models.DecimalField("Phụ cấp", max_digits=10, decimal_places=2, null=False)
    date_of_receipt = models.DateField("Ngày nhận chức danh",null=False)
    form_of_appointment = models.CharField("Hình thức bổ nhiệm",max_length=100, null=False)
    decision_number = models.CharField("Số quyết định",max_length=100, null=False)
    decision_date = models.DateField("Ngày quyết định",null=False)
    stop_decision_date = models.DateField("Ngày dừng quyết định",null=True,blank=True)
    is_active = models.CharField("Hiệu lực", max_length=1, null=True)
    file = models.FileField("File đính kèm",upload_to='employee_titles/', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Người tạo", related_name="emp_titles_created",)
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Người sửa", related_name="emp_titles_updated",)
    update_at = models.DateTimeField("Ngày sửa", auto_now_add=False,null=True)
    # kiểm soát không overlap chức danh cho cùng 1 nhân viên
    def clean(self):
        super().clean()
        start = self.decision_date
        end = self.stop_decision_date

        if end and end < start:
            raise ValidationError("Ngày dừng quyết định >= ngày quyết định")
        qs = Emp_Title.objects.filter(emp=self.emp).exclude(id=self.id)

    # Overlap condition:
    # [start, end] giao nhau với [a, b]
    # end null => b = +inf
        if end:
            qs = qs.filter(
                Q(stop_decision_date__isnull=True, decision_date__lte=end) |
                Q(stop_decision_date__isnull=False, decision_date__lte=end, stop_decision_date__gte=start)
            )
        else:
            qs = qs.filter(Q(stop_decision_date__isnull=True) | Q(stop_decision_date__gte=start))
        if qs.exists():
            raise ValidationError("Khoảng thời gian chức danh bị chồng lấn với bản ghi khác.")
    def __str__(self):
        return self.emp_title
        
    #Xóa file khi xóa bản ghi chức vụ
    @receiver(post_delete, sender='employee.Emp_Title')
    def delete_file(sender, *args, instance, **kwargs):
        if instance.file and os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
    #Xóa file khi thay đổi file mới
    @receiver(pre_save, sender='employee.Emp_Title')
    def pre_save_file(sender, instance, **kwargs):
        if not instance.pk:
            return False
        try:
            old_file = Emp_Title.objects.get(pk=instance.pk).file
        except Emp_Title.DoesNotExist:
            return False
        new_file = instance.file
        if not old_file == new_file:
            if old_file and os.path.isfile(old_file.path):
                os.remove(old_file.path)

#3 Bảng thông tin quy hoạch chức vụ của nhân viên
class Emp_Position(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    position = models.ForeignKey(position, on_delete=models.CASCADE, verbose_name="Chức vụ", default='')
    date_position = models.DateField("Ngày quy hoạch",null=False)
    votes = models.CharField("Số phiếu bầu",max_length=100, null=False)
    date_stop_position = models.DateField("Ngày dừng quy hoạch",null=True, blank=True)
    reason_stop_position = models.CharField("Lý do dừng quy hoạch",max_length=100, null=False)
    is_active = models.CharField("Hiệu lực", max_length=1, null=True)
    file = models.FileField("File đính kèm",upload_to='employee_Position/', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Người tạo", related_name="emp_Position_created",)
    created_at = models.DateTimeField("Ngày tạo", auto_now_add=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Người sửa", related_name="emp_Position_updated",)
    update_at = models.DateTimeField("Ngày sửa", auto_now_add=False,null=True)

    # kiểm soát không overlap chức danh cho cùng 1 nhân viên
    def clean(self):
        super().clean()
        start = self.date_position
        end = self.date_stop_position

        if end and end < start:
            raise ValidationError("Ngày dừng quyết định >= ngày quyết định")
        qs = Emp_Position.objects.filter(emp=self.emp).exclude(id=self.id)

    # Overlap condition:
    # [start, end] giao nhau với [a, b]
    # end null => b = +inf
        if end:
            qs = qs.filter(
                Q(date_stop_position__isnull=True, date_position__lte=end) |
                Q(date_stop_position__isnull=False, date_position__lte=end, date_stop_position__gte=start)
            )
        else:
            qs = qs.filter(Q(date_stop_position__isnull=True) | Q(date_stop_position__gte=start))
        if qs.exists():
            raise ValidationError("Khoảng thời gian chức danh bị chồng lấn với bản ghi khác.")
        
    def __str__(self):
        return self.position
        
    #Xóa file khi xóa bản ghi chức vụ
    @receiver(post_delete, sender='employee.Emp_Title')
    def delete_file(sender, *args, instance, **kwargs):
        if instance.file and os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
    #Xóa file khi thay đổi file mới
    @receiver(pre_save, sender='employee.Emp_Title')
    def pre_save_file(sender, instance, **kwargs):
        if not instance.pk:
            return False
        try:
            old_file = Emp_Title.objects.get(pk=instance.pk).file
        except Emp_Title.DoesNotExist:
            return False
        new_file = instance.file
        if not old_file == new_file:
            if old_file and os.path.isfile(old_file.path):
                os.remove(old_file.path)

    def __str__(self):
        return self.position.name

#4 Bảng thông tin cấp ủy Đảng
class Emp_PartyCommittee(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    party_committee = models.CharField("Đảng ủy",max_length=100, unique=True, null=False)
    from_date = models.DateField("Từ ngày",null=False)
    to_date = models.DateField("Đến ngày",null=False)

    def __str__(self):
        return self.party_committee

#5 Bảng thông tin đào tạo
class Emp_Training(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    from_date = models.DateField("Từ ngày",null=False)
    to_date = models.DateField("Đến ngày",null=False)
    specialized = models.CharField("Chuyên môn",max_length=100, null=False)
    formality = models.CharField("Hình thức đào tạo",max_length=100, null=False)
    level = models.CharField("Trình độ",max_length=100, null=False)
    training_school = models.CharField("Trường đào tạo",max_length=100, null=False)
    equal_number = models.CharField("Số bằng",max_length=100, null=False)

    def __str__(self):
        return self.specialized

#6 Bảng thông tin quá trình lương
class Emp_SalaryProcess(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    level = models.CharField("Cấp bậc",max_length=50, null=False)
    date_issue = models.DateField("Ngày nhận cấp bậc",null=False)
    salary_coefficient = models.DecimalField("Hệ số lương", max_digits=10, decimal_places=2, null=False)
    date_receive = models.DateField("Ngày nhận hệ số lương",null=False)
    decision_number = models.CharField("Số quyết định",max_length=100, null=False)
    decision_date = models.DateField("Ngày quyết định",null=False)
    decision_number = models.CharField("Số quyết định",max_length=100, null=False)

    def __str__(self):
        return self.level
    
#7 Bảng thông tin khen thưởng
class Emp_Awards(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    date_issue= models.DateField("Ngày nhận khen thưởng",null=False)
    forms_of_reward = models.CharField("Hình thức khen thưởng",max_length=100, null=False)
    award_level = models.CharField("Cấp khen thưởng",max_length=100, null=False)

    def __str__(self):
        return self.forms_of_reward
    
#8 Bảng thông tin kỷ luật
class Emp_Discipline(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    discipline_party = models.CharField("Kỷ luật Đảng",max_length=100, null=False)
    date_issue_party =  models.DateField("Ngày kỷ luật Đảng",null=False)
    discipline_government =     models.CharField("Kỷ luật chính quyền",max_length=100, null=False)
    date_issue_government = models.DateField("Ngày kỷ luật chính quyền",null=False)
    violations = models.CharField("Vi phạm",max_length=100, null=False)
    summary_of_violations = models.TextField("Tóm tắt vi phạm", null=False)
    date_recognizes_progress = models.DateField("Ngày nhận tiến bộ",null=False)

    def __str__(self):
        return self.discipline_party

#9 Bảng thông tin thân nhân
class Emp_Relationship (models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    relationship_type = models.CharField("Loại quan hệ",max_length=100, null=False)
    full_name = models.CharField("Họ và tên thân nhân",max_length=100, null=False)
    date_of_birth = models.DateField("Năm sinh",null=False)
    career = models.CharField("Nghề nghiệp",max_length=100, null=False)
    title = models.CharField("Chức vụ",max_length=100, null=False)
    work_unit = models.CharField("Nơi làm việc",max_length=100, null=False)
    address = models.CharField("Địa chỉ",max_length=100, null=False)

    def __str__(self):
        return self.id

#10 Bảng thông tin ra nước Ngoài
class Emp_Foreign(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    from_date = models.DateField("Từ ngày",null=False)
    to_date = models.DateField("Đến ngày",null=False)
    nation = models.CharField("Quốc gia",max_length=100, null=False)
    reason = models.TextField("Lý do đến", null=False)

    def __str__(self):
        return self.id
    
#11 Bảng thông tin tham gia quân đội
class Emp_Army(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    date_join = models.DateField("Ngày nhập ngũ",null=False)
    level = models.CharField("Bậc hàm",max_length=50, null=False)
    position = models.CharField("Chức vụ",max_length=100, null=False)
    place = models.CharField("Nơi làm việc",max_length=100, null=False)
    date_out = models.DateField("Ngày xuất ngũ",null=False)

    def __str__(self):
        return self.id

#12 Bảng thông tin sức khỏe
class Emp_Health(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    date_check = models.DateField("Ngày kiểm tra sức khỏe",null=False)
    heal_check = models.CharField("Tình trạng sức khỏe",max_length=100, null=False)
    wounded_soldiers = models.CharField("Thương binh",max_length=100, null=False)
    agency = models.CharField("Đơn vị khám bệnh",max_length=100, null=False)    

    def __str__(self):
        return self.id

#13 Bảng thông tin kết quả công tác
class Emp_ResultWork(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    year = models.CharField("Năm",max_length=4, null=False)
    result = models.CharField("Kết quả công tác",max_length=100, null=False)
    comments = models.TextField("Nhận xét đánh giá", null=True)   

    def __str__(self):
        return self.id

#14 Bảng thông tin đặc điểm lịch sử
class Emp_History(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    emp_history = models.TextField("Đặc điểm lịch sử", null=False)

    def __str__(self):
        return self.id

#15 Bảng thông tin thân nhân ở nước ngoài
class Emp_WithForeigners(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    relationship = models.CharField("Quan hệ",max_length=100, null=False)
    full_name = models.CharField("Họ và tên thân nhân",max_length=100, null=False)
    date_of_birth = models.DateField("Năm sinh",null=False)
    job = models.CharField("Nghề nghiệp",max_length=100, null=False)
    address = models.CharField("Địa chỉ",max_length=100, null=False)
    nation = models.CharField("Hiện ở Quốc gia",max_length=100, null=False)
    
    def __str__(self):
        return self.id

#16 Bảng thông tin thôi việc
class Emp_Disengaged(models.Model):
    id = models.AutoField(primary_key=True)
    emp = models.ForeignKey(Emp_information,to_field='emp_num',db_column='emp_num', on_delete=models.CASCADE, verbose_name="Nhân viên", default='')
    date_out = models.DateField("Ngày thôi việc",null=False)
    reason = models.CharField("Lý do",max_length=100, null=False)
    address = models.CharField("Nơi chuyển đến",max_length=100, null=False)
    decision = models.CharField("Số quyết định",max_length=100, null=False)

    def __str__(self):
        return self.id