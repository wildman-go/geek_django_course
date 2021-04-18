from django.contrib import admin
from .models import Job, Resume
from interview.models import Candidate
from django.contrib import messages
from datetime import datetime


def enter_interview_process(modeladmin, request, queryset):
    candidate_names = ""
    for query in queryset:
        candidate = Candidate()
        # 把query对象里面的所有属性拷贝到candidate对象中
        candidate.__dict__.update(query.__dict__)
        candidate.created_date = datetime.now()
        candidate.modified_date = datetime.now()
        candidate_names = candidate.username + ',' + candidate_names
        candidate.creator = request.user.username
        candidate.save()
    messages.add_message(request, messages.INFO, '候选人: %s 已成功进入面试流程' % (candidate_names))


enter_interview_process.short_description = '进入面试流程'


# Register your models here.

class JobAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')
    list_display = ['job_name', 'job_type', 'job_city', 'creator', 'created_date', 'modified_date']

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class ResumeAdmin(admin.ModelAdmin):
    list_display = ['username', 'applicant', 'city', 'apply_position', 'bachelor_school', 'master_school', 'major',
                    'created_date']

    readonly_fields = ['created_date', 'modified_date', 'applicant']
    actions = [enter_interview_process]

    fieldsets = (
        (None,
         {'fields': ('applicant', ('username', 'city', 'phone'),
                     ('email', 'apply_position', 'born_address', 'gender'),
                     ('bachelor_school', 'master_school'), ('major', 'degree'), ('created_date', 'modified_date'),
                     'candidate_introduction', 'work_experience', 'project_experience')}),
    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super(ResumeAdmin, self).save_model(request, obj, form, change)


admin.site.register(Job, JobAdmin)
admin.site.register(Resume, ResumeAdmin)
