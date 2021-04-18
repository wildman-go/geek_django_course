from django.contrib import admin
from .models import Job, Resume


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
