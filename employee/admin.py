from django.contrib import admin
from .models import Emp_information, company,Emp_Title,position, committee, formality, Traning_level,level, award_level, award_type, relationship_type
# Register your models here.

admin.site.register(Emp_information)
admin.site.register(company)
admin.site.register(Emp_Title)
admin.site.register(position)
admin.site.register(committee)
admin.site.register(formality)
admin.site.register(Traning_level)
admin.site.register(level)
admin.site.register(award_level)
admin.site.register(award_type)
admin.site.register(relationship_type)