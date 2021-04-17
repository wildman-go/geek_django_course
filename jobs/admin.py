from django.contrib import admin
from .models import Job


# Register your models here.

class JobAdmin(admin.ModelAdmin):
    list_display = ['job_name', 'job_type', 'job_city', 'creator', 'created_date', 'modified_date']


admin.site.register(Job, JobAdmin)
